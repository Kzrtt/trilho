# Painel — o contrato que a API entrega para a interface

> A interface dos sistemas feitos com este kit segue um padrão fixo (lista → modal de
> detalhe com abas → formulário; nunca ID cru; tudo editável; exclusão lógica). Esse
> padrão **só fecha se a API devolver o que a tela precisa**. Este documento é o lado do
> back desse acordo. O lado do front é `docs/padrao/13-CONTRATO-COM-A-API.md` do
> repositório da interface.
>
> As peças descritas aqui moram no `core` (são infraestrutura sem regra de negócio).
> Implementação de referência: `app-modules/core/src/Support/Listing.php` e
> `app-modules/core/src/Admin/` do Fibro+.

## As regras 11 a 16 (somam-se às 10 regras de ouro)

11. **Toda lista é paginada, buscada e ordenada no servidor**, pelo `Listing` do core,
    com `meta.counts`. Nenhum endpoint devolve "tudo" para a tela filtrar.
12. **O detalhe devolve todas as colunas visíveis** do registro, com as datas de controle
    e o **nome** de cada vínculo. A tela mostra tudo; o recurso não pode omitir.
13. **A API nunca obriga a tela a mostrar um ID.** Todo lugar que menciona outro registro
    traz o rótulo legível junto.
14. **Vínculo recebe id de registro existente, ativo e do mesmo recorte**; qualquer outra
    coisa é 422 no campo. Nunca texto livre para ligar registros.
15. **Não existe apagar.** Cadastro se arquiva (flag de ativo); registro se exclui
    logicamente, em cascata, com prévia; tudo se restaura.
16. **O nível mais alto nunca é barrado por falta de tenant.** Quando o usuário não
    pertence a uma entidade, a borda descobre a entidade pelo alvo da ação.

## 1. `Listing` — o contrato único de lista

```php
// no módulo dono, dentro da Action de listagem
$data = $input->validate(Listing::rules(orderable: ['name', 'created_at']) + [
    'status'  => ['sometimes', Rule::in(['active', 'archived', 'all'])],
    'unit_id' => ['sometimes', 'uuid'],
]);

$query = Unit::query();                                   // o EntityScope já recorta o tenant
if ($text = Listing::searchText($data['q'] ?? null)) {    // minúsculas, sem acento
    $query->where('unt_name_search', 'like', "%{$text}%");
}

return Listing::paginate(
    $query, $data,
    orderable: ['name' => 'unt_name', 'created_at' => 'unt_created_at'],
    defaultOrder: ['unt_name', 'asc'],
    counts: ['active' => $active, 'archived' => $archived],
);
```

| Parâmetro | Regra |
| --- | --- |
| `page` | ≥ 1; além do fim devolve a última |
| `per_page` | padrão 20, máximo 100 |
| `q` | nome **sem diferenciar acento e maiúscula** (coluna auxiliar `*_name_search` preenchida ao salvar); documento com ou sem máscara (`Listing::digits`) |
| `order` | `campo` ou `-campo`, **só os da lista permitida**; inválido cai no padrão; desempate pela chave |
| filtros | `=` para vínculo e conjunto fechado (nunca `LIKE`); faixa para data e número |
| `deleted=1` | só para o nível mais alto (`Listing::onlyDeleted`); ignorado em silêncio para os demais |

Resposta: `{ data: [...], meta: { total, page, per_page, last_page, counts } }`.

`counts` é por status **dentro da busca e dos outros filtros, ignorando o filtro de
status**: alimenta a linha do tempo e as abas de status da tela.

Cada item traz o **nome** dos vínculos que a lista mostra (`unit_name`), com as relações
pré-carregadas (sem N+1). O total vem de `COUNT`, nunca de carregar a tabela.

## 2. Motor de cadastros (`Core\Admin`)

Cadastro simples não ganha controller próprio. O módulo dono declara uma `AdminResource`
e registra as rotas; o core serve o contrato inteiro com cinco Actions genéricas.

```php
final class UnitAdminResource extends AdminResource
{
    public function key(): string { return 'units'; }
    public function query(): Builder { return Unit::query(); }            // recorte de quem pergunta
    public function present(Model $record): array { /* TODAS as colunas visíveis + nomes dos vínculos */ }
    public function orderable(): array { return ['name' => 'unt_name', 'created_at' => 'unt_created_at']; }
    public function defaultOrder(): array { return ['unt_name', 'asc']; }
    public function activeColumn(): ?string { return 'unt_active'; }
    public function search(Builder $query, string $text, string $digits): void { /* ... */ }
    public function filterRules(): array { return ['entity_id' => ['sometimes', 'uuid']]; }
    public function applyFilters(Builder $query, array $data): void { /* ... */ }
    public function createRules(): ?array { /* null = não cria */ }
    public function updateRules(Model $record): array { /* imutável depois de usado → regra que recusa */ }
    public function update(Model $record, array $data): void { /* ... */ }
}

// no provider do módulo dono
AdminRoutes::register(UnitAdminResource::class, 'units.manage');
```

