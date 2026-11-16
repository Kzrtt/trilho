# 00 — Princípios

## A ideia em uma frase

O dono do produto descreve **o que** o sistema faz; o padrão decide **como a tela sai**.
Dois sistemas de áreas diferentes, feitos com este kit, devem parecer irmãos: a mesma
casca, a mesma lista, o mesmo modal, as mesmas palavras de estado.

## Para quem é a interface

Equipes de trabalho que não são de tecnologia (servidor público, secretaria, atendimento).
Isso decide quase tudo:

- frase curta e direta, sem jargão nem palavra em inglês;
- um caminho óbvio por tela (um botão primário);
- nada escondido atrás de gesto (arrastar, duplo clique, menu de contexto) sem alternativa visível;
- o sistema explica a si mesmo (guia de tela, textos de vazio, motivo de botão desabilitado).

## O fluxo que organiza tudo

```
┌─ TOPO (logo · nome do sistema · [perfil]) ──────────────────────────────────┐
├─ MENU ─────────┬─ PALCO ─────────────────────────────────────────────────────┤
│ ▸ Seção        │  Título da área + descrição                    [+ Novo]     │
│ ▾ Seção aberta │  (guia de tela, quando a área é complexa)                   │
│   · item       │  Busca [..........] 🔍 filtros      [Atualizar] [excluídos] │
│   · item atual │  ┌ TABELA ───────────────────────────────────────────────┐  │
│                │  │ Principal (2 linhas)   Vínculo(chip)  Status(badge) ⟩ │  │
│                │  └───────────────────────────────────────────────────────┘  │
│                │  Mostrar [20▾]                  1-20 de 240  ‹ 1 2 3 … 12 › │
└────────────────┴─────────────────────────────────────────────────────────────┘

Linha ⟩ ──► MODAL DE DETALHE
            ficha (ícone · tipo · badges · título · resumo)        [Excluir][Editar]
            faixa de ações (todas neutras)
            abas: Dados | Relação A (12) | Relação B (3) | Atividade
            corpo: seções de leitura, todos os campos
                └─ Editar ──► formulário (cartões por grupo) ──► salva e volta ao modal
                └─ linha de uma aba ──► modal do registro relacionado
```

1. A pessoa abre uma área pelo menu e cai na **lista**.
2. Busca, filtra, ordena, pagina. Tudo isso vai para a URL.
3. Clica na linha: abre o **modal** com resumo, ações e **todos** os dados.
4. Do modal ela edita, arquiva, executa as ações do registro ou visita um registro
   relacionado por uma aba.
5. Fechou o modal: está na mesma página da lista, com a linha marcada como "última vista".

## O que cada papel de coisa faz

| Coisa | Papel | Nunca |
| --- | --- | --- |
| Menu | levar a uma área | listar tabela-filha, ter dois níveis de sublista |
| Lista | achar e reconhecer um registro | editar, mostrar tudo |
| Modal | ver tudo e agir | virar página, ter rodapé |
| Aba | registros ligados a este | repetir o que já está em "Dados" |
| Formulário | criar e mudar | misturar leitura longa |
| Guia de tela | ensinar o fluxo | repetir rótulo de botão |
| Painel inicial | dizer o que pede atenção agora | ser enfeite de gráficos |

## Dez decisões que já foram tomadas (não reabra)

1. **Sóbrio.** Charcoal e sand como base; cor só onde informa.
2. **Sem edição inline** em tabela. Exceção única: listas-filhas dentro do modal editam
   no próprio lugar (um segundo modal ficaria atrás do primeiro).
3. **Sem rodapé no modal**: fecha no X, no fundo e no Esc; sobra altura para o conteúdo.
4. **Foco neutro**, nunca na cor da marca.
5. **Alerta é âmbar**, nunca amarelo.
6. **Uma biblioteca de ícones**, traço único (Lucide por padrão).
7. **Um mapa central** de palavras e cores de estado; nenhuma tela inventa o seu.
8. **Arquivar no lugar de apagar**, com aviso do que está em uso.
9. **O servidor manda**: o front valida o óbvio (obrigatório, tamanho) e mostra o resto
   como erro do campo.
10. **Admin enxerga o que os outros não veem**: excluídos, tabelas sem tela, "entrar
    como". Sempre dentro das telas normais, nunca numa área paralela.

## Anti-padrões (já deram errado)

| Tentação | Por que não |
| --- | --- |
| Seção "Todos os campos" no fim do modal | duplica dados, não tem dono, foi rejeitada mais de uma vez |
| Área "Dados" separada com as tabelas cruas | vira um segundo sistema; cada tabela é uma tela normal no menu certo |
| Colocar toda tabela-filha no menu | o menu passa a rolar e ninguém acha nada |
| Mostrar `01HX…` porque "não tem nome" | o back precisa devolver um rótulo; peça |
| Cor diferente por assunto (financeiro verde, documento azul) | a cor deixa de significar estado |
| Abas com rolagem horizontal | no celular as últimas abas somem |
| `width: 100%` no modal para "caber" | o modal ocupa a tela toda em monitor largo |
