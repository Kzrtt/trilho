---
name: guia-de-tela
description: Escreve ou revisa o tutorial do topo de uma tela complexa (a faixa de passos "Como funciona esta tela") — título, introdução, 3 a 6 passos com ícone, texto e a parte da tela que cada passo destaca. Use quando uma tela tiver fluxo ou regra de negócio que precisa ser explicada, quando o usuário pedir tutorial/ajuda/guia/onboarding de uma tela, ou quando uma regra de negócio mudar e o guia precisar acompanhar.
---

# Guia de tela

Leia `docs/padrao/07-GUIA-DE-TELA.md` inteiro antes.

## Passo 1 — Entender o fluxo de verdade

1. Leia a tela (ações, estados, permissões) e a regra de negócio na fonte (documento de
   domínio da API, se houver). **Números e prazos têm de ser os reais.**
2. Liste, na ordem em que a pessoa trabalha: o que ela procura, o que ela abre, o que ela
   decide, o que acontece depois de cada decisão (inclusive o que não se vê: e-mail
   enviado, etapa liberada, ação sem volta).

## Passo 2 — Escrever

- **Título**: o trabalho, em forma de "Como …" ou "O ciclo de …".
- **Introdução**: uma frase dizendo o que a tela mostra e qual é o trabalho ali.
- **3 a 6 passos.** Para cada um:
  - `title`: verbo no imperativo + objeto, **até quatro palavras**;
  - `text`: **uma a três frases** — o que fazer e o que acontece depois;
  - `icon`: um ícone da biblioteca do projeto que lembre a ação;
  - `target`: o `data-guia` da parte da tela (omita se o passo só explica uma consequência).
- Mesmas palavras dos botões e dos status. Sem jargão, sem "clique aqui", sem nome técnico.

## Passo 3 — Ligar

1. Ponha `data-guia="…"` nas partes da tela (no mínimo: filtros, linha do tempo, tabela).
2. Registre o guia no arquivo único de guias, com `id` estável (é a chave do "escondido").
3. Ponha a peça do guia entre o cabeçalho da tela e a lista.

## Passo 4 — Conferir

- Cada passo destaca a parte certa; o destaque rola até ela e some sozinho.
- "Entendi, esconder" some com o guia, "Como funciona esta tela" traz de volta, e a
  escolha sobrevive a recarregar.
- Teclado: setas andam entre os passos.
- 390px: os passos quebram de linha, sem rolagem lateral.
- Leia os textos em voz alta para alguém de fora: entendeu sem perguntar?

## Quando a regra muda

Mudou prazo, etapa ou consequência: o guia muda **na mesma entrega**. Guia desatualizado
ensina errado.
