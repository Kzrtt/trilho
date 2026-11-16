# 14 — Peças por framework

O kit de componentes do painel. Os nomes são os mesmos nas duas implementações de
referência: **Fibro+** (Angular 21, sinais, Vitest) e **Urban Pass** (React 19, Vite,
TanStack Query, react-hook-form + zod). Em outro framework, **mantenha os nomes**.

Regra (lei 19): tela nova se monta com estas peças. Faltou uma? Ela nasce **no kit**, com
teste, e não dentro da tela.

## 1. O kit

| Peça | Papel | Doc |
| --- | --- | --- |
| `AdmPageHeader` | título, descrição, botão primário, traço de realce | 02 |
| `AdmMenu` | menu lateral em acordeão (e o conteúdo da gaveta) | 02 |
| `AdmProfileMenu` | pílula do perfil e o painel dela | 02 |
| `AdmButton` | variantes: primary, secondary, neutral, danger-soft, danger, success | 06 |
| `AdmBadge` (+ `AdmRoleBadge`) | estado: `state` + ícone + texto | 06 |
| `AdmChip` | coisa: `ref` (com ícone) ou `code` | 06 |
| `AdmAlert` | faixa info/alerta/erro/sucesso | 10 |
| `AdmEmpty` | bloco de vazio com frase e ação | 10 |
| `AdmToolbar` | barra da lista (esquerda/direita) | 03 |
| `AdmSearch` | busca ao vivo + botão de filtros | 03 |
| `AdmListFilters` / `AdmFilterModal` | modal de filtros | 03 |
| `AdmDeletedToggle` | "Ver excluídos" (Admin) | 09 |
| `AdmTable` (+ `AdmRow`, `AdmCell`) | tabela em cartão; vira cartões no celular; célula pelo vocabulário visual | 03 |
| `AdmPaginator` | "Mostrar", "x-y de n", janela de páginas | 03 |
| `Timeline` | etapas com contagem; clicável como filtro | 03, 07 |
| `AdmDetailModal` | a caixa: ficha, ações, abas, corpo | 04 |
| `AdmDetailSection` / `AdmDetailField` / `AdmValue` | seção de leitura e campo desenhado pelo vocabulário | 04 |
| `AdmTabs` | abas que quebram de linha | 04 |
| `AdmRelatedTable` | aba de relação: lista filtrada pelo registro aberto | 04 |
| `AdmChildTable` | aba de lista-filha, editada no lugar | 04 |
| `AdmDataActions` | Editar dados · Excluir · Restaurar (Admin) | 09 |
| `AdmImpersonateButton` | "Entrar como" | 09 |
| `AdmFormCard` | cartão de grupo do formulário | 05 |
| `AdmField` | rótulo + controle + ajuda + erro | 05 |
| `AdmFormFields` | desenha um grupo a partir da configuração | 05, 08 |
| `AdmRelationSelect` / `AdmCombobox` | campo de relação com busca no servidor | 05 |
| `AdmMultiSelect` / `AdmMultiCheck` | escolha múltipla | 05 |
| `AdmListField`, `AdmRowsField` | lista de textos, lista de objetos | 05 |
| `FormDialog` | diálogo de formulário curto | 05 |
| `TempPasswordDialog` | mostra a senha provisória uma vez | 09 |
| `AdmScreenGuide` / `ScreenGuide` | o guia de tela | 07 |
| `FeedbackService` / `feedback` | confirm, success, error | 10 |
| `CountUp` | número que conta ao entrar na tela | 12 |

## 2. Lógica (sem interface)

