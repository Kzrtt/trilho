# 10 — Feedback e estados

Toda mensagem ao usuário passa pelo **serviço de feedback** (uma peça global, com o tema
do painel). `alert()`, `confirm()` e `prompt()` do navegador não são usados.

```ts
feedback.success('Unidade salva.')
feedback.error('Não foi possível salvar.', detalhe?)
const ok = await feedback.confirm({ title, message, confirmLabel, danger? })
```

## 1. Confirmação

Pede confirmação: toda ação **destrutiva** (excluir, arquivar, revogar, desvincular),
toda ação **em massa**, toda ação **sem volta** ou que **avisa terceiros** (enviar
e-mail, publicar, emitir), e **Sair**.

Anatomia (diálogo pequeno, `role="alertdialog"`):

- **título** = a pergunta com o nome do registro: "Arquivar a unidade UBS Centro?";
- **mensagem** = o efeito, em uma ou duas frases, com números: "12 usuários e 240
  pacientes usam esta unidade. Ela sai das escolhas novas; o que já existe continua.";
- **botões**: "Cancelar" (neutro) à **esquerda** e o de confirmar à **direita**, com
  espaço entre eles. O de confirmar **repete o verbo** ("Arquivar", não "OK") e é
  *Perigo* quando destrutivo;
- o foco inicial vai para **Cancelar**; Esc cancela.

Ação que precisa de **motivo** (recusar, encerrar): a confirmação é um diálogo de
formulário com o campo "Motivo" obrigatório.

## 2. Sucesso

Aviso curto (toast) no canto, some sozinho em ~4s, `role="status"`: verbo no particípio +
o que foi: "Unidade salva.", "3 carteirinhas marcadas como impressas." Não existe tela
de confirmação separada.

Resultado que a pessoa **precisa** guardar (senha provisória, token gerado) **não** é
toast: é um diálogo que só fecha por ação, com botão de copiar e o aviso de que não
aparecerá de novo.

## 3. Erro

| Origem | Onde aparece |
| --- | --- |
| validação do campo (422 com `errors`) | embaixo do campo |
| regra de negócio sem campo (422/409) | alerta de erro no topo do formulário ou do diálogo, com a mensagem do servidor |
| sem permissão (403) | aviso: "Você não tem permissão para isto." |
| não encontrado (404) | no modal: "Este registro não existe mais." + fechar |
| servidor fora (5xx, rede) | aviso de erro com "Tentar de novo"; **o que a pessoa digitou não se perde** |
| muitas tentativas (429) | mensagem com o tempo de espera |

A mensagem do servidor já vem em português e é mostrada como veio. Nunca aparece código
de erro, rastro de pilha ou "undefined".

## 4. Alerta na tela

Faixa com ícone (fundo tom 50, borda tom 300, texto tom 700, ícone tom 500):

| Tipo | Uso |
| --- | --- |
| `info` | instrução ("Os campos em negrito são obrigatórios"), aviso permanente de tela |
| `alerta` | pendência, prazo, consequência de uma mudança |
| `erro` | falha |
| `sucesso` | resultado que precisa ficar visível (importação concluída: 40 criados, 2 com erro) |

## 5. Vazio

Bloco centralizado no lugar do conteúdo: ícone neutro, **frase que ensina** e, se couber,
a ação.

| Situação | Texto |
| --- | --- |
| área ainda sem registros | o que é a área + "Nova …" (se pode criar) |
| filtro sem resultado | "Nada encontrado para estes filtros." + "Limpar filtros" |
| aba de relação vazia | "Nenhum usuário nesta unidade." |
| sem permissão para aquele bloco | o bloco não aparece |

## 6. Carregando

- **Primeira carga** de lista, modal ou painel: esqueleto com a forma do conteúdo.
- **Recarga** (filtro, página): o conteúdo anterior fica, esmaecido; sem salto de layout.
- **Ação em andamento**: o botão mostra o gerúndio ("Salvando…") e trava.
- **Operação longa** (importação, geração de arquivo): a API responde 202; a tela mostra
  o andamento e avisa ao terminar. A pessoa pode sair e voltar.
- Indicador giratório só dentro de botão ou de bloco pequeno; nunca tela inteira.

## 7. Estados especiais

| Estado | Como aparece |
| --- | --- |
| Sem conexão | faixa de alerta fixa no topo do palco; ações de escrita desabilitadas com o motivo |
| Alteração não salva | pergunta ao sair |
| Registro mudou por outra pessoa (409) | mensagem + "Recarregar" |
| Sessão de "Entrar como" | faixa fixa: "Você está vendo o sistema como Fulana. [Encerrar]" |
| Ambiente de teste | selo no topo |

## 8. Texto das mensagens

- Diga o que aconteceu e o que fazer. "Não foi possível enviar o arquivo. Ele precisa ter
  até 2 MB." em vez de "Erro no upload".
- Sem culpa, sem exclamação, sem "Ops".
- Mesmo verbo do botão que a pessoa apertou.
