"""Gera o Manual do Trilho (HTML para PDF). Uso: python3 -I build.py && node pdf.cjs && node wm.cjs"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).parent
KIT = ROOT.parent
ICONS = json.loads((ROOT / 'icons/icons.json').read_text())
E = html.escape
MARK = ICONS['train-track']


def ic(name, cls='ic'):
    assert name in ICONS, name
    return f'<span class="{cls}">{ICONS[name]}</span>'


SRC = {'fb': ('Fibro+', 'a1'), 'up': ('Urban Pass', 'a2')}


def shot(img, caption, kind='wide', crop=None):
    assert (ROOT / f'img/{img}.jpg').exists(), img
    label, cls = SRC[img[:2]]
    style = f' style="max-height:{crop}mm"' if crop else ''
    return (f'<figure class="shot {kind}"><div class="frame"><img src="img/{img}.jpg"{style}></div>'
            f'<figcaption><span class="src {cls}">{label}</span>{caption}</figcaption></figure>')


def diag(name, caption, h=None):
    assert (ROOT / f'diagramas/{name}.svg').exists(), name
    style = f' style="max-height:{h}mm"' if h else ''
    return f'<figure class="diag"><img src="diagramas/{name}.svg"{style}><figcaption>{caption}</figcaption></figure>'


def row(*figs, cls='row'):
    return f'<div class="{cls}">{"".join(figs)}</div>'


def steps(items):
    return '<ol class="steps">' + ''.join(f'<li><b>{E(t)}</b><span>{d}</span></li>' for t, d in items) + '</ol>'


def note(text, kind='info', title=None):
    icon = {'info': 'info', 'tip': 'sparkles', 'lock': 'lock', 'warn': 'triangle-alert'}[kind]
    head = f'<b>{E(title)}</b> ' if title else ''
    return f'<aside class="note {kind}">{ic(icon)}<p>{head}{text}</p></aside>'


def chips(*items):
    return '<span class="chips">' + ''.join(f'<span class="chip {c}">{E(t)}</span>' for t, c in items) + '</span>'


def part(num, title, lead, icon, color='charcoal'):
    return (f'<section class="part {color}"><div class="part-sym">{MARK}</div>'
            f'<div class="part-badge"><span class="part-logo">{MARK}</span><span>Trilho</span></div>'
            f'<div class="part-num">{"Parte " + str(num) if str(num).isdigit() else "Apêndices"}</div>{ic(icon, "part-ic")}<h1>{E(title)}</h1><p>{lead}</p></section>')


def chapter(code, title, lead, icon):
    return (f'<header class="chap"><div class="chap-code">{code}</div><div class="chap-body">'
            f'<h2>{ic(icon)}{E(title)}</h2><p class="lead">{lead}</p></div></header>')


def h3(t):
    return f'<h3>{E(t)}</h3>'


def p(t):
    return f'<p>{t}</p>'


def bullets(items):
    return '<ul class="bul">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def stats(items):
    return '<div class="stats">' + ''.join(f'<div><b>{E(str(n))}</b><span>{E(t)}</span></div>' for n, t in items) + '</div>'


def cards(items, cols=3):
    return f'<div class="cards c{cols}">' + ''.join(
        f'<div class="card">{ic(i)}<b>{E(t)}</b><p>{d}</p></div>' for i, t, d in items) + '</div>'


def law(n, title, why):
    return f'<div class="law"><span class="law-n">{n}</span><div><b>{E(title)}</b><p>{why}</p></div></div>'


def table(head, rows_, cls='grid'):
    th = ''.join(f'<th>{E(h)}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows_)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def ask(prompt, out):
    return (f'<div class="ask"><div class="ask-q">{ic("message-square-text")}<p>{prompt}</p></div>'
            f'<div class="ask-a">{ic("wand-sparkles")}<p>{out}</p></div></div>')


def count(glob):
    return len(list(KIT.glob(glob)))


N_FRONT_DOCS = count('front/docs/padrao/[0-9]*.md')
N_BACK_DOCS = count('back/docs/arquitetura/*.md')
N_FRONT_SK = count('front/.claude/skills/*/SKILL.md')
N_BACK_SK = count('back/.claude/skills/*/SKILL.md')
N_MD = count('front/**/*.md') + count('back/**/*.md') + count('*.md')

pages = []
add = pages.append

# ------------------------------------------------------------------ capa
add(f'''<section class="cover">
  <div class="cover-sym">{MARK}</div>
  <div class="cover-top"><span class="cover-logo">{MARK}</span><span>Trilho · padrão de construção de sistemas</span></div>
  <div class="cover-main">
    <span class="kicker">Manual do padrão</span>
    <h1>Trilho<em>Sistemas de áreas diferentes, com a mesma arquitetura e a mesma cara.</em></h1>
    <p>Como funcionam os arquivos orientadores e as skills para agentes de codificação, e como os sistemas saem depois de construídos com eles. Com telas do Fibro+ e do Urban Pass.</p>
  </div>
  <div class="cover-levels">
    <div class="lv">{ic('server')}<span>Servidor<br><i>{N_BACK_DOCS} documentos · {N_BACK_SK} skills</i></span></div>
    <div class="lv">{ic('app-window')}<span>Interface<br><i>{N_FRONT_DOCS} documentos · {N_FRONT_SK} skills</i></span></div>
    <div class="lv">{ic('message-square-text')}<span>Você<br><i>só o negócio, em linguagem natural</i></span></div>
  </div>
  <div class="cover-foot"><span>Kurt Pohling</span><span>Versão 1 · novembro de 2026</span></div>
</section>''')

# ------------------------------------------------------------------ antes de começar
toc = [
    ('1', 'A ideia', 'O que você decide, o que o kit decide e de onde o padrão veio.'),
    ('2', 'Como o sistema sai', 'As telas que todo projeto ganha: casca, lista, modal com abas, formulário, guia, auditoria.'),
    ('3', 'O que o servidor garante', 'A arquitetura modular e o contrato que a API entrega para a tela.'),
    ('4', 'Os arquivos e as skills', 'O que vai em cada repositório e o que cada skill faz.'),
    ('5', 'Como usar', 'O caminho de um projeto novo, exemplos de pedidos e os limites do kit.'),
    ('A', 'Apêndices', 'As 20 leis do painel, as 16 regras do servidor e a lista de conferência.'),
]
add(f'''<section class="page-flow">
{chapter('00', 'Antes de começar', 'O que é este material e como ler.', 'book-open')}
{p('O <b>Trilho</b> é um conjunto de arquivos em Markdown (<code>AGENTS.md</code>, <code>CLAUDE.md</code>, documentos de apoio e skills) que se copia para dentro de um projeto. Com eles, um agente de codificação constrói o sistema seguindo sempre a mesma arquitetura no servidor e a mesma lógica visual na interface. Você descreve o negócio; o agente não precisa perguntar como deve ser uma lista, um detalhe ou um formulário.')}
{p('O padrão não foi inventado para este manual. Ele foi extraído de dois sistemas que já existem: o <b>Urban Pass</b> (gestão de manutenção urbana, em React) e o <b>Fibro+</b> (acompanhamento de pessoas com fibromialgia, em Angular). As telas mostradas aqui são desses dois sistemas.')}
{stats([(N_MD, 'arquivos Markdown no kit'), (N_FRONT_SK + N_BACK_SK, 'skills para os agentes'), (20, 'leis do painel'), (16, 'regras do servidor')])}
{note('As telas do Fibro+ usam dados fictícios criados para documentação. As do Urban Pass vêm do ambiente de testes e ainda mostram o nome antigo do produto, <b>Safari Urbano</b>. Cada figura traz um selo dizendo de qual sistema é.', 'lock', 'Sobre as capturas.')}
{h3('Como ler')}
<div class="legend">
  <div>{ic('scale')}<p><b>Lei</b>: uma regra do padrão, com o motivo. As leis estão nos arquivos que o agente lê.</p></div>
  <div>{ic('image')}<p><b>Tela</b>: como a regra aparece num sistema de verdade.</p></div>
  <div>{ic('message-square-text')}<p><b>Pedido</b>: um exemplo do que você escreve, em linguagem natural.</p></div>
  <div>{ic('wand-sparkles')}<p><b>O que sai</b>: o que o agente entrega sem você precisar pedir.</p></div>
</div>
{h3('Partes')}
<table class="toc">{''.join(f'<tr><td class="n">{n}</td><td><b>{E(t)}</b><span>{E(d)}</span></td></tr>' for n, t, d in toc)}</table>
</section>''')

# ------------------------------------------------------------------ parte 1
add(part(1, 'A ideia', 'Você cuida do que só você sabe: o negócio. O que é igual em todo sistema já está decidido e escrito.', 'compass', 'charcoal'))
add(f'''<section class="page-flow">
{chapter('1.1', 'Quem decide o quê', 'A divisão de trabalho que o kit impõe.', 'scale')}
{diag('d2-quem-decide', 'O lado direito é o conteúdo do kit. O lado esquerdo é o que o agente pergunta a você, e só isso.', 78)}
{p('Sem o kit, cada pedido de tela vira uma conversa sobre aparência: onde fica o botão, se abre modal ou página, que cor tem o status. Com o kit, essas respostas estão nos arquivos que o agente lê antes de escrever. O que sobra para a conversa é o que muda de um produto para outro.')}
{note('Em todo arquivo do kit vale a mesma instrução: faltou uma <b>decisão de produto</b>, o agente para e pergunta uma vez, com opções. Faltou uma <b>decisão de tela</b>, ele consulta o padrão e não pergunta.', 'tip', 'A regra de conversa.')}
{chapter('1.2', 'Do pedido ao sistema pronto', 'As cinco etapas de um projeto novo.', 'route')}
{diag('d1-do-pedido-ao-sistema', 'Cada etapa tem uma skill que a conduz. O detalhe de cada uma está na Parte 5.', 62)}
</section>''')
add(f'''<section class="page-flow">
{chapter('1.3', 'De onde o padrão veio', 'Quatro camadas, cada uma vinda de um trabalho real.', 'history')}
{diag('d4-origem', 'O kit não acrescenta ideia nova: ele registra o que os dois sistemas já fazem.', 66)}
{cards([
    ('ruler', 'Especificação visual', 'O ponto de partida: papéis de cor (neutros, marca, quatro estados), anatomia dos componentes e o fluxo lista, modal, edição. É um documento privado; o que valia dele está reescrito no padrão.'),
    ('boxes', 'Template modular', 'A arquitetura do servidor: módulos com fronteira que um teste protege, tenant automático, auditoria, ciclo de entrega com relatório. É um repositório público: <code>github.com/Kzrtt/laravel-modular-template</code>.'),
    ('map', 'Urban Pass', 'Trouxe o guia de tela no topo das áreas complexas, a tabela que vira cartões no celular e o motor de cadastros em React.'),
    ('heart-handshake', 'Fibro+', 'A versão mais completa: aba para cada relação, edição de todos os campos, nunca mostrar ID, selos iguais em toda tela, console de dados do Admin.'),
], 2)}
{note('O Fibro+ continua sendo a referência. Quando algo muda lá e vale para todos os projetos, a mudança sobe para o kit, no documento do assunto, como regra com o motivo.', 'info', 'Como o kit se mantém vivo.')}
</section>''')

# ------------------------------------------------------------------ parte 2
add(part(2, 'Como o sistema sai', 'As telas que todo projeto ganha, mostradas em dois sistemas de áreas diferentes: saúde e manutenção urbana.', 'app-window', 'sand'))
add(f'''<section class="page-flow">
{chapter('2.1', 'A casca', 'Topo, menu lateral e palco. Igual em todas as telas.', 'panels-top-left')}
{row(shot('fb-adm-painel', 'Painel do Admin: topo escuro, menu em seções, palco em cartão claro sobre fundo areia.', 'half'),
     shot('up-painel', 'O mesmo esqueleto em outro produto, com outra marca e outro framework.', 'half'))}
{bullets([
    '<b>Topo</b> escuro com o logo, o nome do sistema e a pílula do perfil (nome, nível, trocar senha, sair).',
    '<b>Menu</b> em acordeão de seção única, gerado de uma definição só e filtrado por permissão. O que o nível não pode abrir não aparece.',
    '<b>Palco</b>: um cartão claro com o título da área, uma linha de descrição e o único botão colorido da tela.',
    'Abaixo de 900 px o menu vira uma gaveta que abre pela esquerda.',
])}
{row(shot('fb-adm-menu-aberto', 'Seção aberta: itens ligados por uma linha, item atual marcado.', 'half', 58),
     f'<div>{h3("O que a casca nunca tem")}{bullets(["Sombra em item de menu.", "Faixa colorida na lateral de cartão ou item.", "Tabela-filha como item de menu: ela se edita dentro do registro pai.", "Mais de um botão colorido por tela."])}</div>')}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.2', 'A lista', 'Serve para achar e reconhecer um registro. Ver e agir é no modal.', 'table-2')}
{shot('fb-adm-tela-patients', 'Lista de pacientes: guia no topo, busca com filtros, coluna principal em duas linhas, vínculos em etiquetas, situação em selo, seta que abre o detalhe.', 'wide', 96)}
{row(f'<div>{h3("O que toda lista tem")}{bullets(["Busca ao vivo por nome (sem diferenciar acento) e por documento.", "Filtros num modal, com um seletor por filtro.", "Ordenação pelo título da coluna.", "Paginação com escolha de tamanho.", "Textos próprios para vazio, carregando e erro.", "No celular, cada linha vira um cartão."])}</div>',
     f'<div>{h3("O que não se vê, mas está lá")}{bullets(["Busca, ordem e página rodam <b>no servidor</b>.", "O estado da lista mora no <b>endereço da página</b>: o link de um colega abre a mesma busca, na mesma página.", "A linha do registro que acabou de ser aberto fica marcada ao voltar.", "Nenhuma coluna de identificador."])}</div>')}
{shot('up-destinos-lista', 'Uma lista do Urban Pass: mesma barra, mesma tabela, mesma paginação.', 'wide', 56)}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.3', 'O modal de detalhe', 'O centro do sistema: resumo, ações, todos os dados e tudo o que está ligado ao registro.', 'square-pen')}
{diag('d3-lista-modal-edicao', 'Não existe edição dentro da tabela nem página só para ver um registro.', 50)}
{shot('fb-inst-unidade-modal', 'Detalhe de uma unidade. Em cima, a ficha (ícone, tipo, selos, nome, resumo) e os botões. Depois as abas. Embaixo, os dados em seções por tema, no mesmo desenho do formulário.', 'wide', 84)}
{table(['Parte', 'Regra'], [
    ['Ficha', 'Ícone do tipo de registro, selos de estado, o nome que a pessoa reconhece e de 2 a 4 dados de resumo.'],
    ['Botões', 'A ação destrutiva em vermelho discreto e <b>Editar</b> como o único botão colorido.'],
    ['Faixa de ações', 'Todas as outras ações, sempre em cinza, qualquer que seja o assunto.'],
    ['Abas', 'A primeira é Dados; depois, uma para cada tipo de registro relacionado.'],
    ['Corpo', 'Seções por tema, grade de 12 colunas. É a única parte que rola. O modal não tem rodapé.'],
])}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.4', 'Relação vira aba', 'Dá para andar pelo sistema inteiro sem sair do lugar.', 'link')}
{row(shot('fb-inst-unidade-usuar', 'Unidade › aba Usuários: a lista de usuários, filtrada por esta unidade.', 'half'),
     shot('fb-inst-paciente-modal-crede', 'Paciente › aba Credenciamentos. A linha abre o modal daquele registro.', 'half'))}
{p('Para cada tabela que aponta para o registro aberto, o modal ganha uma aba. A aba é a lista normal daquele outro recurso, com o filtro pelo registro aberto, a mesma tabela, a mesma paginação e a permissão daquela lista. Quem não pode ver a lista não vê a aba.')}
{row(shot('fb-adm-condicoes-nive', 'Lista-filha: os níveis só existem dentro da condição e são editados no próprio lugar.', 'half'),
     shot('up-destinos-detalhe', 'No Urban Pass, a ação curta abre um diálogo de formulário sobre a tela.', 'half'))}
{note('Qualquer menção a um registro, em qualquer tela (uma etiqueta numa lista, a linha de uma aba, um item da auditoria), leva ao <b>modal</b> dele, e não a uma página.', 'info', 'Regra de link.')}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.5', 'O modal mostra tudo', 'Todas as colunas da tabela aparecem no detalhe, cada uma na seção do seu assunto.', 'list-checks')}
{diag('d7-certo-errado', 'A correção mais repetida durante a construção do Fibro+. No kit ela é lei, com skill própria para conferir.', 80)}
{p('A conferência é feita em três pontos: as colunas da tabela no banco, as chaves que a API devolve e os campos do modal. A falta pode estar na API, que deixou de devolver uma data ou o nome de um vínculo. Nesse caso o agente da interface <b>pede o campo</b> ao servidor, em vez de contornar.')}
{row(shot('fb-inst-paciente-modal', 'Paciente: identificação, contato, vínculo, credenciamento, registro.', 'half'),
     shot('fb-adm-entidades-modal', 'Entidade: o mesmo desenho numa tabela de outro assunto.', 'half'))}
{bullets(['Ficam de fora só segredos (senha, token) e a data de exclusão.', 'Toda ficha termina com a seção <b>Registro</b>: criado em, última alteração e, se houver, por quem.', 'Seção nova só quando nenhuma das existentes serve, e com nome de tema.'])}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.6', 'Tudo se edita', 'Toda coluna é editável por quem tem permissão, menos a chave, as datas de controle e os segredos.', 'pencil')}
{row(shot('fb-inst-unidade-nova', 'Formulário: um cartão por grupo, com os mesmos nomes das seções do detalhe.', 'half'),
     shot('up-oficio-novo', 'Cadastro curto no Urban Pass: diálogo de formulário.', 'half'))}
{table(['O dado é', 'O controle é'], [
    ['um vínculo com outro registro', 'campo de relação: busca por nome no servidor. Nunca texto livre, nunca uma lista com centenas de opções.'],
    ['um valor de conjunto fechado', 'seletor com as mesmas palavras dos selos.'],
    ['sim ou não', 'interruptor.'],
    ['um campo que não pode mais mudar', 'aparece travado, com o motivo embaixo.'],
    ['uma senha', 'nunca se mostra nem se edita. A ação é "Redefinir senha".'],
])}
{row(shot('fb-adm-dados-editar', 'Admin › Editar dados: um campo tipado para cada coluna editável do registro, com os vínculos escolhidos por busca.', 'half'),
     f'<div>{h3("O que acontece ao salvar")}{bullets(["Vai para o servidor <b>só o que mudou</b>.", "O erro de validação aparece embaixo do campo, com a mensagem do servidor.", "Sair com alteração não salva pergunta antes.", "A mudança fica na auditoria, com antes e depois."])}</div>')}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.7', 'O vocabulário visual', 'A mesma informação tem a mesma cara em toda tela.', 'tags')}
<table class="badges">
<tr><th>Estado</th><td>{chips(('Ativa', 'success'), ('Pendente', 'warning'), ('Recusado', 'error'), ('Em análise', 'info'), ('Arquivado', 'neutral'))}<span class="small"> selo: cor, ícone e texto, vindos de um mapa central</span></td></tr>
<tr><th>Coisa</th><td>{chips(('UBS Centro', 'ref'), ('Prefeitura de Beltrão', 'ref'), ('***.456.789-**', 'code'), ('UBSC', 'code'))}<span class="small"> etiqueta: registro vinculado pelo nome; código em letra fixa</span></td></tr>
<tr><th>Data</th><td><span class="plain">12/03/2026 · 12/03/2026 14:30</span></td></tr>
<tr><th>Texto de alguém</th><td><span class="quote">“Paciente mudou de bairro.”</span><span class="small"> motivo e observação aparecem como citação</span></td></tr>
<tr><th>Vazio</th><td><span class="plain muted">—</span></td></tr>
</table>
{row(f'<div>{h3("Nunca um identificador")}{p("Em nenhum lugar da interface aparece o código interno de um registro. No lugar dele vai um nome útil. Registro que não tem nome próprio recebe um nome composto, como <i>Dra. Ana · UBS Centro</i>. Sem dado nenhum, aparece <i>Registro sem nome</i>.")}{p("Antes de cada entrega, um roteiro automático abre todas as telas, o primeiro registro de cada lista e cada aba, e procura texto com cara de identificador. O resultado esperado é zero.")}</div>',
     f'<div>{h3("A mesma palavra em toda tela")}{p("Cada vocabulário (situações, níveis, tipos, ações) tem um mapa só, que diz a palavra em português, a cor e o ícone. Lista, modal, auditoria e painel leem o mesmo mapa. Valor que não está no mapa sai cinza, e isso avisa que falta acrescentá-lo.")}{p("Nome de coluna do banco e valor em inglês nunca chegam à tela.")}</div>')}
{shot('fb-adm-tela-cadastros-units', 'Unidades no Fibro+: códigos em letra fixa, entidade como etiqueta, situação como selo.', 'wide', 74)}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.8', 'O guia de tela', 'Tela com regra de negócio abre com um tutorial em passos.', 'info')}
{shot('up-fila-guia', 'Fila de ocorrências do Urban Pass. O passo escolhido mostra a explicação e destaca a parte da tela de que ele fala (o contorno na tabela).', 'wide', 100)}
{row(f'<div>{h3("Quando a tela ganha guia")}{bullets(["Há mais de uma ação que muda o estado do registro.", "Existe uma ordem certa de fazer as coisas.", "Uma ação tem consequência que não se vê na hora.", "Um colega novo precisaria de alguém ao lado."])}</div>',
     f'<div>{h3("Como é escrito")}{bullets(["De 3 a 6 passos; título de até quatro palavras.", "Texto de uma a três frases: o que fazer e <b>o que acontece depois</b>.", "As mesmas palavras dos botões da tela.", "Mudou a regra de negócio, o guia muda na mesma entrega."])}</div>')}
{row(shot('fb-gs-fila', 'Fibro+: guia e, logo abaixo, a linha do tempo das etapas, que também filtra a lista.', 'half'),
     shot('up-quadro', 'Urban Pass: o guia explica o ciclo de vida das colunas do quadro.', 'half'))}
{note('"Entendi, esconder" recolhe o guia, e a escolha é lembrada por tela. No lugar fica o botão "Como funciona esta tela".', 'tip')}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.9', 'Fluxos de trabalho', 'Fila, decisão, emissão: telas próprias, feitas com as mesmas peças.', 'workflow')}
{row(shot('fb-gs-fila-modal', 'Credenciamento: o modal traz os dados, os documentos enviados e as ações da etapa.', 'half'),
     shot('fb-gs-fila-decisao', 'A decisão: aprovar, pedir ajustes ou não aprovar, com os campos de cada caso.', 'half'))}
{row(shot('up-rejeitar', 'Encerrar sem obra pede o motivo. O botão repete o verbo da ação.', 'half'),
     shot('up-saida-passos', 'Tarefa em etapas: passos numerados, um de cada vez.', 'half'))}
{table(['Situação', 'O que o padrão manda'], [
    ['Ação destrutiva, em massa, sem volta ou que avisa alguém', 'Confirmação que diz o efeito, com números. Cancelar à esquerda, confirmar à direita.'],
    ['Recusa ou encerramento', 'Motivo obrigatório.'],
    ['Deu certo', 'Aviso curto que some sozinho.'],
    ['Resultado que a pessoa precisa guardar', 'Diálogo que só fecha por ação, com botão de copiar.'],
    ['Mudança de estado', 'Acontece por ação (Aprovar, Encerrar), que roda as regras. Não por um campo de situação.'],
])}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.10', 'Níveis de acesso e o Admin', 'Cada nível vê só o que pode fazer. O nível mais alto vê e corrige tudo, dentro das telas normais.', 'shield-check')}
{row(shot('fb-adm-usuario-modal', 'Conta de usuário: a pessoa (operador), o nível, as unidades, e as ações do Admin na faixa.', 'half'),
     shot('fb-inst-usuario-permissoes', 'Permissões da conta, por grupo.', 'half'))}
{row(shot('fb-inst-usuario-criar', 'Criar conta: o nível é escolhido entre os que a pessoa pode criar.', 'half'),
     shot('up-senha-temp', 'A senha provisória aparece uma única vez, com botão de copiar.', 'half'))}
{table(['Poder do nível mais alto', 'Onde aparece'], [
    ['Ver todas as entidades', 'Filtro e coluna de entidade nas listas.'],
    ['Ver excluídos', 'Alternador ao lado de "Atualizar lista".'],
    ['Editar dados (todas as colunas)', 'Botão na faixa de ações de todo modal.'],
    ['Excluir e restaurar em cascata', 'Mesma faixa, com prévia do que será afetado e do que fica.'],
    ['Entrar como outra conta', 'Faixa de ações do modal da conta; sessão temporária em outra aba.'],
])}
{row(shot('fb-med-motivo', 'Dado sensível: a tela pede o motivo antes de buscar qualquer coisa.', 'half'),
     shot('fb-gs-redefinir-senha', 'Redefinir senha: confirmação que explica o efeito.', 'half'))}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.11', 'Auditoria', 'Quem fez o quê, quando, e o que mudou.', 'scroll-text')}
{shot('fb-adm-tela-audit', 'Auditoria no Fibro+: quem (pessoa e login), a ação em selo, a tabela pelo nome em português e o registro pelo nome, nunca pelo identificador.', 'wide', 92)}
{row(shot('fb-inst-auditoria-modal', 'O detalhe mostra só os campos que mudaram: antes e depois.', 'half'),
     shot('up-auditoria', 'A mesma tela no Urban Pass.', 'half'))}
{bullets([
    'Toda alteração é gravada sozinha, com a conta <b>e a pessoa</b> que a usava naquele momento.',
    'Conteúdo sensível não entra na trilha: fica registrado que a ação aconteceu, sem o conteúdo.',
    'A trilha é só leitura. Ninguém edita nem apaga, nem o nível mais alto.',
    'Cada modal de registro pode ter a aba <b>Atividade</b>, com a trilha daquele registro.',
])}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.12', 'No celular', 'O painel é pensado para o computador e funciona inteiro no telefone.', 'smartphone')}
{row(shot('up-m-fila', 'Guia com os passos quebrando de linha; filtros empilhados.', 'phone'),
     shot('up-m-lista', 'A tabela vira cartões: cada célula com o seu rótulo.', 'phone'),
     shot('up-m-quadro', 'Quadro de etapas em coluna única.', 'phone'), cls='row phones')}
{row(f'<div>{h3("Regras")}{bullets(["Só rolagem vertical. Rolagem lateral é tratada como defeito.", "Abas e passos quebram de linha; nunca rolam de lado.", "O menu vira gaveta, pela esquerda.", "Tudo o que se faz arrastando tem um botão equivalente."])}</div>',
     f'<div>{h3("Acessibilidade")}{bullets(["Foco sempre visível; tudo alcançável pelo teclado.", "O modal prende o foco, fecha no Esc e devolve o foco a quem abriu.", "Estado nunca só por cor: cor, ícone e texto.", "Toda animação se desliga para quem pede movimento reduzido."])}</div>')}
</section>''')
add(f'''<section class="page-flow">
{chapter('2.13', 'As cores', 'Base fixa em charcoal e sand. Cada projeto escolhe duas cores de realce.', 'palette')}
<div class="swatches">
  <div><i style="background:#1e1e1c"></i><b>Charcoal</b><span>#1E1E1C · topo, menu, texto</span></div>
  <div><i style="background:#d8cbb3"></i><b>Sand</b><span>#D8CBB3 · fundo da página</span></div>
  <div><i style="background:#fbf9f4;border:.3mm solid #ded3bd"></i><b>Creme</b><span>#FBF9F4 · cartões</span></div>
  <div><i style="background:var(--a1)"></i><b>Realce 1</b><span>a ação principal</span></div>
  <div><i style="background:var(--a2)"></i><b>Realce 2</b><span>o detalhe que chama o olho</span></div>
</div>
{table(['Projeto', 'Realce 1 (ação)', 'Realce 2 (detalhe)'], [
    ['Fibro+', '<span class="dotc" style="background:#1b6b38"></span> verde #1B6B38', '<span class="dotc" style="background:#ee6e93"></span> rosa #EE6E93'],
    ['Urban Pass', '<span class="dotc" style="background:#5b6b21"></span> oliva #5B6B21', '<span class="dotc" style="background:#b04a19"></span> laranja #B04A19'],
    ['Padrão do kit (e deste manual)', '<span class="dotc" style="background:#1f5e63"></span> petróleo #1F5E63', '<span class="dotc" style="background:#c8643a"></span> cobre #C8643A'],
])}
{row(f'<div>{h3("Onde a cor entra")}{bullets(["<b>Realce 1</b>: o único botão principal da tela, o item atual do menu, as barras de um gráfico.", "<b>Realce 2</b>: o ponto do item atual, o contador de pendências, o pico de um gráfico.", "<b>Estados</b>: verde, âmbar, vermelho e azul, só em selos e avisos.", "Todo o resto é neutro."])}</div>',
     f'<div>{h3("O que não se faz")}{bullets(["Cor diferente por assunto: a cor deixaria de significar estado.", "Realce em borda de cartão ou faixa lateral.", "Branco puro em cartão ou preto puro em texto.", "Valor de cor solto no código: tudo vem de variáveis."])}</div>')}
{note('A skill <code>/identidade</code> recebe as duas cores, calcula os tons de cada uma, confere o contraste e mostra as telas de demonstração para aprovação antes de qualquer tela ser escrita.', 'tip')}
</section>''')

# ------------------------------------------------------------------ parte 3
add(part(3, 'O que o servidor garante', 'O padrão visual só fecha se a API devolver o que a tela precisa. Esse acordo está escrito dos dois lados.', 'server', 'charcoal'))
add(f'''<section class="page-flow">
{chapter('3.1', 'As camadas', 'A arquitetura modular por baixo e, por cima, o contrato com a tela.', 'layers')}
{diag('d6-camadas-do-servidor', 'As três camadas de cima são o que este kit acrescenta ao template modular.', 76)}
{cards([
    ('boxes', 'Módulos', 'O domínio é dividido por capacidade de negócio. Um módulo nunca importa a classe interna de outro; eles conversam por contratos e eventos. Um teste de arquitetura quebra a entrega se a fronteira for furada.'),
    ('database', 'Dados', 'Um arquivo só lista todos os vínculos entre tabelas. Dele saem as chaves do banco, a exclusão em cascata e as abas da tela genérica. Nada se apaga de verdade.'),
    ('user-cog', 'Contas e auditoria', 'Nível, permissão e recorte. A conta é o login; o operador é a pessoa. Toda linha de auditoria grava os dois.'),
    ('plug', 'Contrato do painel', 'Lista paginada no servidor com contagens, detalhe com todas as colunas, nome no lugar de identificador, vínculo validado.'),
], 2)}
</section>''')
add(f'''<section class="page-flow">
{chapter('3.2', 'O contrato com a tela', 'O que cada lei do painel exige da API.', 'cable')}
{table(['A tela precisa', 'A API entrega'], [
    ['Lista com busca, ordem, página e contagens por etapa', 'Um contrato único de listagem: página, tamanho (até 100), busca sem acento, ordem só por campos permitidos, contagens por situação.'],
    ['Modal com todos os campos', 'O detalhe devolve todas as colunas visíveis, as datas de controle e o nome de cada vínculo. Um teste por recurso garante.'],
    ['Nunca mostrar identificador', 'Todo lugar que cita outro registro traz o nome junto. A auditoria devolve o nome do registro e dos vínculos do antes e depois.'],
    ['Vínculo escolhido por busca', 'Uma consulta de opções por nome (até 30, só ativos). Na gravação, o vínculo precisa existir, estar ativo e ser do mesmo cliente.'],
    ['Aba de relação', 'A lista do recurso relacionado aceita o filtro pelo registro pai, com o mesmo recorte e a mesma permissão.'],
    ['Arquivar com aviso', 'O detalhe traz quantos registros usam aquele cadastro. Arquivar e restaurar podem ser repetidos sem efeito colateral.'],
    ['Excluir com prévia', 'A prévia lista cada tabela afetada e o que fica. Se o total mudou até a confirmação, a exclusão é recusada.'],
    ['Erro embaixo do campo', 'Mensagens em português, com as chaves iguais aos nomes dos campos.'],
])}
{note('Quando a interface precisa de algo que a API não devolve, o agente escreve um pedido com a tela, a lei, o endpoint e o campo. Quando a API muda o que a tela vê, o relatório da entrega traz a seção <b>Para o front</b>.', 'info', 'Dois repositórios, um acordo.')}
{chapter('3.3', 'O batimento', 'Toda mudança segue o mesmo ritual.', 'refresh-cw')}
{diag('d5-batimento', 'O relatório de cada entrega é uma fotografia datada. A documentação viva é atualizada a partir deles.', 92)}
</section>''')

# ------------------------------------------------------------------ parte 4
front_docs = [
    ('00', 'Princípios', 'Por que o padrão é assim; o fluxo lista, modal, edição; o que já foi decidido.'),
    ('01', 'Tokens', 'Papéis de cor, a folha de variáveis, tipografia, medidas.'),
    ('02', 'Casca', 'Topo, menu em acordeão, perfil, gaveta.'),
    ('03', 'Listagem', 'Busca, filtros, tabela, paginação, estados da linha.'),
    ('04', 'Modal de detalhe', 'Ficha, ações, abas de relação, leitura em seções.'),
    ('05', 'Formulário', 'Cartões por grupo, grade de 12, controles, validação.'),
    ('06', 'Vocabulário visual', 'Selo, etiqueta, data, citação; nunca ID.'),
    ('07', 'Guia de tela', 'Quando usar, anatomia, como escrever.'),
    ('08', 'Cadastros declarativos', 'Uma configuração vira lista, detalhe e formulário.'),
    ('09', 'Acesso e menu', 'Níveis, permissões, poderes do Admin.'),
    ('10', 'Feedback e estados', 'Confirmação, sucesso, erro, vazio, carregando.'),
    ('11', 'Responsivo e acessibilidade', 'Celular, teclado, contraste, movimento.'),
    ('12', 'Painel e auditoria', 'Tela inicial, auditoria e login.'),
    ('13', 'Contrato com a API', 'O que a tela espera do servidor.'),
    ('14', 'Peças por framework', 'O kit de componentes em Angular e em React.'),
    ('15', 'Verificação', 'A lista de conferência e as varreduras.'),
]
back_docs = [
    ('ARQUITETURA', 'O paradigma modular, o tenant automático, o fluxo canônico.'),
    ('MODULOS · CORE · COMUNICACAO · FRONTEIRAS', 'O pacote de módulos, o núcleo compartilhado, contratos e eventos, o teste de arquitetura.'),
    ('IMPLEMENTACAO · BANCO · CODE_STYLE', 'Respostas práticas de código, convenções de tabela, estilo.'),
    ('PAINEL', '<b>Novo.</b> O contrato que a API entrega para a tela.'),
    ('DADOS', '<b>Novo.</b> Mapa de vínculos, chaves, exclusão em cascata, console de dados.'),
    ('CONTAS_E_AUDITORIA', '<b>Novo.</b> Níveis, conta e operador, auditoria com responsável, leitura sensível.'),
]
add(part(4, 'Os arquivos e as skills', 'O que se copia para cada repositório e o que cada skill faz quando é chamada.', 'folder-tree', 'sand'))
add(f'''<section class="page-flow">
{chapter('4.1', 'O que vai em cada repositório', 'Duas pastas no kit: uma para a interface, outra para o servidor.', 'folder')}
<div class="tree">
<pre>trilho/
├─ <b>front/</b>                      interface, qualquer framework
│  ├─ AGENTS.md  CLAUDE.md      as 20 leis, a ordem de leitura, a definição de pronto
│  ├─ docs/padrao/              {N_FRONT_DOCS} documentos do padrão
│  └─ .claude/skills/           {N_FRONT_SK} skills
├─ <b>back/</b>                       servidor (Laravel modular)
│  ├─ CLAUDE.md  AGENTS.md      as 16 regras, o mapa de pastas, o ciclo de entrega
│  ├─ docs/arquitetura/         {N_BACK_DOCS} documentos
│  ├─ docs/dominio/  docs/reports/   contratos dos documentos de negócio e dos relatórios
│  └─ .claude/skills/           {N_BACK_SK} skills
├─ <b>manual/</b>                     este manual e o que o gera
└─ README.md  COMO_USAR.md  PROMPTS.md</pre>
</div>
{note('<code>AGENTS.md</code> é o arquivo que a maioria dos agentes lê (Codex, OpenCode, Cursor). <code>CLAUDE.md</code> é o do Claude Code. No kit, um aponta para o outro, e as regras ficam num lugar só. As skills são arquivos Markdown: um agente sem suporte a skills lê o arquivo e segue os passos.', 'info')}
{h3('Interface: os documentos do padrão')}
{table(['Nº', 'Documento', 'Responde'], [[n, f'<b>{E(t)}</b>', E(d)] for n, t, d in front_docs], 'grid tight')}
</section>''')
add(f'''<section class="page-flow">
{h3('Servidor: os documentos de arquitetura')}
{table(['Documento', 'Conteúdo'], [[f'<code>{E(n)}</code>', d] for n, d in back_docs], 'grid tight')}
{chapter('4.2', 'As skills da interface', 'Cada skill é um roteiro que o agente segue do começo ao fim.', 'wand-sparkles')}
{cards([
    ('palette', '/identidade', 'A primeira de um projeto. Entrevista curta (nome, logo, duas cores, níveis, menu), gera as variáveis de cor, monta a casca e pede o aceite da paleta.'),
    ('table-2', '/novo-cadastro', 'Tabela com lista, detalhe e formulário. Sai um arquivo de configuração: todas as colunas no detalhe, todas as editáveis no formulário, uma aba por relação.'),
    ('workflow', '/nova-tela', 'Tela com comportamento próprio: fila, quadro, assistente. Primeiro procura se já existe uma tela do assunto para estender.'),
    ('list-checks', '/auditar-detalhe', 'Compara banco, API e tela. Encaixa cada campo que falta na seção existente e varre a interface atrás de identificadores.'),
    ('info', '/guia-de-tela', 'Escreve o tutorial do topo: título, de 3 a 6 passos, texto com a consequência de cada ação, e a parte da tela que cada passo destaca.'),
    ('camera', '/revisao-visual', 'Antes de entregar: testes, capturas em dois tamanhos, varreduras, entrada com cada nível, e o relato do que foi conferido.'),
], 3)}
{chapter('4.3', 'As skills do servidor', 'Cinco vêm do template modular; duas são novas.', 'terminal')}
{cards([
    ('notebook-pen', '/prontuario', 'Entrevista o dono do produto e gera os documentos de negócio, os níveis de acesso, o glossário e os módulos.'),
    ('book-open', '/dominio', 'Carrega as regras de negócio da área antes de responder ou planejar.'),
    ('git-branch', '/nova-feature', 'O ciclo completo: contexto, código com teste, conferência, relatório.'),
    ('refresh-cw', '/sync-docs', 'Leva os relatórios pendentes para a documentação viva.'),
    ('box', '/novo-modulo', 'Cria um módulo com todas as convenções.'),
    ('database', '/nova-tabela', '<b>Nova.</b> Toda tabela ou vínculo novo: convenções, mapa de vínculos, nome legível, auditoria, testes de guarda.'),
    ('plug', '/novo-recurso-admin', '<b>Nova.</b> Expõe uma tabela ao painel no contrato único e escreve o aviso para a interface.'),
], 3)}
{chapter('4.4', 'Qual skill para qual pedido', 'Você não precisa chamar a skill pelo nome: o agente escolhe pela descrição do pedido. Exemplos completos em PROMPTS.md.', 'compass')}
{table(['Você pede', 'Servidor', 'Interface'], [
    ['Um sistema novo', '<code>/prontuario</code>', '<code>/identidade</code>'],
    ['Uma coisa nova para cadastrar', '<code>/nova-tabela</code> e <code>/novo-recurso-admin</code>', '<code>/novo-cadastro</code>'],
    ['Um fluxo com etapas e decisão', '<code>/nova-feature</code>', '<code>/nova-tela</code> e <code>/guia-de-tela</code>'],
    ['Um dado a mais num registro', '<code>/nova-feature</code>', 'o campo entra na seção existente'],
    ['Falta um dado no modal; apareceu um código', 'devolver o campo e o nome', '<code>/auditar-detalhe</code>'],
    ['Uma regra que mudou', '<code>/nova-feature</code>', 'o guia de tela muda junto'],
    ['Conferir antes de mostrar a alguém', '<code>/sync-docs</code>', '<code>/revisao-visual</code>'],
])}
</section>''')

# ------------------------------------------------------------------ parte 5
add(part(5, 'Como usar', 'O caminho de um projeto novo, exemplos de pedidos e o que o kit não faz.', 'rocket', 'charcoal'))
add(f'''<section class="page-flow">
{chapter('5.1', 'O caminho de um projeto novo', 'Sete passos, cada um com a sua skill.', 'route')}
{steps([
    ('Copie os arquivos', 'A API parte do <code>laravel-modular-template</code>. O conteúdo de <code>back/</code> vai para o repositório da API e o de <code>front/</code> para o da interface. O arquivo <code>COMO_USAR.md</code> diz o que não sobrescrever num projeto que já existe.'),
    ('Rode /prontuario na API', 'Você responde à entrevista: o que o sistema faz, as coisas do negócio e seus estados, quem pode o quê, os números. Saem os documentos de negócio, os níveis e o glossário.'),
    ('Descreva tabelas e regras', 'Com <code>/nova-feature</code>, o agente cria módulos, tabelas e recursos do painel. Cada entrega fecha com um relatório que tem a seção "Para o front".'),
    ('Rode /identidade na interface', 'Nome, logo e as duas cores de realce. O agente monta a casca e mostra as telas de demonstração para você aprovar a paleta.'),
    ('Peça os cadastros', 'Para cada tabela simples, <code>/novo-cadastro</code>: lista, modal com abas e formulário saem de um arquivo de configuração.'),
    ('Peça os fluxos', 'Para o que tem regra (fila, aprovação, emissão), <code>/nova-tela</code> e <code>/guia-de-tela</code>.'),
    ('Revise', '<code>/revisao-visual</code> na interface e <code>/sync-docs</code> na API. De tempos em tempos, <code>/auditar-detalhe</code>.'),
])}
{row(f'<div>{h3("O que você precisa dizer")}{bullets(["O que o sistema faz e para quem.", "As coisas do negócio e os estados de cada uma.", "Quem pode o quê.", "Os números: prazos, limites, percentuais.", "Como você chama cada coisa."])}</div>',
     f'<div>{h3("O que você não precisa dizer")}{bullets(["Que a lista tem busca, paginação e filtros.", "Que o detalhe abre em modal, com abas.", "Que o status é um selo e o vínculo mostra o nome.", "Que a exclusão pede confirmação.", "Que precisa funcionar no celular e em português."])}</div>')}
</section>''')
add(f'''<section class="page-flow">
{chapter('5.2', 'Pedidos em linguagem natural', 'O que você escreve e o que sai. Os exemplos são de um sistema hipotético de pedidos de poda de árvore.', 'message-square-text')}
{ask('Preciso cadastrar as equipes de poda: nome, encarregado, telefone, quantas pessoas e se tem caminhão cesto. Cada equipe é de uma regional.',
     'Item <b>Equipes</b> no menu Cadastros. Lista com a equipe e a regional em etiqueta. Modal com Identificação, Contato, Estrutura e Registro, e as abas Pedidos e Atividade. Formulário com a regional escolhida por busca. Arquivar avisa quantos pedidos usam a equipe.')}
{ask('O gestor precisa aprovar os pedidos vistoriados. Ele vê o laudo e as fotos, aprova ou recusa com motivo. O morador é avisado por e-mail nos dois casos.',
     'Tela <b>Aprovação</b> com a linha do tempo (Vistoriados, Aprovados, Recusados), a fila e o modal com laudo e fotos. "Aprovar" e "Recusar" (que pede o motivo), cada um com a confirmação dizendo que o morador será avisado. No topo, o guia "Como aprovar um pedido".')}
{ask('No pedido, quero guardar também a espécie da árvore e a altura estimada.',
     'Os dois campos entram na seção <b>Árvore</b>, que já existe no modal, e no mesmo grupo do formulário. Nenhuma seção nova. O relatório da API avisa a interface dos campos novos.')}
{ask('No modal da equipe não aparece quando ela foi criada, e na lista de pedidos está aparecendo um código esquisito no lugar do nome do fiscal.',
     '<code>/auditar-detalhe</code>: compara banco, API e modal. A causa provável é a API não devolver a data nem o nome do fiscal. O agente corrige no servidor (ou escreve o pedido) e roda a varredura de identificadores em todas as telas.')}
{ask('A vistoria agora vale 60 dias, não 30.',
     'A regra e o teste mudam na API. O texto do guia de tela que citava 30 dias muda <b>na mesma entrega</b>.')}
</section>''')
add(f'''<section class="page-flow">
{chapter('5.3', 'Como saber que ficou pronto', 'Nada é pronto porque compilou.', 'circle-check')}
{cards([
    ('list-checks', 'Testes e build', 'Verificação de tipos, testes e pacote de produção, nessa ordem, um bloqueando o seguinte.'),
    ('camera', 'Capturas olhadas', 'Lista, modal e formulário em 1440×900 e 390×844. O agente olha as imagens antes de dizer que terminou.'),
    ('search', 'Três varreduras', 'Identificador na tela, texto cru (nome de coluna, valor em inglês) e rolagem lateral. As três têm de dar zero.'),
    ('users', 'Cada nível', 'O agente entra com cada nível de acesso e confere menu, botões e abas.'),
    ('file-text', 'Relato', 'O que mudou, o que foi conferido, o que ficou de fora e o que precisa de decisão sua.'),
    ('flag', 'Ressalva declarada', 'O que não está completo vai escrito no relato. Entrega com ressalva escondida é proibida pelos arquivos.'),
], 3)}
{chapter('5.4', 'Limites do kit', 'O que ele não faz, dito com clareza.', 'triangle-alert')}
{table(['Limite', 'O que isso significa na prática'], [
    ['O kit é documentação, não código.', 'Ele não traz os componentes prontos. Em Angular e em React, eles existem no Fibro+ e no Urban Pass e são copiados de lá. Em outro framework, o primeiro projeto precisa construir as peças seguindo os documentos, e isso é trabalho de alguns dias.'],
    ['A parte do servidor está escrita para Laravel modular.', 'As regras do contrato com a tela valem para qualquer servidor, mas as skills e os exemplos citam as peças do template.'],
    ['Agente erra.', 'As regras reduzem o erro e as varreduras o pegam, mas a conferência final das capturas continua valendo a pena, principalmente nas primeiras telas de um projeto.'],
    ['O kit ainda não foi usado num projeto do zero.', 'Ele registra o que dois sistemas já fazem. O primeiro projeto novo vai mostrar o que falta escrever, e o que faltar deve voltar para o kit.'],
    ['Área do usuário final fica de fora.', 'O padrão cobre o painel da equipe. O site público e o aplicativo do usuário final têm identidade própria em cada produto.'],
])}
{h3('Próximos passos que fazem sentido')}
{steps([
    ('Usar num projeto novo, do começo ao fim', 'É o teste que falta. Anote cada pergunta de tela que o agente ainda fizer: cada uma é uma lacuna de um documento.'),
    ('Transformar as peças em ponto de partida', 'Separar do Fibro+ e do Urban Pass a casca, o kit de componentes e o motor de cadastros, num repositório-base por framework. Aí o primeiro dia de um projeto novo já começa com a casca pronta.'),
    ('Levar as peças do servidor para o template', 'A listagem, o motor de cadastros, o mapa de vínculos e a exclusão em cascata hoje vivem no Fibro+. No template modular, todo projeto novo já nasceria com eles.'),
])}
</section>''')

# ------------------------------------------------------------------ apêndices
LAWS = [
    ('Lista → modal → edição', 'Clicar numa linha abre o modal de detalhe. Sem edição na tabela, sem página só para ver.'),
    ('O modal mostra tudo', 'Todas as colunas, em seções por tema. Proibido bloco genérico para o que sobrou.'),
    ('Relação vira aba', 'Uma aba para cada tipo de registro ligado; a linha abre o modal dele.'),
    ('Tudo se edita', 'Menos chave, datas de controle e segredos. O nível mais alto edita e vê tudo.'),
    ('Nunca ID cru', 'No lugar do identificador, um nome útil. Sem nome: "Registro sem nome".'),
    ('Vocabulário fixo é selo; coisa é etiqueta', 'A mesma palavra em toda tela, vinda de um mapa central.'),
    ('Vínculo se escolhe numa lista com busca', 'Nunca texto livre para ligar registros.'),
    ('Cor é exceção', 'Um botão principal por tela. Sem faixa lateral colorida, sem sombra em item de menu.'),
    ('Estado nunca só por cor', 'Sempre cor, ícone e texto.'),
    ('A lista roda no servidor e o estado mora no endereço', 'Página, busca, ordem, filtros, registro aberto e aba.'),
    ('Exclusão é lógica', 'Arquivar e restaurar, com prévia do que será afetado.'),
    ('Tela complexa tem guia no topo', 'A faixa de passos "Como funciona esta tela".'),
    ('Um menu, uma definição', 'Filtrado por permissão. Tabela-filha não ganha item.'),
    ('Integrar ao que existe', 'Dado novo entra na tela e na seção que já tratam do assunto. Nunca uma área paralela.'),
    ('Mensagem pelo serviço de feedback', 'Nada de diálogo do navegador. Erro de validação embaixo do campo.'),
    ('No celular só rola na vertical', 'Tabela vira cartões; abas quebram de linha.'),
    ('Foco visível, teclado, leitor de tela', 'Modal com foco preso, Esc e retorno do foco.'),
    ('Variável, nunca valor solto', 'Toda cor, raio e fonte vem das variáveis do painel.'),
    ('Peça do kit, nunca marcação solta', 'Faltou uma peça? Ela nasce no kit, com teste.'),
    ('Tela em português simples; código em inglês', 'Frases curtas, sem jargão.'),
]
RULES = [
    ('A verdade mora na documentação', 'Em dúvida de negócio, perguntar. Nunca assumir.'),
    ('Uma única camada de dados', 'Sem consulta crua para regra de negócio.'),
    ('Fronteira de módulo é sagrada', 'Lógica em Actions; controladores finos; contratos e eventos entre módulos.'),
    ('Multi-cliente sempre', 'Recorte automático; contexto restaurado em tarefas em segundo plano.'),
    ('Tipagem estrita em todo arquivo', 'Garantida pelo verificador de estilo e pelo teste de arquitetura.'),
    ('Segredos nunca em claro', 'Cifrados ou em hash; nenhuma credencial no repositório.'),
    ('Trabalho pesado é assíncrono e resiliente', 'Aceita, enfileira, reprocessa em falha de transporte.'),
    ('Tudo auditável e imutável', 'Alterações gravadas sozinhas, só acrescentando.'),
    ('Padrões sempre verdes', 'Testes, estilo e arquitetura barram cada mudança.'),
    ('Nenhuma entrega sem relatório', 'E a documentação viva é atualizada a partir deles.'),
    ('Toda lista é paginada, buscada e ordenada no servidor', 'Com contagens por situação.'),
    ('O detalhe devolve todas as colunas visíveis', 'Com as datas de controle e o nome de cada vínculo.'),
    ('A API nunca obriga a tela a mostrar um ID', 'O nome legível vem junto.'),
    ('Todo vínculo se escolhe numa lista', 'Registro existente, ativo e do mesmo cliente.'),
    ('Não existe apagar', 'Arquivar, excluir logicamente em cascata, restaurar.'),
    ('Quem fez, responde', 'Conta e pessoa em toda linha de auditoria; o nível mais alto nunca é barrado por falta de contexto.'),
]
add(part('A', 'Apêndices', 'As leis e as regras, numa página cada, e a lista de conferência de uma tela.', 'book-open', 'sand'))
add(f'''<section class="page-flow">
{chapter('A', 'As 20 leis do painel', 'Estão no AGENTS.md da interface. Quando duas parecerem colidir, vale a de número menor.', 'scale')}
<div class="laws">{''.join(law(i + 1, t, w) for i, (t, w) in enumerate(LAWS))}</div>
</section>''')
add(f'''<section class="page-flow">
{chapter('B', 'As 16 regras do servidor', 'As dez primeiras são do template modular. As seis últimas são as do painel.', 'server')}
<div class="laws">{''.join(law(i + 1, t, w) for i, (t, w) in enumerate(RULES))}</div>
{chapter('C', 'Lista de conferência de uma tela', 'A versão completa está no documento 15 do padrão.', 'clipboard-check')}
{row(bullets(['Coluna principal em duas linhas; de 4 a 6 colunas.', 'Situação em selo; vínculo em etiqueta, pelo nome.', 'Busca, filtros, ordem e página no endereço.', 'Um botão principal na tela.', 'Todas as colunas no modal, em seções por tema.', 'Uma aba para cada relação.', 'Formulário com todas as colunas editáveis.']),
     bullets(['Nenhum identificador em nenhuma tela.', 'Nenhuma palavra em inglês ou nome de coluna.', 'Cada nível vê só o que pode fazer.', 'Sem rolagem lateral em 390 px, com e sem modal.', 'Teclado chega em tudo; o foco é visível.', 'Testes e pacote de produção verdes.', 'Capturas olhadas; relato escrito.']))}
</section>''')
add(f'''<section class="closing">
  <div class="cover-sym">{MARK}</div>
  <span class="cover-logo">{MARK}</span>
  <h2>A arquitetura vira o trilho.<br>O agente vira o trem.</h2>
  <p>O que sobra para você é o que só você pode fazer: decidir o negócio.</p>
  <p class="small">Kurt Pohling · kvrt.pohling@gmail.com</p>
</section>''')

# ------------------------------------------------------------------ estilo
CSS = r'''
@page { size: A4; margin: 16mm 15mm 16mm 15mm;
  @bottom-left { content: "Trilho · Manual do padrão"; font: 7.5pt 'Nunito Sans', sans-serif; color: #8b8273; }
  @bottom-right { content: counter(page); font: 600 8pt 'Nunito Sans', sans-serif; color: #1f5e63; } }
@page :first { margin: 0; @bottom-left { content: none } @bottom-right { content: none } }
@page part { margin: 0; @bottom-left { content: none } @bottom-right { content: none } }
:root { --char: #1e1e1c; --sand: #d8cbb3; --paper: #fbf9f4; --cream: #f4efe5; --a1: #1f5e63; --a1-soft: #dcebeb; --a1-light: #7fbfc4; --a2: #c8643a; --a2-soft: #f6dccf; --a2-light: #e39a76; --muted: #6f685c; --line: #e2d8c5; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 9.6pt/1.5 'Nunito Sans', sans-serif; color: var(--char); }
.ic { display: inline-flex; width: 1.15em; height: 1.15em; vertical-align: -0.2em; }
.ic svg, .cover-sym svg, .part-sym svg, .cover-logo svg, .part-logo svg, .part-ic svg { width: 100%; height: 100%; }
.ic svg { stroke-width: 2; }
h1, h2, h3 { font-family: 'Fraunces', Georgia, serif; font-weight: 700; margin: 0; }
p { margin: 0 0 2.2mm; }
.small { font-size: 7.8pt; color: var(--muted); }
code { font: 7.8pt 'IBM Plex Mono', monospace; background: #efe8d9; padding: .3mm 1.2mm; border-radius: 1mm; }
/* capa */
.cover, .closing { page: part; height: 297mm; width: 210mm; background: var(--char); color: var(--paper); position: relative; overflow: hidden; padding: 22mm 20mm; display: flex; flex-direction: column; break-after: page; }
.cover-sym { position: absolute; right: -28mm; top: 30mm; width: 190mm; height: 190mm; color: var(--sand); opacity: .07; transform: rotate(12deg); }
.cover-sym svg { stroke-width: .9; }
.cover-top { display: flex; align-items: center; gap: 4mm; font: 600 9pt 'Nunito Sans'; letter-spacing: .14em; text-transform: uppercase; color: var(--sand); }
.cover-logo, .part-logo { display: inline-flex; width: 15mm; height: 15mm; border-radius: 3.4mm; background: var(--sand); color: var(--char); padding: 3mm; }
.cover-main { margin-top: 46mm; position: relative; }
.kicker { display: inline-block; font: 700 8pt 'Nunito Sans'; letter-spacing: .16em; text-transform: uppercase; color: var(--a2-light); border: .3mm solid var(--a2-light); border-radius: 10mm; padding: 1.4mm 4mm; margin-bottom: 8mm; }
.cover h1 { font-size: 64pt; line-height: 1; color: var(--paper); }
.cover h1 em { display: block; font-size: 20pt; line-height: 1.25; color: var(--sand); font-style: italic; font-weight: 600; margin-top: 6mm; max-width: 140mm; }
.cover-main p { max-width: 125mm; margin-top: 9mm; font-size: 11pt; color: #cfc7b7; }
.cover-levels { margin-top: auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; position: relative; }
.lv { display: flex; align-items: flex-start; gap: 3mm; background: rgba(216,203,179,.06); border: .25mm solid rgba(216,203,179,.25); border-radius: 2.5mm; padding: 3.2mm 3.5mm; font: 700 9.5pt 'Nunito Sans'; }
.lv .ic { width: 6mm; height: 6mm; color: var(--a1-light); flex: none; } .lv i { font: 400 8pt 'Nunito Sans'; color: #b8ad98; font-style: normal; }
.cover-foot { display: flex; justify-content: space-between; margin-top: 9mm; padding-top: 4mm; border-top: .25mm solid rgba(216,203,179,.3); font-size: 8pt; color: var(--sand); position: relative; }
.closing { justify-content: center; align-items: flex-start; break-after: auto; }
.closing h2 { font-size: 30pt; line-height: 1.12; margin: 10mm 0 5mm; color: var(--paper); } .closing p { color: var(--sand); font-size: 11.5pt; } .closing .small { color: #a79f8f; margin-top: 10mm; font-size: 8.5pt; }
/* parte */
.part { page: part; height: 297mm; width: 210mm; position: relative; overflow: hidden; padding: 0 22mm 40mm; display: flex; flex-direction: column; justify-content: flex-end; break-before: page; break-after: page; }
.part.charcoal { background: var(--char); color: var(--paper); } .part.sand { background: var(--sand); color: var(--char); }
.part-sym { position: absolute; right: 12mm; top: 30mm; width: 140mm; height: 140mm; opacity: .08; } .part-sym svg { stroke-width: .9; }
.part.charcoal .part-sym { color: var(--sand); } .part.sand .part-sym { color: var(--char); opacity: .09; }
.part-badge { position: absolute; top: 18mm; left: 22mm; display: flex; align-items: center; gap: 3mm; font: 700 9pt 'Nunito Sans'; letter-spacing: .16em; text-transform: uppercase; }
.part-logo { width: 12mm; height: 12mm; padding: 2.4mm; border-radius: 3mm; } .part.sand .part-logo { background: var(--char); color: var(--sand); }
.part-num { font: 700 9pt 'Nunito Sans'; letter-spacing: .2em; text-transform: uppercase; }
.part.charcoal .part-num { color: var(--a2-light); } .part.sand .part-num { color: var(--a2); }
.part-ic { display: block; width: 16mm; height: 16mm; margin: 8mm 0 6mm; } .part-ic svg { stroke-width: 1.5; }
.part.charcoal .part-ic { color: var(--a1-light); } .part.sand .part-ic { color: var(--a1); }
.part h1 { font-size: 40pt; line-height: 1.05; } .part p { font-size: 12pt; max-width: 130mm; margin-top: 6mm; opacity: .88; }
/* fluxo */
.page-flow { margin-bottom: 7mm; }
.part + .page-flow { break-before: page; }
.chap { break-after: avoid; display: grid; grid-template-columns: 17mm 1fr; gap: 4mm; margin: 0 0 5mm; padding-bottom: 4mm; border-bottom: .3mm solid var(--line); break-inside: avoid; }
.page-flow > .chap:not(:first-child) { margin-top: 8mm; }
.chap-code { font: 700 15pt 'Fraunces'; color: var(--a2); padding-top: .5mm; }
.chap h2 { font-size: 18pt; display: flex; align-items: center; gap: 2.5mm; } .chap h2 .ic { color: var(--a1); width: 6mm; height: 6mm; flex: none; }
.lead { font-size: 10.2pt; color: #3e3a33; margin-top: 2mm; }
h3 { font-size: 12pt; margin: 4.5mm 0 2.5mm; color: var(--a1); break-after: avoid; }
.row > div > h3:first-child { margin-top: 0; }
.chips { display: inline-flex; flex-wrap: wrap; gap: 1.6mm; vertical-align: middle; }
.chip { font: 700 7.4pt 'Nunito Sans'; padding: .7mm 2.6mm; border-radius: 10mm; background: #ece5d6; color: #4a463e; border: .2mm solid #d6cab2; }
.chip.success { background: #d9f6dd; color: #03642b; border-color: #9bdda8; } .chip.warning { background: #fee8da; color: #7e3f02; border-color: #feb98b; }
.chip.error { background: #ffe6e3; color: #89322c; border-color: #ffb5ac; } .chip.info { background: #dfeffe; color: #02578b; border-color: #9cd1fe; }
.chip.ref { background: var(--paper); border-radius: 1.4mm; font-weight: 600; } .chip.code { background: #ece5d6; border-radius: 1.4mm; font: 500 7.4pt 'IBM Plex Mono'; }
.plain { font-size: 9pt; } .muted { color: var(--muted); } .quote { font-style: italic; border-left: .7mm solid var(--sand); padding-left: 2.5mm; font-size: 9pt; }
/* figuras */
.shot { margin: 0 0 4.5mm; break-inside: avoid; }
.frame { border-radius: 2.6mm; overflow: hidden; border: .3mm solid #cdbfa5; background: #fff; box-shadow: 0 1mm 3mm rgba(30,30,28,.10); }
.frame img { display: block; width: 100%; object-fit: cover; object-position: top; }
.shot.wide .frame img { max-height: 102mm; }
.shot.half .frame img { max-height: 60mm; }
figcaption { font-size: 7.9pt; color: var(--muted); margin-top: 1.8mm; line-height: 1.45; }
.src { display: inline-block; font: 700 6.6pt 'Nunito Sans'; letter-spacing: .08em; text-transform: uppercase; padding: .3mm 1.8mm; border-radius: 1mm; margin-right: 1.8mm; vertical-align: .2mm; }
.src.a1 { background: var(--a1-soft); color: var(--a1); } .src.a2 { background: var(--a2-soft); color: #8a3f1f; }
.diag { margin: 1mm 0 4.5mm; break-inside: avoid; background: var(--cream); border: .3mm solid var(--line); border-radius: 3mm; padding: 3mm 4mm 2.5mm; }
.diag img { display: block; max-width: 100%; margin: 0 auto; }
.diag figcaption { text-align: center; }
.row { break-inside: avoid; display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; margin-bottom: 1mm; }
.row.phones { grid-template-columns: repeat(3, 1fr); align-items: start; padding: 0 12mm; gap: 8mm; }
.shot.phone .frame { border-radius: 5mm; border: 1.5mm solid var(--char); }
.shot.phone .frame img { max-height: 100mm; }
/* passos, notas, listas */
.steps { list-style: none; counter-reset: s; padding: 0; margin: 2mm 0 5mm; display: grid; gap: 2.4mm; }
.steps li { counter-increment: s; display: grid; grid-template-columns: 7mm 1fr; column-gap: 3mm; align-items: start; break-inside: avoid; }
.steps li::before { content: counter(s); grid-row: span 2; width: 7mm; height: 7mm; border-radius: 50%; background: var(--char); color: var(--sand); font: 700 9pt 'Fraunces'; display: flex; align-items: center; justify-content: center; }
.steps b { font-family: 'Fraunces'; font-size: 10pt; } .steps span { color: #4a463e; font-size: 9pt; }
.note { display: grid; grid-template-columns: 7mm 1fr; gap: 3mm; background: var(--cream); border: .3mm solid var(--line); border-radius: 2.6mm; padding: 3.2mm 4mm; margin: 2mm 0 4.5mm; break-inside: avoid; }
.note .ic { width: 6mm; height: 6mm; color: var(--a1); } .note p { margin: 0; font-size: 8.9pt; }
.note.lock .ic, .note.warn .ic { color: var(--a2); } .note.tip { background: var(--a1-soft); border-color: #bfd8d9; }
.bul { margin: 0 0 4mm; padding: 0; list-style: none; } .bul li { position: relative; padding-left: 4.5mm; margin-bottom: 1.3mm; font-size: 9.1pt; break-inside: avoid; }
.bul li::before { content: ''; position: absolute; left: .6mm; top: 2.1mm; width: 1.6mm; height: 1.6mm; border-radius: 50%; background: var(--a2); }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; margin: 3mm 0 5mm; break-inside: avoid; }
.stats div { background: var(--char); color: var(--paper); border-radius: 2.6mm; padding: 3.5mm 4mm; } .stats b { display: block; font: 700 20pt 'Fraunces'; color: var(--a2-light); line-height: 1.1; } .stats span { font-size: 8pt; color: var(--sand); }
.cards { display: grid; gap: 3.5mm; margin: 2mm 0 5mm; } .cards.c3 { grid-template-columns: repeat(3, 1fr); } .cards.c2 { grid-template-columns: repeat(2, 1fr); }
.card { background: var(--paper); border: .3mm solid var(--line); border-radius: 3mm; padding: 3.6mm 4mm; break-inside: avoid; }
.card .ic { width: 8.5mm; height: 8.5mm; padding: 1.8mm; border-radius: 2mm; background: var(--a1-soft); color: var(--a1); display: flex; margin-bottom: 2.2mm; }
.card:nth-child(even) .ic { background: var(--a2-soft); color: #8a3f1f; }
.card b { font-family: 'Fraunces'; font-size: 10.2pt; } .card p { font-size: 8.5pt; color: #4a463e; margin: 1.3mm 0 0; line-height: 1.42; }
.legend { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm 6mm; margin-bottom: 4mm; break-inside: avoid; }
.legend div { display: grid; grid-template-columns: 7mm 1fr; gap: 2mm; } .legend .ic { width: 5.5mm; height: 5.5mm; color: var(--a1); } .legend p { font-size: 8.8pt; margin: 0; }
table { width: 100%; border-collapse: collapse; }
.toc td { padding: 1.7mm 0; border-bottom: .25mm solid var(--line); vertical-align: top; }
.toc .n { width: 12mm; font: 700 13pt 'Fraunces'; color: var(--a2); } .toc b { display: block; font-family: 'Fraunces'; font-size: 10.2pt; } .toc span { font-size: 8.5pt; color: var(--muted); }
.grid { margin: 2mm 0 5mm; } .grid th { text-align: left; font: 700 7.4pt 'Nunito Sans'; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); padding: 2mm; border-bottom: .5mm solid var(--char); }
.grid td { padding: 1.8mm 2mm; border-bottom: .25mm solid var(--line); font-size: 8.8pt; vertical-align: top; }
.grid td:first-child { font-weight: 700; width: 34%; } .grid.tight td { padding: 1.15mm 2mm; font-size: 8.5pt; } .grid.tight td:first-child { width: auto; white-space: nowrap; color: var(--a2); }
tr { break-inside: avoid; }
.badges { margin: 1mm 0 5mm; break-inside: avoid; } .badges th { text-align: left; width: 34mm; font: 700 9pt 'Fraunces'; padding: 2.6mm 0; border-bottom: .25mm solid var(--line); vertical-align: middle; }
.badges td { padding: 2.6mm 0; border-bottom: .25mm solid var(--line); } .badges .small { margin-left: 2mm; }
.swatches { display: grid; grid-template-columns: repeat(5, 1fr); gap: 3mm; margin: 2mm 0 5mm; break-inside: avoid; }
.swatches i { display: block; height: 17mm; border-radius: 2.6mm; margin-bottom: 2mm; } .swatches b { display: block; font-family: 'Fraunces'; font-size: 9.6pt; } .swatches span { font-size: 7.6pt; color: var(--muted); }
.dotc { display: inline-block; width: 3.2mm; height: 3.2mm; border-radius: 50%; vertical-align: -.4mm; margin-right: 1mm; }
.tree { background: var(--char); color: #e9e1d0; border-radius: 3mm; padding: 4mm 5mm; margin: 2mm 0 4.5mm; break-inside: avoid; }
.tree pre { margin: 0; font: 7.7pt/1.62 'IBM Plex Mono', monospace; white-space: pre; } .tree b { color: var(--a2-light); font-weight: 500; }
.ask { display: grid; grid-template-columns: 1fr 1.15fr; gap: 0; margin-bottom: 3.6mm; border-radius: 3mm; overflow: hidden; border: .3mm solid var(--line); break-inside: avoid; }
.ask > div { display: grid; grid-template-columns: 6.5mm 1fr; gap: 2.5mm; padding: 3.4mm 4mm; } .ask p { margin: 0; font-size: 8.8pt; line-height: 1.45; }
.ask-q { background: var(--char); color: #efe8d9; } .ask-q .ic { width: 5.5mm; height: 5.5mm; color: var(--a2-light); } .ask-q p { font-style: italic; }
.ask-a { background: var(--paper); } .ask-a .ic { width: 5.5mm; height: 5.5mm; color: var(--a1); }
.laws { display: grid; grid-template-columns: 1fr 1fr; gap: 2.2mm 6mm; margin-bottom: 5mm; }
.law { display: grid; grid-template-columns: 8mm 1fr; gap: 2.5mm; padding: 2mm 0; border-bottom: .25mm solid var(--line); break-inside: avoid; }
.law-n { font: 700 13pt 'Fraunces'; color: var(--a2); line-height: 1.1; } .law b { font-family: 'Fraunces'; font-size: 9.4pt; line-height: 1.25; display: block; } .law p { margin: .8mm 0 0; font-size: 8.2pt; color: #4a463e; line-height: 1.4; }
'''

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,700;1,9..144,600&family=IBM+Plex+Mono:wght@400;500&family=Nunito+Sans:wght@400;600;700&display=swap" rel="stylesheet">'
doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Trilho · Manual do padrão</title>{FONTS}<style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
(ROOT / 'manual.html').write_text(doc)
print('ok', len(doc), 'imagens', doc.count('<img src="img/'), 'diagramas', doc.count('<img src="diagramas/'))
