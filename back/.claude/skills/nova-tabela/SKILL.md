---
name: nova-tabela
description: Cria uma tabela de domínio com todas as convenções e todos os registros que o resto do sistema lê — prefixo de 3 letras, PK UUID, exclusão lógica, vínculos no ForeignKeyMap, chaves deferrable, nome legível, observer de auditoria, testes de guarda. Use sempre que uma migration criar tabela nova ou acrescentar coluna de vínculo a uma existente.
---

# Nova tabela (ou novo vínculo)

Uma tabela esquecida num dos registros abaixo fica **invisível** para a exclusão em
cascata, para o console de dados, para a auditoria ou para a tela. Os testes de guarda
pegam parte disso; esta skill pega o resto.

Leia antes: `docs/arquitetura/BANCO.md` e `DADOS.md`.

## 1. Migration (no módulo dono)

- Nome no plural, **prefixo de 3 letras** em todas as colunas (confira que o prefixo é novo).
- PK `<pre>_id` UUID; `<pre>_created_at`, `<pre>_updated_at`, `<pre>_deleted_at`.
- Coluna do tenant (`entity_ent_id`) se a tabela tem escopo de tenant.
- Vínculo: coluna `{tabela_pai}_{pk_do_pai}`, com **índice** `ix_<tabela>_<coluna>`.
- Chave estrangeira **só no PostgreSQL**, no padrão `fk_<tabela>_<coluna>`
  `DEFERRABLE INITIALLY DEFERRED`. **Nunca** `->constrained()`.
- `down()` que reverte de verdade. Teste `migrate`, `rollback`, `migrate` num banco de rascunho.
- Padrão de coluna nova que afeta quem já está em produção: migration nova, nunca editar
  uma que já rodou.
- Coluna que dispara comunicação com o usuário final nasce **desligada** (opt-in).

## 2. Model + observer

- `HasUuids`, `SoftDeletes`, `Entityable` (se tenant), constantes das colunas de tempo.
- Observer que estende o `AuditObserver`, com as colunas sensíveis em `$hidden`.
- Relação com model de outro módulo: por `config('models.*')`, nunca importando a classe.

## 3. Os registros (todos, na mesma entrega)

| Onde | O que acrescentar |
| --- | --- |
| `ForeignKeyMap::KEYS` | uma linha por vínculo: filha, coluna, pai, PK do pai, **anulável igual ao da coluna** |
| `ForeignKeyMap::PRIMARY_KEYS` | a tabela e a PK |
| `ForeignKeyMap::READ_ONLY` | se for trilha, registro de acesso ou de envio |
| nome legível (`DataExplorer::LABELS`) | as partes que formam o nome da linha (`@vínculo` para o nome do pai) |
| palavras de status | cada valor de enum com a palavra em português (a mesma do front) |
| `docs/arquitetura/BANCO.md` | a linha na tabela de ownership |
| `config/models.php` | se outro módulo vai se relacionar com ela |

## 4. Decidir e registrar

- **Anulável ou obrigatório?** Obrigatório = o filho é excluído junto com o pai na cascata.
  Anulável = o filho fica e perde a referência. Erre aqui e a cascata apaga o que não devia.
- **Índice único × exclusão lógica**: trate o recadastro de um excluído no fluxo, ou use
  índice parcial. Registre a escolha.
- **Quem vê?** A tabela ganha tela própria, vira aba de um pai, ou as duas?

## 5. Testes

- Os testes de guarda do mapa (coluna `*_id` no mapa; tabela em `PRIMARY_KEYS`; anulável
  batendo) verdes.
- Recorte de tenant; auditoria da criação/alteração/exclusão; cascata com esta tabela
  como filha (prévia lista a tabela no lugar certo: `deletes` ou `kept`).
- `composer lint && composer lint:check && composer test`.

## 6. Avisar o front (seção "Para o front" do relatório)

Rótulo da tabela (plural) e de cada coluna; palavras e cores de status; de quem ela é aba;
se tem tela própria; ícone sugerido.
