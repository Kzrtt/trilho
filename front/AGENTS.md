# AGENTS.md — front (padrão Trilho)

Guia para qualquer pessoa ou agente que escreva a interface deste projeto.
**Leia antes de escrever código.** Vale para qualquer framework (Angular, React, Vue...):
o que é fixo é o **comportamento** e a **aparência** do sistema; o que muda é a sintaxe.

O dono do produto descreve o negócio (modelagem, requisitos, regras). Este arquivo e os
documentos em [`docs/padrao/`](docs/padrao/README.md) decidem **como a tela sai**. Não
pergunte ao dono como deve ser uma lista, um detalhe ou um formulário: está escrito aqui.
Pergunte só o que é decisão de produto (o que o sistema faz, quem pode, com que palavras).

## Visão do projeto

> PREENCHIDO PELA SKILL `/identidade`. Enquanto este bloco existir, o projeto ainda não
> tem nome, paleta, níveis de acesso nem menu definidos. Rode `/identidade` antes da
> primeira tela.

## Ordem de leitura

| Vai fazer | Leia |
| --- | --- |
| Qualquer coisa | este arquivo inteiro e [`docs/padrao/00-PRINCIPIOS.md`](docs/padrao/00-PRINCIPIOS.md) |
| Cores, fontes, espaçamento | [`01-TOKENS.md`](docs/padrao/01-TOKENS.md) |
| Topo, menu, perfil | [`02-CASCA.md`](docs/padrao/02-CASCA.md) |
| Uma lista | [`03-LISTAGEM.md`](docs/padrao/03-LISTAGEM.md) |
| O detalhe de um registro | [`04-MODAL-DE-DETALHE.md`](docs/padrao/04-MODAL-DE-DETALHE.md) |
| Criar ou editar | [`05-FORMULARIO.md`](docs/padrao/05-FORMULARIO.md) |
| Status, vínculos, datas, códigos | [`06-VOCABULARIO-VISUAL.md`](docs/padrao/06-VOCABULARIO-VISUAL.md) |
| Tela com regra de negócio difícil | [`07-GUIA-DE-TELA.md`](docs/padrao/07-GUIA-DE-TELA.md) |
| Um cadastro simples (lista + detalhe + form) | [`08-CADASTROS-DECLARATIVOS.md`](docs/padrao/08-CADASTROS-DECLARATIVOS.md) |
| Menu, permissões, o que o Admin vê | [`09-ACESSO-E-MENU.md`](docs/padrao/09-ACESSO-E-MENU.md) |
| Confirmação, erro, vazio, carregando | [`10-FEEDBACK-E-ESTADOS.md`](docs/padrao/10-FEEDBACK-E-ESTADOS.md) |
| Celular e acessibilidade | [`11-RESPONSIVO-E-ACESSIBILIDADE.md`](docs/padrao/11-RESPONSIVO-E-ACESSIBILIDADE.md) |
| Painel inicial e auditoria | [`12-PAINEL-E-AUDITORIA.md`](docs/padrao/12-PAINEL-E-AUDITORIA.md) |
| O que a API precisa devolver | [`13-CONTRATO-COM-A-API.md`](docs/padrao/13-CONTRATO-COM-A-API.md) |
| Nomes das peças em Angular e em React | [`14-PECAS-POR-FRAMEWORK.md`](docs/padrao/14-PECAS-POR-FRAMEWORK.md) |
| Conferir antes de entregar | [`15-VERIFICACAO.md`](docs/padrao/15-VERIFICACAO.md) |

## As 20 leis do painel

Cada lei tem o motivo. Quando duas parecerem colidir, vale a de número menor.

1. **Lista → modal → edição.** Clicar numa linha (ou na seta dela) abre o **modal de
   detalhe**. Não existe edição dentro da tabela, nem página só para ver um registro.
   *Motivo: a pessoa nunca perde o lugar na lista.*
2. **O modal mostra tudo.** Todas as colunas da tabela aparecem no detalhe, em seções
   por tema. Ficam de fora só segredos (senha, token) e a data de exclusão. **Proibido**
   bloco genérico ("Outros dados", "Todos os campos"): cada campo entra na seção que já
   existe; seção nova só se nenhuma servir.
3. **Relação vira aba.** O modal tem a aba "Dados" e uma aba para cada tipo de registro
   ligado (Unidade → usuários, pacientes...). A linha de uma aba abre o modal daquele
   registro. *Motivo: dá para andar pelo sistema inteiro sem sair do lugar.*
4. **Tudo se edita.** Toda coluna é editável por quem tem permissão, menos chave
   primária, datas de controle e segredos. O nível mais alto (Admin) edita e vê tudo,
   inclusive registros excluídos, e nunca é barrado por falta de contexto.
5. **Nunca ID cru.** Em lista, cabeçalho de modal, campo, aba ou auditoria: no lugar do
   identificador aparece um nome útil do outro registro. Sem nome, "Registro sem nome";
   o ID nunca.
6. **Vocabulário fixo é badge; coisa é chip.** Status, tipo, papel, sim/não: badge com
   cor, ícone e texto. Registro vinculado, código, documento: chip. Texto cru nesses
   casos é defeito. A mesma palavra em todas as telas, vinda de **um** mapa central.
