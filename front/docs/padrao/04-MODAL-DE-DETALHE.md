# 04 — Modal de detalhe

O centro do sistema. **Toda** lista abre o detalhe do registro num modal, que resume o
registro, concentra as ações, mostra **todos** os dados e dá acesso a tudo que está ligado
a ele.

## 1. Anatomia

```
┌──────────────────────────────────────────────────────────────────────── ✕ ┐
│ [ícone]  UNIDADE · (✓ Ativa) (tipo)                     [Arquivar] [Editar]│  ficha
│          UBS Centro                                                        │
│          CNES 1234567 · Francisco Beltrão      Entidade: Prefeitura …      │
│ ────────────────────────────────────────────────────────────────────────── │
│ [▣ Imprimir] [▣ Redefinir senha] [▣ Entrar como]                           │  faixa de ações (neutras)
├────────────────────────────────────────────────────────────────────────────┤
│  Dados   Usuários (12)   Médicos (3)   Pacientes (240)   Atividade         │  abas
├────────────────────────────────────────────────────────────────────────────┤
│ ┌ IDENTIFICAÇÃO ─────────────────────────────────────────────────────────┐ │  corpo (só ele rola)
│ │ Nome           Sigla        CNES          Situação                     │ │
│ │ [UBS Centro ]  [UBSC]       [1234567]     (✓ Ativa)                    │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
│ ┌ ENDEREÇO ──────────────────────────────────────────────────────────────┐ │
│ ┌ REGISTRO ───────────────── Criado em · Última alteração ───────────────┐ │
└────────────────────────────────────────────────────────────────────────────┘
```

| Parte | Regra |
| --- | --- |
| Fundo | escurece a página (`rgba(30,30,28,.45)`); clicar fecha |
| Caixa | largura máx. **1320px**, altura máx. `100vh - 32px`, raio 12px, `sombra-alta`; entra com `opacity` + `translateY(6px)` |
| X | canto superior direito, 34×34 |
| Cabeça | fixa; ficha + faixa de ações |
| Abas | fixas, logo abaixo da cabeça; **quebram de linha**, nunca rolam |
| Corpo | fundo `neutro-50`; **é a única parte que rola** |
| Rodapé | **não existe** |

## 2. Ficha (o resumo)

- **Ícone** do tipo de registro num quadro 44×44 `neutro-100`.
- **Rótulo** em caixa-alta 11px: o tipo ("UNIDADE") e, ao lado, os **badges** de estado.
  Se o registro tem um número com significado (nº do documento, do pedido), aparece como
  "Nº 000123". **Identificador interno nunca.**
- **Título** 18px/650: o nome que a pessoa usa para reconhecer o registro.
- **Linha de resumo**: subtítulo (documento · cidade) e 2–4 metadados "Rótulo: valor".
- **Botões à direita**: a ação destrutiva em *perigo discreto* e **Editar** como primário.
  Ação que não vale para este registro fica desabilitada com o motivo no `title`; o lugar
  do botão é mantido.

## 3. Faixa de ações

