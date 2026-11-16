# 07 — Guia de tela (o tutorial do topo)

Tela com regra de negócio (fila de aprovação, emissão, quadro de etapas, importação)
abre com uma **faixa de passos** que ensina o fluxo. Quem usa o sistema não é de
tecnologia; a tela precisa se explicar.

## 1. Quando a tela ganha guia

Ganha, se **qualquer** uma for verdade:

- a tela tem mais de uma ação que muda o estado do registro;
- existe uma ordem certa de fazer as coisas;
- uma ação tem consequência que não se vê na hora (dispara e-mail, libera outra etapa,
  não tem volta);
- um colega novo precisaria de alguém ao lado na primeira vez.

Não ganha: cadastro simples (lista + detalhe + formulário).

## 2. Anatomia

```
┌ Como aprovar um credenciamento ───────────────────────── [✕ Entendi, esconder] ┐
│ A fila mostra os pedidos na ordem de chegada. O trabalho aqui é decidir cada um.│
│                                                                                 │
│  (🔍)¹          (👁)²           (✓)³            (🖨)⁴                            │
│  Filtre a fila  Abra o pedido   Decida          Emita o documento               │
│                                                                                 │
│  Abra o pedido. Clique numa linha para ver os documentos enviados e os dados    │
│  da pessoa. A parte da tela correspondente ficou destacada.                     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

- Fica **entre o cabeçalho da tela e a lista**.
- **Título** (o trabalho, em forma de "como…") e **uma frase** de introdução.
- **3 a 6 passos.** Cada passo: bolha com ícone, número, título de **até quatro palavras**.
- Clicar num passo abre o texto dele (**uma a três frases**: o que acontece ali e o que
  fazer) e **rola até a parte da tela correspondente, que fica destacada** por ~2,5s.
  Clicar de novo fecha.
- **"Entendi, esconder"** recolhe o guia. A escolha é lembrada **por tela** (no
  navegador). No lugar fica o botão discreto **"Como funciona esta tela"**, que o traz de volta.
- Teclado: setas ←/→, Home e End andam entre os passos; a região do texto é `aria-live`.
- No celular os passos **quebram de linha** (nunca rolam de lado).
- Não aparece na impressão.

## 3. Ligando o passo à tela

A parte da tela ganha um marcador; o passo aponta para ele:

```html
<div data-guia="filtros"> ...busca e filtros... </div>
<div data-guia="tabela">  ...tabela...          </div>
```

```ts
interface GuideStep { id: string; icon: Icon; title: string; text: string; target?: string }
interface Guide     { id: string; title?: string; intro?: string; steps: GuideStep[] }

const guide: Guide = {
  id: 'fila',                                   // chave para lembrar "escondido"
  title: 'Como fazer a triagem',
  intro: 'A fila mostra as ocorrências da mais prioritária para a menos. O trabalho aqui é decidir o destino de cada uma.',
  steps: [
    { id: 'filtrar', icon: Search, title: 'Filtre a fila',
      text: 'Use a busca, o tipo e os grupos de estado para chegar ao que importa. Os filtros ficam no endereço da página, então você pode mandar o link a um colega.',
      target: 'filtros' },
    { id: 'abrir', icon: Eye, title: 'Abra a ocorrência',
      text: 'Clique numa linha para ver os relatos, as fotos e por que ela tem aquela faixa.',
      target: 'tabela' },
    { id: 'decidir', icon: Hand, title: 'Qualifique ou encerre',
      text: 'Qualificar confirma o problema e libera a ocorrência para uma ordem de serviço. Rejeitar (com motivo) encerra sem obra.' },
  ],
};
```

Passo sem `target` só explica (uma consequência que acontece em outro lugar).

Marque sempre, no mínimo: a barra de busca/filtros, a linha do tempo de status e a tabela.

## 4. Como escrever

- **Título do passo = verbo no imperativo + objeto**: "Filtre a fila", "Decida", "Emita o documento".
- **Texto do passo** diz o que a pessoa faz e **o que acontece depois**. As consequências
  são o que mais importa: "Só um pedido aprovado pode virar carteirinha." "Rejeitar pede
  um motivo, que a pessoa recebe por e-mail."
- Use as **mesmas palavras** dos botões e dos status da tela.
- Sem jargão, sem nome de tabela, sem "clique aqui". Frase curta.
- Números e prazos citados (30 minutos, 5 tentativas) têm de bater com a regra real.
- Os textos dos guias moram num **arquivo só** (ou num documento de produto, com teste que
  confere a forma). Mudou a regra de negócio: muda o guia na mesma entrega.

## 5. O guia serve também como documentação de produto

A lista de guias é o resumo de como o sistema é operado. Mantenha-a legível de ponta a
ponta: alguém que leia só os guias deve entender o fluxo principal do produto.

## 6. Parentes do guia

| Peça | Para quê |
| --- | --- |
| **Linha do tempo de status** | as etapas de um registro, com contagem; clicável como filtro. Também usada parada, só para explicar uma hierarquia (níveis de acesso) |
| **Aviso permanente** | faixa `info` fixa numa tela de leitura ("Visão da equipe: só leitura") |
| **Aviso do formulário** | alerta no topo dizendo o efeito de mudar aquilo ("Mudar o nome muda o que o usuário final vê") |
| **Texto de vazio** | explica a área quando ainda não há registros |
