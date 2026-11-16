---
name: novo-cadastro
description: Cria a tela de um cadastro simples (lista + modal de detalhe + formulário) como configuração declarativa do motor, com todas as colunas no detalhe, todas as editáveis no formulário e uma aba por relação. Use quando o usuário pedir uma tela para uma tabela/entidade cujo trabalho principal é criar, ver, editar e arquivar registros.
---

# Novo cadastro

O resultado é **um arquivo de configuração + uma linha no registro**. Menu, rotas e
guarda de acesso saem sozinhos. Se a tela precisa de mais do que criar/ver/editar/arquivar,
use `/nova-tela`.

## Fase 0 — Contexto

1. Leia `docs/padrao/08-CADASTROS-DECLARATIVOS.md`, `04-MODAL-DE-DETALHE.md`, `05-FORMULARIO.md`, `06-VOCABULARIO-VISUAL.md`.
2. Abra um cadastro existente parecido e use-o de molde.
3. Descubra o contrato real:
   - a tabela no back (migration/model): **todas as colunas**, tipos, obrigatoriedade, vínculos;
   - quem aponta para esta tabela (as futuras abas de relação);
   - o que `GET /` e `GET /{id}` devolvem de verdade (chame a API; não suponha);
   - as regras do `POST`/`PATCH` (nomes exatos dos campos).
4. Monte a tabela de conferência e guarde-a para o relato:

   | Coluna do banco | Vem na lista? | Vem no detalhe? | Seção do modal | Editável? | Controle |
   | --- | --- | --- | --- | --- | --- |

   Coluna que a API não devolve e deveria: **peça ao back** (formato em `13-CONTRATO-COM-A-API.md`, §12)
   e siga com o resto. Não esconda a falta.

## Fase 1 — Configuração

- `label` com singular, plural e gênero; `icon` único para este tipo de registro;
  `description` de uma linha; `permissions` de leitura e escrita.
- **Lista**: coluna principal + segunda linha; 4 a 6 colunas; status com `badge`; vínculo
  com `chip: 'ref'` e o **nome**; código com `chip: 'code'`; `sort` nos campos que a API ordena;
  filtros; textos de busca e de vazio.
- **Detalhe**: `title`, `subtitle`, `meta`; **todas as colunas** distribuídas em seções por
  tema; a seção "Registro" no fim. Nenhuma seção genérica.
- **Formulário**: os mesmos grupos do detalhe; **todas as colunas editáveis**; vínculo como
  `relation`; conjunto fechado como `select` com as palavras do mapa central; `locked` com
  o motivo para o que não muda depois de usado; `only`/`when` para o que é condicional;
  linhas somando 12.
- **`related`**: uma aba para cada tabela que aponta para esta, com `open` levando ao modal
  do relacionado e `permissions` da lista relacionada.
- **`children`**: listas que só existem dentro deste registro.
- **`usage`**: singular e plural de cada referência, para o aviso de arquivar.

## Fase 2 — Vocabulário

- Rótulo da tabela e de cada coluna no mapa central de rótulos.
- Cada valor de status/tipo novo no mapa central de badges (procure o valor antes: reaproveite a palavra que já existe).
- Regra nova de rótulo → jeito de mostrar, no "olhar do detalhe".

## Fase 3 — Teste e conferência

1. Teste do cadastro: lista, abre o modal, mostra os campos, cria, edita (envia só o que mudou), 422 cai no campo, arquiva com o aviso.
2. Verificação de tipos `&&` testes `&&` build de produção.
3. Capturas 1440 e 390: lista, modal (cada aba), formulário. **Olhe.**
4. Varredura de ID e de texto cru nesta tela (`docs/padrao/15-VERIFICACAO.md`).

## Relato

A tabela de conferência preenchida, o que foi pedido ao back, as capturas, e o que ficou de fora.
