# Dados — vínculos, exclusão em cascata e o console do nível mais alto

> Complementa [`BANCO.md`](BANCO.md). Aquele documento diz como uma tabela nasce; este diz
> como as tabelas se **ligam**, como um registro **sai** e **volta**, e como o nível mais
> alto enxerga e corrige qualquer dado **dentro do produto**.
>
> Implementação de referência: `app-modules/core/src/Support/{ForeignKeyMap,CascadeDeletion,DataExplorer,SystemOverview}.php`
> e `app-modules/core/src/Admin/Http/AdminDataController.php` do Fibro+.

## 1. `ForeignKeyMap` — a fonte única dos vínculos

Um arquivo no `core` lista **todos** os vínculos entre tabelas. Ninguém mais declara
relação entre tabelas em outro lugar "de verdade": tudo lê daqui.

```php
final class ForeignKeyMap
{
    /** tabela filha, coluna, tabela pai, PK do pai, anulável */
    private const KEYS = [
        ['units',    'entity_ent_id', 'entities', 'ent_id', false],
        ['patients', 'units_unt_id',  'units',    'unt_id', true],
        // ...
    ];

    private const PRIMARY_KEYS = ['entities' => 'ent_id', 'units' => 'unt_id', /* toda tabela do banco */];

    /** Trilhas e registros de acesso: só leitura, nunca editados, excluídos ou levados em cascata. */
    public const READ_ONLY = ['audit_logs', /* registros de acesso, envios, ... */];

    public static function all(): array;
    public static function childrenOf(string $parent): array;
    public static function parentsOf(string $table): array;
    public static function primaryKey(string $table): string;
}
```

Quem lê o mapa:

| Consumidor | Para quê |
| --- | --- |
| a migration das chaves estrangeiras | cria as constraints reais a partir da lista |
| `CascadeDeletion` | sabe o que depende de quê |
| `DataExplorer` | pais e filhas de cada tabela (as abas da tela genérica), nome legível por vínculo |
| auditoria | resolve o nome de cada id do antes/depois |
| visão geral do sistema | contagens e distribuições |

`audit_logs` fica **fora** do mapa de propósito: a trilha sobrevive a quem a gerou.

### Testes de guarda (quebram o CI)

1. Toda coluna `*_id` que aponta para outra tabela está no mapa.
2. Toda tabela do banco (fora a infraestrutura do framework) está em `PRIMARY_KEYS`.
3. O "anulável" de cada vínculo do mapa bate com a coluna real.

Sem o item 2, uma tabela nova fica invisível para a cascata e para o console; sem o 3,
excluir um pai apaga logicamente filhos que só deviam perder a referência. Os dois já
aconteceram.

## 2. Chaves estrangeiras reais

- Padrão único: `fk_<tabela>_<coluna>`, `DEFERRABLE INITIALLY DEFERRED`, `NO ACTION`,
  criada **só no PostgreSQL** (a suíte em sqlite não as tem; a cascata funciona igual
  porque lê o mapa).
- **Nunca** `->constrained()` numa migration: cria a constraint fora do padrão e fora do mapa.
- Toda coluna de vínculo tem índice (`ix_<tabela>_<coluna>`).
- Tabela nova cria as próprias chaves no padrão, na própria migration, e entra no mapa
  **na mesma entrega**.
- A migration geral de chaves **pula** vínculos cuja tabela/coluna ainda não existe e
  **aborta listando os órfãos** (tabela.coluna e quantidade) em vez de apagar qualquer coisa.
- `DEFERRABLE` permite carregar e restaurar dados numa transação sem depender da ordem
  das tabelas.

## 3. Exclusão: três níveis, nenhum físico

| O quê | Quem | Como |
| --- | --- | --- |
| **Arquivar** um cadastro | quem gere o cadastro | flag `*_active`; sai das escolhas novas; o que existe continua; restaurar é idempotente |
| **Excluir** um registro (lógico, em cascata) | só o nível mais alto | `*_deleted_at` no registro e nos dependentes **obrigatórios**; some das telas; restaurável |
| **Apagar de verdade** | ninguém | não existe por nenhuma via |

### `CascadeDeletion`

```
GET    …/admin/data/{tabela}/{id}/delete-preview[?restore=1]
       → { deletes: [{ table, label, count }], kept: [{ table, label, count, reason }], total }
DELETE …/admin/data/{tabela}/{id}   { confirm: true, expected_total }
POST   …/admin/data/{tabela}/{id}/restore   { expected_total }
```

- Marca o registro raiz e, recursivamente, os dependentes de vínculo **obrigatório**
  (coluna NOT NULL).
- **Ficam** (`kept`): dependentes de vínculo opcional, tabelas sem exclusão lógica e as
  `READ_ONLY`.
- Dentro de uma transação, **refaz o plano** e confere `expected_total`: mudou → **409**
  (a tela mostra a prévia nova).
