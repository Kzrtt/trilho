# 12 — Painel inicial e auditoria

Duas telas que todo sistema tem e que não são lista comum.

## A. Painel inicial

Responde a uma pergunta: **o que pede a minha atenção agora?** Não é vitrine de gráficos.

### Blocos, nesta ordem

1. **Números do momento** (2 a 4 ladrilhos): o que está aberto, o que está atrasado, o
   que chegou hoje. Cada ladrilho: ícone num quadro com tinta de realce (alternando as
   duas cores), número grande, rótulo curto. **O ladrilho é um link** para a lista já filtrada.
2. **Precisa de atenção**: lista curta (até 5) do que está pendente para **este nível**,
   cada item com contagem e link. Item com pendência ganha um ponto pulsante de realce.
   Sem pendência: "Tudo em dia." com ícone de sucesso.
3. **Fila de trabalho**: os registros mais urgentes; a linha abre o **mesmo modal** da lista.
4. **Série no tempo** (opcional): um gráfico simples (barras ou linha) do indicador
   principal. Barras na cor `marca`, com o **pico** em `realce`. Dia sem dado é lacuna.
5. **Resumo por área** (níveis de gestão): contagens por unidade/tipo, em barras horizontais.

### Regras

- O painel **muda por nível**: cada nível vê os blocos do que pode agir. Bloco sem
  permissão não aparece (não vira bloco vazio).
- Todo número vem do servidor já no recorte de quem olha.
- Painel de tela complexa tem guia ([`07`](07-GUIA-DE-TELA.md)): "O seu dia de trabalho".
- Entrada em cascata leve (ladrilhos sobem um após o outro), números contam ao aparecer;
  tudo desligável.
- No celular: ladrilhos em duas colunas, depois uma; gráfico em largura total.
- Indicador de população pequena não é exibido (supressão quando o grupo é menor que o
  mínimo definido pelo produto), com a explicação no lugar.

### Não fazer

Gráfico de pizza com muitas fatias; cores fora dos tokens; número sem link; "bem-vindo"
ocupando a primeira dobra; cartões todos iguais em fileira só para preencher.

## B. Auditoria

A tela que prova quem fez o quê. Permissão própria (ex.: `audit.view`).

### Lista

| Coluna | Conteúdo |
| --- | --- |
| Quando | data e hora |
| Quem | "Nome do operador (login)"; ação do sistema: "Sistema"; Admin agindo como outro: os dois |
| Ação | **badge**: Criou (sucesso), Alterou (info), Excluiu (erro), Restaurou (alerta), além das ações do domínio |
| Onde | a tabela, pelo nome em português |
| Registro | o **rótulo** do registro (nunca o ID), clicável: abre o modal dele |

Filtros: ação, tabela, período, quem; o Admin também por entidade. Busca pelo rótulo do registro.

### Detalhe (modal)

- Ficha: ação, registro, quem, quando, de onde (IP, aparelho) quando houver.
- **O que mudou**: tabela de três colunas, **Campo · Antes · Depois**, só com os campos
  que mudaram, rótulos em português, valores pelo vocabulário visual (status em badge,
  vínculo pelo nome, data formatada).
- Criação: só "Depois". Exclusão: só "Antes". Cascata: a lista de tabelas e contagens.
- Campos sensíveis **não aparecem** (o servidor não os grava no diff). Para registros de
  conteúdo sensível, a trilha mostra **que houve** a ação, sem o conteúdo.
- A chave do próprio registro some do diff; identificador solto vira "Registro vinculado".

### Regras

- **Só leitura.** Nenhum botão de editar ou excluir. A trilha não se apaga nem pelo Admin.
- Documento pessoal mascarado para quem não é Admin.
- Cada modal de registro tem a aba **Atividade**: a mesma trilha, filtrada por ele.
- Registros de **leitura** (quem abriu um dado sensível, quem leu um QR) são telas
  irmãs: mesma lista, mesmas regras, sem diff.

## C. Login (fora do painel)

Duas zonas: à esquerda o painel da marca (fundo charcoal, logo, uma frase, o ornamento
contínuo); à direita o formulário num cartão de ~400px, campos de 44px, um botão
primário. Mensagens de erro iguais para "não existe" e "senha errada". No celular, só o
formulário com a marca reduzida em cima. O login **não** usa os tokens `.adm`.