| Peça | Papel |
| --- | --- |
| `ListController` / `useListParams` | estado da lista ↔ URL ↔ parâmetros da API |
| `DetailController` | registro aberto ↔ `?ver=`; carrega o detalhe; devolve o foco |
| `LocalDetail` | o mesmo, para tabela dentro de aba (sem URL) |
| `ModalTabs` | aba ativa ↔ `?aba=`; volta a "dados" ao trocar de registro |
| `defineResource` + registro | o motor de cadastros (08) |
| `AdmForm` | monta o formulário da configuração; corpo só com o que mudou; 422 → campo |
| `unsavedChangesGuard` | pergunta ao sair com alteração |
| `detailLook` / `lookFor` | decide badge/chip/data/citação pelo rótulo (06) |
| `badge-maps`, `*-status` | os mapas centrais de vocabulário |
| `labels`, `tableLabels`, `columnLabels` | rótulos em português de tabelas e colunas |
| `menu` | a definição única do menu |
| `access` (`canOpenRoute`, `can`) | quem abre o quê e quem faz o quê |
| `session` | token + usuário (com `permissions[]`) |

## 3. Onde cada coisa mora

### Angular (referência: Fibro+)

```
src/styles/admin-tokens.css          tokens .adm
src/styles/admin-controls.css        controles compactos + grade de 12
src/app/shared/admin/                o kit (adm-*.ts/html/css)
src/app/shared/timeline/             linha do tempo
src/app/core/list/                   list-controller, detail-controller, local-detail, modal-tabs
src/app/core/admin/                  adm-resource (tipos), adm-form, adm-resource.service,
                                     unsaved-changes.guard, related, resources/*.config.ts + index.ts
src/app/core/<projeto>/              menu, access, badge-maps, labels, status, modelos e serviços da API
src/app/core/auth/                   session, guards, interceptor
src/app/layouts/app-layout/          a casca
src/app/pages/staff/admin/           páginas genéricas do motor (lista, formulário, lista-filha, rotas)
src/app/pages/staff/<área>/          telas à mão
```

Convenções: componentes standalone, `input()`/`output()`, sinais e `computed()`,
`inject()`, controle de fluxo nativo (`@if`, `@for` com `track`), sem `ngClass`/`ngStyle`,
estilo do painel em componentes compartilhados via `:host-context(.adm)`, renderização
só no cliente para a área autenticada.

### React (referência: Urban Pass)

```
src/styles/tokens.css                tokens .adm
src/styles/adm-shell.css             casca
src/styles/adm-components.css        peças
src/styles/adm-controls.css          controles + grade de 12
src/styles/adm-parts.css             partes do modal e da leitura
src/components/adm/                  o kit (Adm*.tsx)
src/components/guide/                ScreenGuide + guideStore
src/components/feedback.tsx          confirm/success/error
src/components/FormDialog.tsx        diálogo de formulário
src/lib/                             useListParams, labels, tableLabels, roles, format
src/api/                             client (openapi-fetch), schema.d.ts gerado, um arquivo por recurso
src/features/admin/AdminLayout.tsx   a casca
src/features/admin/menu.ts           a definição do menu
src/features/admin/resources/        types, registry, ResourceList, ResourceModal, configs/
src/features/admin/guides/guides.ts  todos os textos dos guias
src/features/admin/<área>/           telas à mão
```

Convenções: componentes de função, estado de servidor no TanStack Query (chave = recurso
+ parâmetros da lista), formulários com react-hook-form + zod, rotas com react-router,
tipos da API gerados do OpenAPI, CSS simples com os tokens (sem biblioteca de componentes).

## 4. Em outro framework (Vue, Svelte, Solid...)

1. Copie a folha de tokens ([`01`](01-TOKENS.md)) e as folhas de CSS de uma das referências:
   o CSS é quase todo independente de framework.
2. Recrie as peças da tabela 1 **com os mesmos nomes e as mesmas propriedades**.
3. Recrie as peças de lógica da tabela 2; `ListController`, `lookFor` e os mapas são
   funções puras e portam sem mudança.
4. O motor de cadastros é um tipo (`AdmResource`) + três páginas genéricas.
5. Rode a verificação ([`15`](15-VERIFICACAO.md)) contra a referência, lado a lado.

## 5. O que nunca entra

- Biblioteca de componentes pronta com tema próprio (Material, Ant, Bootstrap): o CSS
  colide e o resultado deixa de parecer o padrão.
- Segunda biblioteca de ícones.
- Tabela/grade de terceiros com paginação no cliente.
- CSS utilitário com valores soltos no lugar dos tokens.
