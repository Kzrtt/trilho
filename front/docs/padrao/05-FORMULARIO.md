# 05 — Formulário (criar e editar)

## 1. Onde o formulário abre

| Caso | Forma |
| --- | --- |
| Cadastro com vários grupos de campos | **tela** própria (`/<área>/novo`, `/<área>/<id>/editar`), dentro da casca |
| Ação curta (até ~6 campos: decidir, redefinir senha, vincular, importar) | **diálogo de formulário**, sobre a tela ou sobre o modal |
| Lista-filha dentro do modal | na própria linha ([`04`](04-MODAL-DE-DETALHE.md), §4) |
| "Editar dados" do Admin (todas as colunas editáveis de um registro) | diálogo de formulário gerado a partir das colunas |

A anatomia é a mesma nos quatro.

## 2. Anatomia

```
Unidades                                             [← Voltar para a lista]
Editar unidade
(i) Os campos em negrito são obrigatórios.

┌ IDENTIFICAÇÃO ─────────────────────────────────────────────────────────────┐
│ Nome (8)                                     Sigla (4)                     │
│ [...............................]            [.......]                     │
│ Tipo (4)            Entidade (8)                                           │
│ [selecionar ▾]      [buscar entidade...             🔍]                    │
└────────────────────────────────────────────────────────────────────────────┘
┌ ENDEREÇO ──────────────────────────────────────────────────────────────────┐
└────────────────────────────────────────────────────────────────────────────┘
                                                        [Cancelar] [✓ Salvar]
```

- **Um cartão por grupo**, com a mesma faixa de título do modal de detalhe (caixa-alta,
  ícone). A ordem e os nomes dos grupos são **os mesmos** das seções do detalhe: quem leu
  o modal reconhece o formulário.
- **Grade de 12 colunas**; cada linha soma 12. Abaixo de 900px, uma coluna.
- **Rótulo em cima** do controle (13px/500). **Obrigatório = rótulo em negrito**; sem
  asterisco. Um alerta `info` no topo explica isso.
- **Ajuda** do campo: 12px apagado, embaixo, com ícone de informação.
- **Rodapé**: "Cancelar" (neutro, à esquerda do par) e **"Salvar"** (botão *secundário*
  escuro `neutro-800`, com ícone de check), separados por um espaço claro. O primário de
  cor fica reservado para a ação principal de cada tela (Novo, Editar); salvar é escuro.

## 3. Controles

| Tipo do dado | Controle |
| --- | --- |
| texto curto | input 38px |
| texto longo | textarea (mín. 96px, redimensiona na vertical), linha inteira |
| número, dinheiro | input com teclado numérico; dinheiro com máscara |
| data | campo de data nativo ou com máscara `dd/mm/aaaa` |
| documento, telefone | máscara na tela; só os dígitos vão para a API |
| conjunto fechado (status, tipo, sim/não com mais de 2 estados) | **select** com as palavras do mapa central |
| sim/não | interruptor (switch) com o texto do lado; vários → uma linha só de interruptores |
| **vínculo com outro registro** | **campo de relação**: mostra o nome escolhido e abre uma busca (por nome e documento, no servidor, até 30 resultados); nunca um select com centenas de opções, nunca texto livre |
| lista de textos | campo de lista (adicionar, remover, reordenar) |
| lista de objetos | campo de linhas (uma linha por item, colunas em 12 avos) |
| arquivo/imagem | área tracejada com o botão; mostra tipos e tamanho máximo aceitos e a prévia |
| senha | nunca se mostra nem se edita o valor guardado; a ação é "Redefinir senha" (gera provisória) |

Estilo comum: borda `neutro-300`, raio 6px, fundo `neutro-0`; hover borda `neutro-400`;
**foco** borda `neutro-800` + halo 3px `neutro-300` (neutro, nunca a cor da marca);
desabilitado fundo `neutro-100`.

## 4. O que é editável (lei 4)

- **Toda coluna da tabela é editável** por quem tem a permissão de escrita, menos: chave
  primária, datas de controle (criado/alterado/excluído) e segredos.
- Campo que **não pode mais mudar** (um código já em uso) aparece **travado**, com o motivo
  embaixo, e não é enviado.
- Campo que só existe para um nível (a entidade de uma unidade nova é escolha do Admin)
  aparece só para ele.
- Campo que só existe ao criar ou só ao editar é declarado assim, não escondido por CSS.
- Trocar status "à mão" por um campo é poder do Admin e do diálogo "Editar dados". No
  fluxo normal, status muda por **ação** (Aprovar, Encerrar), que roda as regras.

## 5. Validação e envio

- O front valida só o óbvio para dar resposta rápida: obrigatório, tamanho máximo,
  formato de código/documento.
- **O servidor é a autoridade.** Ele responde `422 { message, errors: { campo: [..] } }` e
  cada mensagem aparece **embaixo do campo** (inclusive numa linha de um campo de linhas).
  Erro sem campo vira alerta no topo do formulário.
- **Estado de erro é só na borda** (1,5px `erro-500`), rótulo em `erro-700`, mensagem com
  ícone embaixo. Nunca fundo colorido no campo.
- Ao editar, envia-se **só o que mudou** (`PATCH` parcial). Nada mudou: o botão Salvar
  fica desabilitado.
- Enquanto envia: Salvar mostra "Salvando…" e trava; duplo clique não cria dois.
- Depois de salvar: mensagem de sucesso curta e volta para onde a pessoa estava (a lista
  com o modal do registro aberto).
- **Sair com alteração não salva pergunta antes** (guarda de navegação e de fechar o diálogo).
- `409` (o estado mudou enquanto a pessoa editava): mensagem clara e recarregar o registro.

## 6. Receitas de layout

| Conteúdo | Linhas (em 12 avos) |
| --- | --- |
| Identificação | Nome 8 · Sigla/Código 4 |
| Pessoa | Nome 6 · Documento 3 · Nascimento 3 |
| Contato | E-mail 6 · Telefone 3 · Celular 3 |
| Endereço | CEP 3 · Logradouro 6 · Número 3 // Bairro 4 · Cidade 5 · UF 3 |
| Vínculos | cada vínculo 6 (o campo de relação precisa de largura) |
| Observações | 12 |
| Interruptores | uma linha só deles, 3 ou 4 cada |

Rótulo comprido em coluna estreita quebra e desalinha: escolha larguras em que caiba.

## 7. Formulário longo ou em etapas

- Muitos grupos: cartões por tema, na ordem em que a pessoa pensa.
- Sequência obrigatória (assistente): passos numerados no topo, um passo por vez,
  "Voltar" e "Continuar", resumo antes de confirmar, e **nada se perde** ao voltar um passo.
- Editor de estrutura (árvore de itens): cada nó tem o próprio pequeno formulário e é
  salvo sozinho; a tela se redesenha com a resposta do servidor.

## 8. Armadilhas

- Cartão de grupo **sem** `overflow: hidden` (corta dropdown e calendário).
- Nada de `input { width: 100% }` global; a largura vem da coluna da grade.
- Mensagem de erro precisa de respiro reservado embaixo do campo, senão a tela "pula".
- Não usar validação nativa do navegador (`required`, `pattern`) junto com a própria.
