---
name: identidade
description: Primeira coisa num projeto de front novo. Entrevista curta com o dono do produto (nome, logo, duas cores de realce, fontes, níveis de acesso, seções do menu), gera a folha de tokens, a definição do menu e preenche a "Visão do projeto" do AGENTS.md. Use quando o AGENTS.md ainda tiver a Visão marcada como "PREENCHIDO PELA SKILL /identidade", ou quando o usuário pedir para definir/trocar a identidade visual, a paleta ou os níveis de acesso do painel.
---

# Identidade do projeto

Você vai transformar o padrão genérico no painel **deste** produto. O padrão já decide
casca, lista, modal e formulário; aqui se decide só o que muda de um produto para outro.
Não pergunte nada sobre layout.

## Pré-checagens

1. Leia `AGENTS.md` e `docs/padrao/00-PRINCIPIOS.md`, `01-TOKENS.md`, `02-CASCA.md`, `09-ACESSO-E-MENU.md`.
2. Se a "Visão do projeto" já estiver preenchida, pergunte se é uma **revisão** e mude só o que for pedido.
3. Se existir o repositório da API ao lado, leia `docs/dominio/` e o `CLAUDE.md` dele: nome,
   atores e módulos provavelmente já estão lá. **Não pergunte o que já está escrito.**

## Passo 1 — Entrevista (grupos pequenos; opções quando forem enumeráveis)

**A. Produto**
- Nome do sistema e uma frase: o que faz e para quem.
- Quem usa o painel no dia a dia (perfil, familiaridade com computador)? Usa celular?
- Existe área para o usuário final (cidadão, paciente, cliente) fora do painel?

**B. Marca**
- Logo (arquivo) e versão para fundo escuro. Sem logo: proponha um símbolo simples e marque como provisório.
- **Duas cores de realce.** Peça as da marca ou proponha três pares sóbrios que funcionem
  sobre charcoal e sand. Realce 1 = ação principal; realce 2 = detalhe.
- Fontes: manter o padrão (Poppins nos títulos, Nunito Sans no texto, IBM Plex Mono em código) ou trocar?
- Neutros: manter a rampa quente charcoal → sand (padrão) ou esfriar?

**C. Acesso**
- Os níveis, do mais alto ao mais baixo, com o nome em português de cada um.
- Quem cria quem. O que cada nível enxerga (toda a plataforma, uma entidade, uma unidade).
- Existe dado sensível que pede motivo para abrir?

**D. Menu**
- As áreas do sistema. Proponha as seções (Início, Operação, Cadastros, Catálogos, Gestão)
  e encaixe as áreas; peça só a confirmação.

## Passo 2 — Gerar

1. **Tokens**: crie a folha de tokens a partir do modelo de `01-TOKENS.md`, com as rampas
   `marca` e `realce` calculadas das duas cores. **Confira o contraste** (texto sobre
   `marca-300` ≥ 4,5:1; `marca-300` sobre `marca-50` ≥ 4,5:1; texto `realce-700` sobre
   `realce-100` ≥ 6:1) e ajuste o tom se não passar. Mostre os valores.
2. **Fontes**: carregue-as no projeto e ligue `--font-heading`, `--font-body`, `--font-mono`.
3. **Menu**: escreva a definição única (seções, ícones, itens, quem pode abrir).
4. **Níveis**: o mapa de níveis (valor da API → nome em português, ícone, estado do badge)
   e o arquivo de acesso (`canOpenRoute`, `can`).
5. **Casca**: monte topo, menu, perfil e palco com as peças do kit; ponha o logo.
6. **AGENTS.md**: substitua o bloco "Visão do projeto" por: nome, frase, público, as duas
   cores (com os hex), fontes, tabela de níveis, seções do menu, e as decisões tomadas.

## Passo 3 — Conferir

- Capturas da casca em 1440×900 e 390×844, com o menu aberto e a gaveta.
- A página de demonstração do kit (botões, badges, chips, alertas, tabela, modal,
  formulário) com a paleta nova: nada ilegível, nenhum realce confundido com estado.
- Mostre as capturas ao dono e peça o aceite da paleta **antes** de escrever telas.

## Regras

- Nunca escolha cor de realce igual à de um estado (verde de sucesso, âmbar, vermelho, azul de info)
  sem avisar do risco e separar bem os usos.
- Nada de terceira cor de realce.
- Decisão de produto que faltar: pergunte uma vez, com opções. Não invente nível nem área.
