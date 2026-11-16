# 02 — Casca (topo, menu, perfil)

A casca é a mesma em todas as telas do painel. Ela nunca é reescrita por tela.

```
┌─ TOPO  charcoal · 64px ─────────────────────────────────────────────────────┐
│ [logo]  Nome do sistema │ subtítulo                       ( Nome · nível ▾ ) │
├─ filete sand ──────────────────────────────────────────────────────────────┤
│ MENU 14rem      │ PALCO (cartão creme sobre fundo sand)                     │
```

## 1. Topo

- Fundo `--adm-topo-fundo` (charcoal), borda inferior no sand, 64px, conteúdo alinhado
  com o palco.
- Esquerda: logo (versão para fundo escuro, ~40px). Ao lado, separados por filete
  vertical, o nome do sistema (15px/650) e um subtítulo (12px, `topo-apagado`): o nome da
  entidade/cliente em uso.
- Direita: a **pílula do perfil**.
- Realce permitido: uma linha fina de 2px na cor `marca` → `realce` percorrendo a borda,
  e um brilho radial muito suave atrás do logo. Nunca `overflow: hidden` no topo (corta o
  menu do perfil). O topo cria contexto de empilhamento: dê a ele `z-index` (40) para o
  dropdown passar por cima do palco.
- Abaixo de 900px: some o subtítulo, aparece o botão do menu (hambúrguer) à esquerda.

## 2. Perfil

Pílula-botão (`aria-haspopup="menu"`, `aria-expanded`): círculo com ícone/iniciais + nome
(corta com reticências; nome inteiro no `title`) + badge do nível + seta que gira ao abrir.

Painel que abre (largura mín. 240px, `sombra-alta`, raio 10px):

1. cabeçalho: nome, login, nível (badge), entidade;
2. "Trocar senha";
3. "Sair", no estilo **perigo discreto**, com confirmação.

Fecha com clique fora, Esc (devolvendo o foco) e ao navegar. Setas ↑/↓ percorrem os itens.

## 3. Menu lateral

**Uma definição só** (arquivo de menu), usada pela lateral e pela gaveta do celular. Cada
item declara quem pode abri-lo (nível ou permissão). Seção sem item permitido **não é
desenhada**.

Comportamento: **acordeão de seção única**. A seção da página atual abre no carregamento;
abrir outra fecha a anterior.

```
┌───────────────────────────────┐
│ (●) Cadastros             ⌄  │  cabeçalho da seção: charcoal, ícone num círculo
├───────────────────────────────┤
│ │  Unidades                   │  itens: fundo claro, linha vertical ligando
│ ●  Pessoas          ← atual   │  item atual: fundo marca-50, texto marca, ponto pulsante realce
│ │  Médicos                    │
└───────────────────────────────┘
```

| Parte | Estilo |
| --- | --- |
| Cabeçalho de seção | fundo `menu-secao`, raio 8px, 13,5px/600, `menu-texto`; ícone 15px num círculo (branco a 8% → `realce` no hover → `marca` quando aberta); seta 10px que gira 180° |
| Seção aberta | cabeçalho com cantos de cima arredondados; lista em `neutro-0` com borda; fecha com faixa de 6px na cor do cabeçalho |
| Item | 13px, padding 6px 9px, raio 5px, ligado por uma linha vertical de 1px; hover desloca 2px |
| Item atual | fundo `marca-50`, texto `marca-300` em 600, ponto de 10px na cor `realce` sobre a linha, pulsando |
| Contador (pendências) | pílula pequena na cor `realce` ao lado do rótulo |
| **Sem sombra** | nos cabeçalhos e nos itens |

Regras de conteúdo:

- Seções são poucas e nomeadas pelo trabalho: Início, Operação/Acompanhamento,
  Cadastros (quem e onde), Catálogos (o que o sistema oferece), Gestão (usuários,
  auditoria, configurações).
- Um item por **tela**. Preset de uma tela (ex.: "Alertas" = Respostas com filtro) é um
  item com parâmetros, não uma tela nova.
- Tabela que já se edita numa aba de um pai não entra no menu.
- O menu não pode rolar em 1366×768 para o nível mais comum. Passou disso? Reagrupe.

## 4. Gaveta (abaixo de 900px)

O mesmo menu dentro de uma gaveta que **abre pela esquerda** (`translateX(-100%)` → 0),
com fundo escurecido, fecha no fundo, no Esc e ao escolher um item.

## 5. Palco

`<main>` em cartão `neutro-0`, borda `card-borda`, raio 10px, padding 20px (12px no
celular). O fundo da página pode ter um ornamento contínuo e muito discreto da marca
(padrão repetido com opacidade de 4% a 11%, onda no rodapé); nunca peças isoladas nos
cantos, e sempre escondido na impressão.

## 6. Cabeçalho da tela

- `h1` 22px/650 com o nome da área no plural ("Unidades").
- Uma linha de descrição, 13px `texto-apagado`: o que se faz ali.
- À direita, o **único botão primário** da tela ("Nova unidade"), só para quem pode criar.
- Sob o título, um traço curto `marca` → `realce` que se desenha ao abrir a tela. É um
  acento embaixo, não uma faixa lateral.
- Sem ícone decorativo no `h1`.

## 7. Impressão

`@media print`: somem topo, menu, botões, abas, barras e guia; aparece um cabeçalho de
impressão com nome do sistema, entidade, data e quem imprimiu.
