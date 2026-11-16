# Pedidos em linguagem natural (e o que cada um aciona)

O padrão existe para que o pedido fale só de negócio. Exemplos reais de como pedir.

## Começo de projeto

> Quero um sistema para a secretaria de obras controlar os pedidos de poda de árvore. O
> morador pede, um fiscal vistoria, o gestor aprova e uma equipe executa.

- API: `/prontuario` (entrevista → domínio, níveis, módulos).
- Interface: `/identidade` (nome, duas cores, menu).

## Uma coisa nova para cadastrar

> Preciso cadastrar as equipes de poda: nome, encarregado, telefone, quantas pessoas e se
> tem caminhão cesto. Cada equipe é de uma regional.

- API: `/nova-tabela` + `/novo-recurso-admin`.
- Interface: `/novo-cadastro`.
- Sai: item "Equipes" em Cadastros; lista com a equipe e a regional (chip); modal com
  Identificação, Contato, Estrutura, Registro; abas "Pedidos" e "Atividade"; formulário
  com a regional escolhida por busca; arquivar com aviso de quantos pedidos usam a equipe.

## Um fluxo de trabalho

> O gestor precisa aprovar os pedidos vistoriados. Ele vê o laudo e as fotos, aprova ou
> recusa com motivo. Aprovado entra na programação. O morador é avisado por e-mail nos
> dois casos.

- API: `/nova-feature` (Actions `approve`/`reject`, evento, listener de e-mail).
- Interface: `/nova-tela` + `/guia-de-tela`.
- Sai: tela "Aprovação" com linha do tempo (Vistoriados · Aprovados · Recusados), fila,
  modal com laudo e fotos, "Aprovar" (sucesso) e "Recusar" (pede motivo), confirmação
  dizendo que o morador será avisado, e o guia "Como aprovar um pedido".

## Um dado a mais

> No pedido, quero guardar também a espécie da árvore e a altura estimada.

- API: migration + recurso (o detalhe passa a devolver os dois) + "Para o front".
- Interface: os dois campos entram **na seção existente** "Árvore" do modal e no mesmo
  grupo do formulário. Nenhuma seção nova.

## Uma regra de acesso

> O fiscal só pode ver os pedidos da regional dele. O gestor vê todas.

- API: recorte no escopo do módulo + teste por nível.
- Interface: nada a fazer na lista (o servidor recorta); o filtro "Regional" some para o fiscal.

## Uma reclamação

> No modal da equipe não aparece quando ela foi criada, e na lista de pedidos está
> aparecendo um código esquisito no lugar do nome do fiscal.

- Interface: `/auditar-detalhe` (banco → API → modal; varredura de ID).
- Provável causa: a API não devolve `created_at` nem o nome do fiscal → pedido ao back.

## Uma mudança de regra

> A vistoria agora vale 60 dias, não 30.

- API: a regra e o teste; relatório.
- Interface: o texto do guia de tela que cita "30 dias" muda **na mesma entrega**.

## Antes de publicar

> Revisa tudo antes de eu mostrar para o cliente.

- Interface: `/revisao-visual` (testes, build, capturas 1440/390, varreduras, cada nível).
- API: `composer lint && composer lint:check && composer test`; `/sync-docs`.

## O que NÃO precisa estar no pedido

"em modal", "com paginação", "com badge", "com busca", "responsivo", "com confirmação",
"em português", "sem mostrar o ID", "com aba para os relacionados", "editável pelo admin".
Tudo isso é lei do padrão.