| Chamada | Comportamento |
| --- | --- |
| `GET /v1/staff/admin/{recurso}` | lista sempre paginada; `status=active|archived|all`; `meta.counts {active, archived}` |
| `GET …/{id}` | `data` com todas as colunas + `usage` (referências vivas, contadas no recorte de quem pergunta); arquivado também abre |
| `POST …` | 201 com o registro completo |
| `PATCH …/{id}` | parcial; campo imutável depois de usado → 422 **naquele campo**, em português |
| `POST …/{id}/archive`, `/restore` | idempotentes; **arquivar = flag `*_active`, nunca DELETE**; arquivar tira o registro das escolhas novas e mantém o que existe |

**`usage` sem furar fronteira**: cada módulo soma as próprias referências ao cadastro de
outro módulo, sem importar o model alheio:

```php
AdminUsage::contribute('units', 'patients', fn (string $unitId): int => Patient::where('units_unt_id', $unitId)->count());
```

Filho de um cadastro (item de um catálogo) é recurso próprio, listado com
`?<pai>_id=<id>` e criado com o id do pai no corpo.

Seeder de catálogo **só cria** o que não existe: nunca desfaz edição feita pelo painel.

## 3. Detalhe completo (regra 12)

`present()` (e todo `JsonResource` de detalhe) devolve:

- todas as colunas do registro, **menos** segredos e a data de exclusão;
- `created_at`, `updated_at`; quem criou/decidiu e quando, se a tabela guarda;
- o nome de cada vínculo (`entity_name`) ou `{ id, name }`;
- `usage`; contagens por relação quando baratas;
- quando a ação depende do estado, o que **este** usuário pode fazer **neste** registro
  (`can: { approve: true }`), para a tela não reimplementar regra.

Teste de contrato por recurso: as chaves do detalhe cobrem as colunas da tabela (lista
de exceções explícita no teste). Coluna nova sem ir para o `present()` quebra o teste.

## 4. Rótulos (regra 13)

- Um mapa central de **nome legível por tabela** (`DataExplorer::LABELS`): partes da
  própria linha ou `@vínculo` (o nome do pai), unidas por ` · `; datas `dd/mm/aaaa`;
  status em português; corte em 70 caracteres; sem dado, **"Registro sem nome"**. Nunca o id.
- A tela genérica de dados recebe `labels` (coluna de vínculo → id → nome) e `title`.
- A auditoria devolve `record_label` e `refs` (coluna de vínculo → id → nome) para o
  antes/depois.
- Palavras de status são **as mesmas** no back e no front. O mapa do back
  (`DataExplorer::STATUS`) e o do front são conferidos um contra o outro.

## 5. Vínculos (regra 14)

- `GET …/{tabela}/options?q=` → até 30 registros **ativos**, `{ value, label }`, busca por
  nome (pessoas também por documento). É o que alimenta o campo de relação da tela.
- Na escrita, a regra de validação confere: existe, está ativo, é do mesmo tenant.
  Fora disso → 422 no campo.
- A lista do filho aceita o filtro pelo pai (`?unit_id=`), com o **mesmo recorte e
  permissão** da lista normal: é a aba de relação do modal.

## 6. Ações de fluxo

Mudança de estado é endpoint próprio com verbo (`POST …/{id}/approve`,
`…/reject {reason}`), passa pela Action (que roda as invariantes e emite o evento) e
responde com o registro atualizado. `PATCH status` não existe no fluxo normal.

## 7. Erros (o que a tela sabe mostrar)

| Código | Quando | Corpo |
| --- | --- | --- |
| 422 | validação | `{ message, errors: { campo: [..] } }`, mensagens em pt-BR, chaves = nomes dos campos do contrato |
| 409 | o estado mudou; total da prévia mudou | `{ message }` |
| 403 | sem permissão | `{ message }` |
| 404 | não existe **ou** é de outro recorte (resposta igual, de propósito) | `{ message }` |
| 428 | falta pré-condição (motivo de acesso) | `{ message }` |
| 429 | limite de tentativas | `{ message }` + `Retry-After` |

Erro 500 nunca chega com rastro de pilha. Toda mensagem é escrita para a pessoa que usa.

## 8. Contrato publicado

`docs/api/openapi.yaml` é a fonte dos tipos do front (`api:types`). Mudou um campo: muda
o contrato na mesma entrega, e o relatório da feature avisa o front. Os nomes dos campos
do corpo e do `errors` são **os do contrato**; divergência silenciosa (a tela manda
`professional_name`, a API valida `doctor_name`) é o defeito mais caro que existe.

## 9. Lista de conferência de um endpoint de painel

- [ ] Lista pelo `Listing`; `counts`; nomes dos vínculos nos itens; sem N+1.
- [ ] Detalhe com todas as colunas, datas de controle, nomes, `usage`.
- [ ] Nenhum id sem rótulo ao lado.
- [ ] Vínculos validados (existe, ativo, mesmo tenant); `options?q=` disponível.
- [ ] Aba de relação possível (`?<pai>_id=`).
- [ ] Arquivar/restaurar idempotentes; nada de DELETE físico.
- [ ] 422 em pt-BR com as chaves do contrato.
- [ ] Funciona para o nível mais alto sem tenant.
- [ ] Teste de contrato do recurso; OpenAPI atualizado.
