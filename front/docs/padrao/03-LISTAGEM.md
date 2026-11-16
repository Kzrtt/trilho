# 03 — Listagem

Toda área começa numa lista. A lista serve para **achar e reconhecer** um registro; ver e
agir é no modal ([`04`](04-MODAL-DE-DETALHE.md)).

## 1. Anatomia (de cima para baixo)

1. **Cabeçalho da tela** (título, descrição, botão primário "Novo …").
2. **Guia de tela**, se a área tiver fluxo ([`07`](07-GUIA-DE-TELA.md)).
3. **Linha do tempo de status**, se o registro passa por etapas: os passos do fluxo com a
   contagem de cada um; clicar num passo filtra a lista por aquele status.
4. **Barra**: busca ao vivo + botão de filtros à esquerda; "Atualizar lista" e (só Admin)
   "Ver excluídos" à direita.
5. **Tabela** em cartão.
6. **Paginação**: "Mostrar N", "1-20 de 240", páginas.

## 2. Busca e filtros

- **Busca**: um campo só, 34px, ao vivo com espera de ~300ms. Procura por nome sem
  diferenciar acento/maiúscula e por documento com ou sem máscara. O texto de exemplo diz
  o que dá para buscar ("Buscar por nome ou CPF").
- **Filtros**: o botão ao lado da busca abre um **modal de filtros** com um `select` por
  filtro (unidade, tipo, status...). As opções são buscadas na primeira abertura. Filtro
  ativo aparece como contagem no botão e pode ser limpo de uma vez.
- Filtro de conjunto pequeno e muito usado (status) pode ficar à vista como chips ou na
  linha do tempo, em vez de ir para o modal.
- Busca, filtros, ordem, página e tamanho ficam na **URL**. Só vai para a URL o que
  difere do padrão.

## 3. Tabela

```
┌───────────────────────────────────────────────────────────────────────────┐
│ NOME ↑                    UNIDADE          SITUAÇÃO        CRIADO EM      │  cabeçalho neutro-50, 11,5px/600
├───────────────────────────────────────────────────────────────────────────┤
│ Maria Aparecida Souza     (⌂ UBS Centro)   (✓ Ativa)       12/03/2026  ⟩  │
│ ***.456.789-** · 54 anos                                                  │  2ª linha: 12px apagado, partes com ·
├───────────────────────────────────────────────────────────────────────────┤
```

Regras de coluna:

- **Coluna principal** (a primeira): o que identifica o registro, em 600. Embaixo, uma
  segunda linha de 12px com 1–3 dados de apoio separados por `·`. Largura mínima 240px.
  Vazia: "Não informado" em itálico apagado.
- **De 4 a 6 colunas.** A lista não é o lugar de mostrar tudo.
- **Status sempre em badge.** Vínculo sempre em chip com o **nome** do outro registro.
  Código em chip monoespaçado. Ver [`06`](06-VOCABULARIO-VISUAL.md).
- Data curta (`dd/mm/aaaa`), números e códigos sem quebra de linha.
- **Sem coluna de ID.** Sem coluna de checkbox, salvo se a tela tiver ação em massa de verdade.
- Ordenação: clique no título. A coluna ordenada mostra a seta. A ordem é do servidor.
- A **última coluna é a seta** (botão 30×30, `aria-haspopup="dialog"`,
  `aria-label="Abrir detalhes de <nome>"`). A linha inteira também é clicável.

Estados da linha:

| Estado | Visual |
| --- | --- |
| normal | fundo do cartão, divisor `neutro-100` |
| hover | fundo `neutro-50`, seta escurece |
| **modal aberto** | fundo `marca-50`, divisor `marca-200` |
| **última vista** | fundo `neutro-50` (marca de leve onde a pessoa estava) |
| excluído/arquivado (quando visível) | texto apagado + badge neutro "Arquivado"/"Excluído" |
| pede atenção | um badge de alerta ou sinal na linha; **nunca** faixa lateral colorida |

O cartão da tabela arredonda os cantos com `overflow: hidden`; nada dentro dele pode
abrir para fora (dropdown em célula não).

## 4. Barra de ações

- Esquerda: busca e filtros.
- Direita: botões **neutros** de apoio com ícone ("Atualizar lista", exportar, importar)
  e o alternador "Ver excluídos" (só Admin).
- Ação em massa só quando existe de verdade (ex.: "Marcar como impressas"): a seleção
  aparece, a barra troca para "N selecionados · [ação] · [limpar]", e a ação pede
  confirmação dizendo quantos serão afetados.
- O primário ("Novo …") fica no cabeçalho da tela, não na barra.

## 5. Paginação

- "Mostrar": 10, 20, 50, 100 (padrão 20; máximo aceito pelo servidor: 100).
- Texto "**21-40** de 240" (milhar com ponto) ou a mensagem de vazio.
- Janela de páginas: primeira, última e duas de cada lado da atual, com reticências.
  Setas desabilitadas nas pontas.
- Página pedida além do fim: o servidor devolve a última; a URL é corrigida.

## 6. Vazio, carregando, erro

- **Carregando**: esqueleto das linhas (primeira carga) ou a lista anterior esmaecida
  (troca de página/filtro). Nunca a tela piscar em branco.
- **Vazio sem filtro**: ícone, frase que explica o que é a área e o botão de criar (se pode).
- **Vazio com filtro**: "Nada encontrado para estes filtros." + "Limpar filtros".
- **Erro**: alerta de erro com "Tentar de novo". A lista não some se já havia dados.

## 7. O controlador da lista

A lógica é uma peça só, reaproveitada por todas as telas (não reescreva por tela):

```ts
interface ListQuery { page: number; perPage: number; q: string; order: string; filters: Record<string, string> }
// lê a URL → ListQuery (valor inválido ou ausente = padrão)
// ListQuery → parâmetros da API (só o que foi definido)
// ListQuery → parâmetros da URL (só o que difere do padrão)
// mudar busca/filtro/ordem volta para a página 1
// resposta: { data: T[], meta: { total, page, per_page, last_page, counts } }
```

`meta.counts` alimenta a linha do tempo e as contagens das abas de status. As contagens
respeitam a busca e ignoram o próprio filtro de status.

## 8. No celular (abaixo de 640px)

Cada linha vira um **cartão**: a coluna principal é o título; as outras viram pares
"rótulo: valor" (o rótulo vem do cabeçalho da coluna); o cartão inteiro abre o modal. Sem
rolagem lateral. A barra empilha: busca em largura total, botões embaixo.

## 9. Variações permitidas

| Variação | Quando | O que não muda |
| --- | --- | --- |
| Quadro (colunas por estado, arrastar) | fluxo com poucas etapas e trabalho diário | o cartão abre o mesmo modal; toda ação de arrastar tem um botão equivalente |
| Mapa + lista | registro com endereço | clicar no ponto abre o mesmo modal |
| Lista local (API devolve tudo) | conjunto pequeno e fechado (< 200) | busca, ordem e página com a mesma aparência; estado na URL |
| Fila (ordenada por prioridade) | trabalho a decidir | linha do tempo + mesmo modal |