Todas as outras ações do registro, em botões **neutros** de 34px com o ícone num quadro
`neutro-100` de 26px. Não importa o assunto (documento, e-mail, dinheiro): cinza. Só a
destrutiva usa a família erro. Ações só do Admin (editar dados brutos, restaurar, "entrar
como") ficam aqui, à direita das demais.

## 4. Abas

- A primeira é sempre **Dados**.
- Depois, **uma aba para cada tipo de registro relacionado**, com a contagem entre
  parênteses quando a API a devolve. A ordem é a do uso, não a alfabética.
- Por último, quando fizer sentido, **Atividade** (a trilha de auditoria daquele registro)
  e abas próprias do domínio.
- A aba ativa vai para a URL (`?aba=`). Abrir outro registro volta para "Dados".
- Aba que o nível não pode ver **não aparece** (a permissão é a da lista relacionada).

### Aba de relação

A lista do outro recurso **filtrada por este registro** (`?<pai>_id=<id>`), desenhada com
a mesma tabela das listas, paginada, com o texto de vazio próprio ("Nenhum usuário nesta
unidade."). Clicar numa linha abre **o modal daquele registro** (por cima, com volta).

Pode ter, por permissão: "Vincular …" (abre a busca e liga um existente), "Novo …" (cria já
ligado a este) e "Desvincular" na linha (com confirmação).

### Aba de lista-filha

Itens que só existem dentro do pai (níveis de uma condição, itens de um pedido). Edita-se
**no próprio lugar**: a linha vira campos, com Salvar/Cancelar na linha. É a única edição
inline do sistema.

## 5. Corpo: leitura em formato de formulário

- Uma **seção por tema**, no mesmo desenho dos grupos do formulário: cartão `neutro-0`,
  faixa de título em caixa-alta com ícone.
- **Grade de 12 colunas**; cada campo ocupa 3, 4, 6, 8, 9 ou 12 (padrão 4). Texto longo: 12.
- **Campo**: rótulo em cima (12,5px/500) e o valor numa **caixa leve** (`neutro-50`, borda
  `neutro-100`), mais leve que um campo editável, para não parecer digitável.
- O valor é desenhado pelo **vocabulário visual** ([`06`](06-VOCABULARIO-VISUAL.md)):
  estado em badge, vínculo em chip clicável, código em chip mono, data formatada, texto
  longo como citação. Quem decide é o rótulo/tipo do campo, num lugar só.
- Vazio: "—" apagado. Grupo inteiro sem dados: não aparece.
- Segredo nunca aparece (nem mascarado com opção de revelar).

### A regra dos campos (lei 2)

**Toda coluna da tabela aparece no modal.** Para conferir (skill `/auditar-detalhe`):

1. liste as colunas da tabela no banco;
2. compare com as chaves que o endpoint de detalhe devolve;
3. compare com os campos do modal.

A falta pode estar na API (o recurso omite `created_at`, quem decidiu, o motivo) e não só
na tela: **peça o campo ao back**, não invente. Ficam de fora só: segredos, a data de
exclusão e colunas técnicas de busca.

Cada campo que faltava entra **na seção existente que combina**. Toda ficha tem, no fim, a
seção **Registro**: "Criado em", "Última alteração" e, se houver, por quem.

**Proibido** uma seção genérica para o que sobrou.

### Seção carregada à parte

Uma seção pode buscar os próprios dados quando o modal abre (ex.: um resumo de números da
unidade). Mostra esqueleto enquanto carrega e some se o nível não tem permissão.

## 6. Comportamento

1. **Abrir**: guarda quem abriu (para devolver o foco), marca a linha como aberta, trava a
   rolagem da página, foca a caixa. O registro aberto vai para a URL (`?ver=<id>`):
   recarregar ou mandar o link abre o mesmo modal.
2. **Carregar**: a ficha aparece na hora com o que a lista já trouxe; o resto vem do
   endpoint de detalhe. Enquanto vem, esqueleto das seções.
3. **Fechar**: X, fundo, Esc. Devolve o foco, destrava a rolagem, marca a linha como
   "última vista", tira `?ver=` e `?aba=` da URL. Navegar para outra rota com o modal
   aberto também destrava a rolagem.
4. **Foco preso**: Tab e Shift+Tab ciclam dentro do modal.
5. **Depois de editar/arquivar**: o modal recarrega o registro e a lista se atualiza por baixo.
6. **Modal sobre modal**: só um nível a mais (o registro relacionado). Esc fecha o de cima.

## 7. Link para um registro

Qualquer menção a um registro em qualquer tela (chip numa lista, linha de uma aba, item da
auditoria) leva ao **modal** dele, não a uma página.

Registro com conteúdo grande demais para um modal (um prontuário, um editor) tem a página
própria; mesmo assim, o primeiro passo é o modal, com o primário "Abrir … completo".

## 8. Abaixo de 760px

A caixa ocupa a tela com margem de 8px; a ficha empilha (botões descem para uma linha
própria, em largura total); todo campo ocupa a linha inteira; as abas quebram em mais de
uma linha; a tabela das abas vira cartões.

## 9. Armadilhas

- **Nunca** ponha `width`/`max-width: 100%` na caixa para resolver texto que estoura: ela
  passa a ocupar o monitor inteiro. Use `overflow-wrap: anywhere` e `min-width: 0` nos
  filhos. Meça a largura em 1440 e em 1920.
- O modal fica **fora** de qualquer cartão com `overflow: hidden` e de qualquer `<form>`.
- Dropdown "atrás" do conteúdo: um ancestral criou contexto de empilhamento sem `z-index`.
- A classe que trava a rolagem precisa sair quando o componente é destruído.
