---
name: novo-recurso-admin
description: Expõe uma tabela ao painel no contrato único de cadastro (lista paginada com counts, detalhe com todas as colunas e usage, criar, editar parcial, arquivar/restaurar), declarando uma AdminResource no módulo dono, com teste de contrato e aviso ao front. Use quando o usuário pedir um cadastro/CRUD para o painel, um endpoint de listagem para uma tela, ou quando o front pedir um campo, um filtro, uma aba de relação ou um rótulo que a API ainda não devolve.
---

# Novo recurso do painel

Leia antes: `docs/arquitetura/PAINEL.md` (o contrato), `DADOS.md` e `CONTAS_E_AUDITORIA.md`.
Molde: um `*AdminResource` que já exista no projeto.

## Fase 0 — Contexto

1. `/dominio` para a área tocada. Regra de negócio ambígua (quem pode, o que é imutável
   depois de usado, o que arquivar provoca): **pergunte antes**.
2. Liste as colunas da tabela e os vínculos (para quem aponta; quem aponta para ela).
3. Decida, e registre no relatório: permissão de leitura/escrita; recorte por nível;
   campos imutáveis depois de usados; se cria; se arquiva; filtros; campos de ordenação.

## Fase 1 — Implementar no módulo dono

1. **Coluna de ativo** (`<prefixo>_active`) se o cadastro arquiva; **coluna de busca sem
   acento** (`<prefixo>_name_search`, preenchida no `saving`) se há busca por nome.
2. **`<Nome>AdminResource extends AdminResource`**:
   - `query()` com o recorte de quem pergunta;
   - `present()` com **todas as colunas visíveis**, as datas de controle e o **nome de
     cada vínculo** (nunca só o id); segredos fora;
   - `orderable()`, `defaultOrder()`, `search()`, `filterRules()` + `applyFilters()`
     (vínculo com `=`; inclua o filtro pelo pai, para a aba de relação);
   - `createRules()` / `updateRules()` em pt-BR, com vínculo validado (existe, ativo,
     mesmo tenant) e imutável-depois-de-usado respondendo 422 no campo;
   - `create()` / `update()`; `activeColumn()`.
3. **Rotas**: `AdminRoutes::register(<Nome>AdminResource::class, '<permissão>')` no provider.
4. **`usage`**: cada módulo que referencia este cadastro contribui com a sua contagem
   (`AdminUsage::contribute`), sem importar o model alheio.
5. **Efeito de arquivar** nos fluxos: o arquivado sai das escolhas novas (selects,
   validação de vínculo); o que já existe continua.
6. **Rótulos**: entrada no mapa de nome legível; palavras de status no mapa de status.
7. **Opções**: o registro aparece em `options?q=` (ativos, até 30, por nome).

## Fase 2 — Testes (junto com o código)

Teste de contrato do recurso, no mínimo:

- lista: `meta` completo, `counts`, `status`, busca sem acento, ordem, página além do fim;
- recorte: cada nível vê só o seu; outro tenant → 404; sem permissão → 403;
- detalhe: **as chaves cobrem as colunas da tabela** (exceções explícitas), `usage` contado no recorte;
- criar/editar: 422 em pt-BR nos campos; vínculo inválido/inativo/de outro tenant → 422;
  imutável depois de usado → 422 naquele campo; `PATCH` parcial;
- arquivar/restaurar idempotentes, com efeito no select e na validação;
- nível mais alto sem tenant consegue tudo;
- mutação auditada com conta e operador.

`composer lint && composer lint:check && composer test` verdes.

## Fase 3 — Contrato e aviso ao front

1. Atualize `docs/api/openapi.yaml`.
2. No relatório da feature, uma seção **"Para o front"**: caminho do recurso, permissões,
   campos da lista e do detalhe (com tipo e rótulo sugerido), filtros, campos de
   ordenação, regras do formulário (obrigatório, tamanho, imutável), relações que viram
   aba (`?<pai>_id=`), palavras de status. É o que a skill `/novo-cadastro` do front lê.

## Quando o front pede algo

Pedido típico: "o modal de X precisa de `created_at` e do nome da entidade". Atenda no
`present()`, acrescente ao teste de contrato e ao OpenAPI. Não responda "use o id":
a regra 13 proíbe a tela de mostrar id.

## Quando NÃO é um recurso do motor

Fluxo com estado (aprovar, emitir, encerrar) ganha Actions e rotas próprias com verbo;
a lista ainda usa o `Listing` e o detalhe ainda devolve tudo.