- Grava **uma** linha de auditoria (`deleted`/`restored`) com o resumo da cascata e o operador.
- **Restaurar** traz de volta também os **pais** excluídos (não os irmãos), para o
  registro não voltar órfão.
- Guardas: tabela `READ_ONLY`, desconhecida ou sem exclusão lógica → 403; inexistente →
  404; estado errado (já excluído/já ativo) → 409.

### Exclusão lógica × índice único

Índice único comum **não ignora** linha excluída: recadastrar um documento excluído daria
erro 500. Trate no fluxo (procurar entre os excluídos e responder com mensagem clara que
aponta para a restauração) ou use índice único parcial (`WHERE deleted_at IS NULL`).
Escolha uma das duas por tabela e registre aqui.

## 4. Console de dados (o nível mais alto vê e corrige tudo, dentro do produto)

Não é uma área separada: cada tabela é uma tela normal do painel. O back fornece um
explorador genérico para as tabelas que não têm endpoint próprio e para a edição ampla.

| Chamada | Devolve |
| --- | --- |
| `GET …/admin/data` | todas as tabelas: total, ativos, excluídos, `read_only`, `soft_delete`, pais e filhas |
| `GET …/admin/data/{tabela}` | lista paginada (`q`, `order`, `status=active|deleted|all`, `column`+`value`), com `labels`, `parents`, `columns` |
| `GET …/admin/data/{tabela}/{id}` | todas as colunas, `title`, `parents[]`, `children[]` |
| `GET …/admin/data/{tabela}/options?q=` | até 30 ativos, para os selects de vínculo |
| `PATCH …/admin/data/{tabela}/{id} { changes }` | edição ampla |
| `GET …/admin/data/overview` | visão geral: totais e distribuições |

Regras da edição ampla:

- **Editável**: toda coluna, **menos** chave primária, `*_created_at`/`*_updated_at`/
  `*_deleted_at` e segredos (`password`, `remember_token`, `secret`, códigos de
  recuperação), que **nunca saem** da API.
- Coerção por tipo com 422 em português; vínculo precisa existir.
- Tabelas `READ_ONLY`: 403.
- Grava direto e audita antes/depois **só das colunas alteradas**, na mesma transação.
- **Atenção, e diga isso na tela**: esta via não roda observers, eventos, máquinas de
  estado nem invariantes do domínio. Trocar um status por aqui não dispara nada. É
  ferramenta de correção, não de operação.
- Só o nível mais alto, checado explicitamente; limite de requisições.

## 5. Nome legível de qualquer linha

`DataExplorer::LABELS`: por tabela, as partes que formam o nome (`['name']`,
`['@doctors_dtr_id', '@units_unt_id']`, `['@patients_pat_id', 'kind', 'sent_at']`).
Tabela nova **entra aqui** na mesma entrega; sem isso a tela mostra "Registro sem nome".

## 6. Dados entre ambientes

- Dado real (desenvolvimento, homologação, produção) vive em **PostgreSQL**. sqlite
  `:memory:` é só da suíte de testes.
- Carga/restauração: uma transação só, `TRUNCATE` + carga, depois de um backup; teste o
  roteiro num banco de rascunho recém-migrado; carga de catálogo roda duas vezes para
  provar que é idempotente.
- Catálogo para produção = só tabelas globais, sem linhas excluídas ou de teste. Nunca
  pessoas, contas ou entidades.
- Migration que já rodou em produção **não se edita**: mudança de padrão é migration nova.
- Código de consulta roda nos dois bancos (`LOWER(CAST(col AS TEXT)) LIKE`); consulta
  agregada nova é testada também no PostgreSQL de verdade.
- **Falha de auditoria dentro de uma transação aborta a transação no PostgreSQL** (o
  `try/catch` engole a exceção, mas a transação fica inválida). Migration de dados que
  usa models de hoje pode quebrar num banco vazio: prefira `DB::table` em migration de dados.

## 7. Lista de conferência de uma tabela nova

- [ ] Prefixo de 3 letras, PK UUID, exclusão lógica, colunas de tempo com prefixo ([`BANCO.md`](BANCO.md)).
- [ ] Vínculos no `ForeignKeyMap` (com o anulável certo) e a tabela em `PRIMARY_KEYS`.
- [ ] Trilha/registro de acesso? Também em `READ_ONLY`.
- [ ] Chaves no padrão `fk_…` deferrable + índice, só no PostgreSQL.
- [ ] Entrada em `DataExplorer::LABELS`; palavras de status no mapa.
- [ ] Observer de auditoria; colunas sensíveis em `$hidden`.
- [ ] Coluna auxiliar de busca sem acento, se a tabela tem busca por nome.
- [ ] Testes de guarda verdes.
- [ ] O front foi avisado: rótulo da tabela e das colunas, aba no pai.
