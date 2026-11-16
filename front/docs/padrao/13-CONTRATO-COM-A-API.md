# 13 — Contrato com a API

O padrão visual só fecha se a API devolver o que a tela precisa. Este é o contrato que o
front **espera** e que o back **entrega** (o lado do back está em
`docs/arquitetura/PAINEL.md` do repositório da API).

Regra de trabalho: faltou um dado para cumprir uma lei do painel? **Peça ao back.** Não
contorne com uma segunda chamada por linha, com o ID na tela ou com um bloco genérico.

## 1. Envelope

```jsonc
// sucesso
{ "data": { ... } }                       // um registro
{ "data": [ ... ], "meta": { ... } }      // lista

// erro
{ "message": "Texto em português para a pessoa.", "errors": { "campo": ["mensagem"] } }
```

| Código | Significado para a tela |
| --- | --- |
| 200/201 | ok |
| 202 | aceito, processando: mostrar andamento |
| 401 | sessão acabou: ir ao login e voltar |
| 403 | sem permissão |
| 404 | não existe **ou** é de outro recorte (a resposta é igual de propósito) |
| 409 | o estado mudou: recarregar |
| 422 | validação: `errors` por campo |
| 428 | falta uma pré-condição (ex.: motivo de acesso): pedir e repetir |
| 429 | muitas tentativas: mostrar a espera |

## 2. Login

`POST /auth/login` devolve o token e o usuário com tudo que a casca precisa:

```jsonc
{ "data": { "token": "...", "user": {
    "id": "...", "name": "...", "login": "...",
    "role": "manager", "role_label": "Gestor",
    "permissions": ["units.manage", "audit.view"],
    "entity": { "id": "...", "name": "..." },
    "units": [{ "id": "...", "name": "..." }],
    "must_change_password": false } } }
```

## 3. Lista

`GET /recurso?page=&per_page=&q=&order=&status=&<filtro>=`

- `per_page` padrão 20, máximo 100.
- `q`: nome sem diferenciar acento/maiúscula; documento com ou sem máscara.
- `order`: `campo` ou `-campo`, só campos permitidos (inválido = padrão).
- Página além do fim devolve a última.

```jsonc
{ "data": [ ... ],
  "meta": { "total": 240, "page": 2, "per_page": 20, "last_page": 12,
            "counts": { "pending": 12, "approved": 200, "rejected": 28 } } }
```

`counts` é por status **dentro da busca e dos outros filtros, ignorando o filtro de
status**: é o que alimenta a linha do tempo e as abas de status.

Cada item da lista já traz **os nomes** dos vínculos mostrados nas colunas
(`unit_name`, `entity_name`), nunca só o id. Sem consulta por linha.

## 4. Detalhe

`GET /recurso/{id}` devolve **todas as colunas** que podem ser vistas, além de:

- o nome de cada vínculo (`*_name`) ou o objeto resumido `{ id, name }`;
- datas de controle (`created_at`, `updated_at`) e quem criou/decidiu, quando houver;
- `usage`: referências vivas por tipo (`{ "users": 12, "patients": 240 }`);
- contagem por relação para as abas, quando barato (`counts: { users: 12 }`);
- o que a pessoa pode fazer neste registro, quando depende do estado
  (`can: { approve: true, edit: false }`), para a tela não reimplementar regra.

Segredos nunca saem. Documento pessoal sai mascarado para quem não pode ver inteiro.

## 5. Relação (aba)

A lista do recurso relacionado aceita o filtro pelo pai: `GET /users?unit_id=<id>`,
paginada, com o **mesmo recorte e permissão** da lista normal.

Vincular/desvincular: `POST /recurso/{id}/<relação> { <campo>_id }` e
`DELETE /recurso/{id}/<relação>/{linkId}`.

## 6. Opções para campo de relação

`GET /recurso/options?q=` → até 30 registros **ativos**, `{ value, label }`, busca por
nome (e documento, quando for pessoa). O `label` é o rótulo legível do registro.

Valor inválido num vínculo (inexistente, de outra entidade, inativo) → 422 no campo.

## 7. Escrita

- `POST /recurso` → 201 `{ data }` (o registro completo, para a tela não buscar de novo).
- `PATCH /recurso/{id}` com **só o que mudou** → 200 `{ data }`.
- Campo imutável depois de usado → 422 **naquele campo**, com a explicação.
- `POST /recurso/{id}/archive` e `/restore` → idempotentes.
- Ações de fluxo são endpoints próprios com verbo (`/approve`, `/reject { reason }`),
  nunca `PATCH status`.
- Operação repetível por engano (clique duplo, reenvio) é idempotente por uma `ref` do cliente.

## 8. Rótulos (nunca ID)

Todo lugar em que a API menciona outro registro traz o **rótulo** junto:

| Onde | Campo |
| --- | --- |
| item de lista/detalhe | `<vínculo>_name` ou `{ id, name }` |
| tela genérica de dados | `labels` (coluna de vínculo → id → nome), `title` (o rótulo do próprio registro) |
| auditoria | `record_label` (o registro) e `refs` (coluna de vínculo → id → nome) para o antes/depois |

Registro sem nome próprio recebe do servidor um rótulo composto ("Dra. Ana · UBS Centro").

## 9. Exclusão em cascata (Admin)

```
GET    /admin/data/{table}/{id}/delete-preview        → { deletes: [{table,label,count}], kept: [...], total }
DELETE /admin/data/{table}/{id}  { confirm: true, expected_total }   → 409 se o total mudou
POST   /admin/data/{table}/{id}/restore  { expected_total }
```

Listas aceitam `deleted=1` (só para o Admin; ignorado em silêncio para os demais).

## 10. Auditoria

`GET /audit?action=&table=&from=&to=&user_id=&q=` (paginada) → itens com `when`, `actor`
(nome e login), `action`, `table`, `table_label`, `record_label`, `before`, `after`, `refs`.

`GET /recurso/{id}/activity` → a mesma trilha, daquele registro (aba "Atividade").

## 11. Tipos

O front não escreve os tipos da API à mão quando o back publica o contrato (OpenAPI):
gere-os (`api:types`). Sem contrato publicado, os tipos ficam num arquivo só, **com as
chaves exatas da API**: já houve formulário enviando `professional_name` para uma API
que validava `doctor_name`, e o campo foi ignorado em silêncio por meses.

## 12. Como pedir algo ao back

Escreva o pedido com: a tela, a lei do painel que depende disso, o endpoint, o campo e o
formato esperado. Exemplo:

> Modal de Unidade (lei 2, todos os campos). `GET /staff/admin/units/{id}` não devolve
> `created_at`, `updated_at` nem `entity_name`. Preciso dos três em `data`.
