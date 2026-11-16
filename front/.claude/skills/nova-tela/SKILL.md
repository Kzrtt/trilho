---
name: nova-tela
description: Cria uma tela do painel com comportamento próprio (fila com decisão, quadro de etapas, assistente em passos, editor, importação, painel) montada só com as peças do kit, o controlador de lista e o modal de detalhe padrão. Use quando o usuário descrever um fluxo de trabalho ou regra de negócio que não é só criar/ver/editar/arquivar um registro.
---

# Nova tela

## Fase 0 — Entender o pedido como produto

1. Leia `AGENTS.md` (as 20 leis) e, de `docs/padrao/`: `00`, `03`, `04`, `07`, `10` e o que mais a tela tocar.
2. Se houver o repositório da API ao lado, leia o documento de domínio da área (`docs/dominio/`).
3. Reescreva o pedido em 3 a 5 frases: quem usa, o que decide ali, quais estados o
   registro percorre, o que cada ação provoca. **Se faltar regra de negócio, pergunte uma
   vez, com opções.** Não pergunte nada de layout.
4. **Procure antes de criar** (lei 14): já existe uma tela, aba, filtro ou modal desse
   assunto? Então a entrega é uma extensão dela: um filtro, um preset no menu, uma aba,
   uma seção, uma ação na faixa do modal. Diga onde vai encaixar.

## Fase 1 — Desenhar com o padrão

Responda por escrito, curto, antes de codar:

| Pergunta | Resposta padrão |
| --- | --- |
| Qual é a lista? | a fila/quadro; coluna principal + 2ª linha; status em badge |
| Qual é o **único** primário? | a ação que inicia o trabalho da tela |
| O que a linha abre? | o modal de detalhe do registro, com todas as colunas e as abas de relação |
| Quais ações mudam o estado? | botões na ficha/faixa do modal; cada uma com confirmação que diz o efeito; motivo quando recusa |
| O que é etapa? | linha do tempo com contagens, clicável como filtro |
| Precisa de guia? | sim, se houver ordem, mais de uma ação de estado ou consequência invisível (`/guia-de-tela`) |
| Quem vê o quê? | permissões por ação no arquivo de acesso; o resto escondido |
| O que acontece no vazio, no erro, no carregando? | textos definidos |
| E no celular? | cartões; ações acessíveis sem arrastar |

Variações permitidas (quadro, mapa + lista, assistente) estão em `03-LISTAGEM.md` §9 e `05-FORMULARIO.md` §7.

## Fase 2 — Construir por blocos

1. Serviço da API com os tipos **exatos** do contrato.
2. A lista com o controlador padrão (estado na URL) e as peças `Adm*`.
3. O modal: ficha, faixa de ações, abas, seções. Confira banco → API → modal.
4. As ações: diálogo de confirmação/formulário, chamada, sucesso, recarregar lista e modal.
5. Guia de tela e marcadores `data-guia`.
6. Item no menu (definição única) e as regras no arquivo de acesso.
7. Vocabulário: rótulos, badges e chips nos mapas centrais.

Teste junto com cada bloco. Tarefa grande: lista de tarefas, entrega por bloco coerente.

## Fase 3 — Conferir

`/revisao-visual` (ou `docs/padrao/15-VERIFICACAO.md` inteiro): testes, build de produção,
capturas 1440/390 com o modal aberto, varreduras de ID, texto cru e rolagem lateral,
entrada com cada nível.

## Não fazer

- Página só para ver um registro; edição dentro da tabela; segundo primário.
- Tela nova para o que é um filtro de tela existente.
- Regra de negócio reimplementada no front (quem pode aprovar, quando expira): a API diz.
- Componente novo dentro da tela para algo que é peça de kit.
