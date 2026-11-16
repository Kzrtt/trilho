# Padrão de interface (Trilho)

Como todo sistema feito com este kit se parece e se comporta. Os documentos são
independentes de framework: descrevem anatomia, medidas, estados e regras. O nome de
cada peça em Angular e em React está em [`14-PECAS-POR-FRAMEWORK.md`](14-PECAS-POR-FRAMEWORK.md).

| Nº | Documento | Responde |
| --- | --- | --- |
| 00 | [PRINCIPIOS](00-PRINCIPIOS.md) | por que o padrão é assim; o fluxo lista → modal → edição |
| 01 | [TOKENS](01-TOKENS.md) | papéis de cor, paleta-base charcoal e sand, duas cores de realce, tipografia, medidas |
| 02 | [CASCA](02-CASCA.md) | topo, menu lateral em acordeão, perfil, gaveta no celular |
| 03 | [LISTAGEM](03-LISTAGEM.md) | cabeçalho, busca, filtros, barra de ações, tabela, paginação |
| 04 | [MODAL-DE-DETALHE](04-MODAL-DE-DETALHE.md) | ficha, ações, leitura em seções, abas de relação |
| 05 | [FORMULARIO](05-FORMULARIO.md) | cartões por grupo, grade de 12, validação, vínculos |
| 06 | [VOCABULARIO-VISUAL](06-VOCABULARIO-VISUAL.md) | badge, chip, data, citação; nunca ID; mesma palavra |
| 07 | [GUIA-DE-TELA](07-GUIA-DE-TELA.md) | o tutorial do topo das telas complexas |
| 08 | [CADASTROS-DECLARATIVOS](08-CADASTROS-DECLARATIVOS.md) | o motor: uma configuração vira lista, detalhe e formulário |
| 09 | [ACESSO-E-MENU](09-ACESSO-E-MENU.md) | menu único, permissões, poderes do Admin |
| 10 | [FEEDBACK-E-ESTADOS](10-FEEDBACK-E-ESTADOS.md) | confirmação, sucesso, erro, vazio, carregando |
| 11 | [RESPONSIVO-E-ACESSIBILIDADE](11-RESPONSIVO-E-ACESSIBILIDADE.md) | celular, teclado, contraste, movimento |
| 12 | [PAINEL-E-AUDITORIA](12-PAINEL-E-AUDITORIA.md) | tela inicial e tela de auditoria |
| 13 | [CONTRATO-COM-A-API](13-CONTRATO-COM-A-API.md) | o que o front espera do back |
| 14 | [PECAS-POR-FRAMEWORK](14-PECAS-POR-FRAMEWORK.md) | o kit de componentes e onde cada coisa mora |
| 15 | [VERIFICACAO](15-VERIFICACAO.md) | a lista de conferência e as varreduras automáticas |

## De onde veio

1. **Uma especificação visual de origem** (documento privado, que não acompanha este
   repositório) descreveu um painel administrativo maduro: papéis de
   cor, anatomia dos componentes e o fluxo lista → modal → edição.
2. **Urban Pass** (React) aplicou a especificação e acrescentou o guia de tela, a tabela
   que vira cartões no celular e o login em duas zonas.
3. **Fibro+** (Angular) é a versão mais completa: abas de relação em todo modal, edição
   ampla, vocabulário visual único, nunca ID cru, console de dados do Admin.

Tudo o que valia daquela especificação está reescrito nos documentos 01 a 12; este
padrão é a fonte.
