# Como usar

## 1. Instalar num projeto

### Servidor (API)

Projeto **novo**: parta do [laravel-modular-template](https://github.com/Kzrtt/laravel-modular-template) e copie por cima o conteúdo de `back/`.

```bash
cp -r trilho/back/. minha-api/
```

Projeto **existente** que já nasceu do template: copie só o que é novo, sem sobrescrever
o que o projeto já preencheu.

```bash
cp trilho/back/docs/arquitetura/{PAINEL,DADOS,CONTAS_E_AUDITORIA}.md  minha-api/docs/arquitetura/
cp -r trilho/back/.claude/skills/{nova-tabela,novo-recurso-admin}     minha-api/.claude/skills/
cp trilho/back/AGENTS.md minha-api/
```

Depois, à mão: traga para o `CLAUDE.md` do projeto a seção **"As regras do painel (11 a
16)"**, as duas linhas novas da tabela de skills e a seção "Para o front" do
`docs/reports/README.md`. **Não** sobrescreva `docs/reports/SISTEMA.md`,
`sync-state.json`, `docs/dominio/` nem a "Visão" do `CLAUDE.md`.

### Interface

```bash
cp -r trilho/front/. minha-interface/
```

Se o projeto já tem `AGENTS.md`/`CLAUDE.md`, mantenha as seções próprias dele (stack,
comandos, convenções do framework) e acrescente o conteúdo do kit.

## 2. O caminho de um projeto novo

| Passo | Onde | O que você faz | O que sai |
| --- | --- | --- | --- |
| 1 | API | `/prontuario` e responde à entrevista | documentos de domínio, glossário, níveis de acesso, módulos, projeto renomeado |
| 2 | API | descreve as tabelas e regras; `/nova-feature` | módulos, tabelas (`/nova-tabela`), recursos do painel (`/novo-recurso-admin`), relatórios com "Para o front" |
| 3 | Interface | `/identidade` | tokens com as duas cores de realce, casca, menu, níveis |
| 4 | Interface | "crie o cadastro de X" → `/novo-cadastro` | lista + modal com abas + formulário |
| 5 | Interface | "crie a fila de aprovação de Y" → `/nova-tela` + `/guia-de-tela` | tela de fluxo com guia no topo |
| 6 | Interface | `/revisao-visual` | capturas, varreduras, relato |
| 7 | API | `/sync-docs` | documentação viva atualizada |
| de tempos em tempos | Interface | `/auditar-detalhe` | todo campo no modal, nenhum ID, tudo editável |

## 3. O que você precisa dizer (e o que não precisa)

**Diga**: o que o sistema faz e para quem; as "coisas" do negócio e os estados de cada
uma; quem pode o quê; os números (prazos, limites); como você chama cada coisa.

**Não diga**: como é a lista, onde fica o botão, que cor tem o status, se abre modal ou
página, como é o formulário, como é o menu. Isso está no padrão.

## 4. Dois repositórios, um acordo

O servidor e a interface conversam por um contrato escrito dos dois lados:
`back/docs/arquitetura/PAINEL.md` e `front/docs/padrao/13-CONTRATO-COM-A-API.md`.
Quando a interface precisa de algo que a API não devolve, o agente **pede** (o formato
está no §12 do contrato do front) em vez de contornar. Quando a API muda o que a tela vê,
o relatório da entrega traz a seção **"Para o front"**.

Dica: abra os dois repositórios lado a lado e dê ao agente da interface acesso de leitura
ao `docs/` da API. A skill `/identidade` e a `/novo-cadastro` leem de lá.

## 5. Outros agentes

`AGENTS.md` é o arquivo que Codex, OpenCode, Cursor e afins leem. As skills são arquivos
`SKILL.md` em Markdown: um agente sem suporte a skills lê o arquivo e segue os passos
("siga `.claude/skills/novo-cadastro/SKILL.md` para a tabela X").

## 6. Manter o kit vivo

Aprendeu algo num projeto (uma armadilha, uma decisão do dono, uma peça nova)? Traga
para cá: a lição entra no documento do assunto, como regra com o motivo, e os projetos
puxam a atualização. O Fibro+ continua sendo a referência: o que muda lá e vale para
todos, sobe para o kit.