7. **Vínculo se escolhe numa lista com busca.** Nunca texto livre para ligar um registro
   a outro. Valor de conjunto fechado é `select`.
8. **Cor é exceção.** Um botão primário por tela. Todo o resto é neutro. Cor aparece em
   estado (badge, alerta), perigo, sucesso e nas duas cores de realce, em dose pequena.
   Sem faixa colorida na lateral de cartão ou item. Sem sombra em item de menu.
9. **Estado nunca só por cor.** Sempre cor + ícone + texto.
10. **A lista roda no servidor e o estado mora na URL.** Página, tamanho, busca, ordem,
    filtros, registro aberto (`?ver=`) e aba (`?aba=`) estão no endereço: o link de um
    colega abre a mesma coisa.
11. **Exclusão é lógica.** Arquivar/restaurar, com prévia do que será afetado antes de
    confirmar. Não existe apagar de verdade em nenhuma tela.
12. **Tela complexa tem guia no topo.** Fluxo com regra de negócio (fila, aprovação,
    emissão) abre com a faixa de passos "Como funciona esta tela".
13. **Um menu, uma definição.** O mesmo arquivo alimenta a lateral e a gaveta do
    celular, filtrado por permissão. O que o nível não pode fazer não aparece. Tabela
    que já se edita dentro de um pai **não** ganha item de menu.
14. **Integrar ao que existe.** Dado novo entra na tela, na seção e no modal que já
    tratam do assunto. Nunca uma área paralela ("Dados", "Extras", "Avançado").
15. **Mensagem pelo serviço de feedback.** Confirmação, sucesso e erro usam o serviço
    próprio; `alert`/`confirm` do navegador não. Erro de validação (422) aparece embaixo
    do campo.
16. **No celular só rola na vertical.** Tabela vira cartões, abas quebram de linha, menu
    vira gaveta pela esquerda. Rolagem lateral é defeito.
17. **Foco visível, teclado, leitor de tela.** Modal com foco preso, Esc e retorno do
    foco; botão só de ícone com `title` e `aria-label`; contraste AA.
18. **Token, nunca hex.** Toda cor, raio, sombra e fonte vem dos tokens `--adm-*`,
    escopados na classe `.adm`. Nada do painel vaza para a área pública.
19. **Peça do kit, nunca marcação solta.** Use os componentes `Adm*`. Faltou uma peça?
    Crie-a no kit, com teste, e use-a.
20. **Texto de tela em português simples; código em inglês.** Rótulos, mensagens e
    cabeçalhos em pt-BR, frases curtas, sem jargão. Identificadores, classes e
    comentários em inglês.

## Definição de pronto (toda tela)

- [ ] Segue as 20 leis; conferido com [`15-VERIFICACAO.md`](docs/padrao/15-VERIFICACAO.md).
- [ ] Testes da tela verdes; verificação de tipos e build de produção verdes.
- [ ] Capturas em 1440×900 e 390×844, com o modal aberto, olhadas de verdade.
- [ ] Nenhum ID na tela (varredura), nenhuma rolagem lateral, nenhum texto em inglês.
- [ ] Se a API não devolve um campo que a tela precisa: o pedido foi feito ao back
      (ver [`13-CONTRATO-COM-A-API.md`](docs/padrao/13-CONTRATO-COM-A-API.md)), não contornado.

## Skills (`.claude/skills/`)

| Skill | Quando usar |
| --- | --- |
| `/identidade` | Primeira coisa num projeto: nome, logo, as duas cores de realce, fontes, níveis de acesso, menu. Gera os tokens e preenche a "Visão do projeto" |
| `/novo-cadastro` | Tabela com lista + detalhe + formulário simples: cria a configuração declarativa |
| `/nova-tela` | Tela com comportamento próprio (fila, quadro, editor), montada com as peças do kit |
| `/auditar-detalhe` | Conferir banco → API → modal: todo campo aparece, nenhum ID, tudo editável |
| `/guia-de-tela` | Escrever o tutorial do topo de uma tela complexa |
| `/revisao-visual` | Antes de entregar: capturas, varreduras e a lista de verificação |

## Como falar com o dono do produto

- Ele descreve o negócio em linguagem natural. Traduza para telas usando o padrão; não
  devolva perguntas de layout.
- Quando o pedido couber em algo que existe, **estenda o que existe** (lei 14) e diga
  onde colocou.
- Entregou? Diga o que mudou, o que foi conferido e o que ficou de fora. Ressalva se
  declara; nunca se esconde.
- Faltou decisão de produto (quem pode, qual palavra, o que acontece quando)? Pare e
  pergunte uma vez, com opções.

## Nunca

- Criar bloco, seção, aba ou área genérica para "sobras".
- Mostrar identificador, nome de coluna do banco ou valor de enum em inglês.
- Pôr cor em botão que não seja o primário, o de perigo ou o de sucesso.
- Paginar, buscar ou ordenar no navegador uma lista que cresce.
- Largura fixa, `overflow-x: auto` em abas, sombra em item de menu, faixa lateral colorida.
- Declarar pronto sem ter olhado as capturas.
