# Trilho

Conjunto de arquivos orientadores (`AGENTS.md`, `CLAUDE.md`, documentos de apoio e skills)
para construir sistemas com **a mesma arquitetura no servidor e a mesma lógica visual na
interface**, descrevendo só o negócio em linguagem natural.

> "A arquitetura vira o trilho; a IA vira o trem. O que sobra para o humano é o que só ele
> pode fazer: decidir o negócio, modelar o domínio e traduzir regras em contratos."

Você modela, escreve os requisitos e a regra de negócio. O kit decide como o sistema sai:
casca, lista, modal de detalhe com abas, formulário, vocabulário visual, guia de tela,
auditoria, exclusão lógica, contrato da API.

## O que tem aqui

```
back/     arquivos do repositório da API (Laravel modular)
  CLAUDE.md · AGENTS.md
  docs/arquitetura/     11 documentos: o paradigma modular + o contrato do painel
  docs/dominio/         o contrato dos documentos de negócio (preenchidos pelo /prontuario)
  docs/reports/         relatórios de entrega + versionamento de contexto
  .claude/skills/       prontuario, dominio, nova-feature, sync-docs, novo-modulo,
                        nova-tabela, novo-recurso-admin

front/    arquivos do repositório da interface (qualquer framework)
  AGENTS.md · CLAUDE.md
  docs/padrao/          16 documentos: o padrão visual e de comportamento
  .claude/skills/       identidade, novo-cadastro, nova-tela, auditar-detalhe,
                        guia-de-tela, revisao-visual

manual/   o manual em PDF (como funciona e como os sistemas saem) e o que o gera
COMO_USAR.md   instalação e o caminho de um projeto novo
PROMPTS.md     exemplos de pedidos em linguagem natural e o que cada um aciona
```

## Comece por aqui

- **[Manual do Trilho (PDF)](manual/Manual-do-Trilho.pdf)**: como funciona e como os sistemas saem, com telas do Fibro+ e do Urban Pass.
- **[laravel-modular-template](https://github.com/Kzrtt/laravel-modular-template)**: o template do servidor. Os arquivos de `back/` são os dele, com os acréscimos do painel; um projeto novo parte de lá.
- [`COMO_USAR.md`](COMO_USAR.md) e [`PROMPTS.md`](PROMPTS.md).

## De onde veio

| Origem | O que deu |
| --- | --- |
| [Template Laravel modular](https://github.com/Kzrtt/laravel-modular-template) | a arquitetura do servidor: módulos com fronteira executável, tenant, auditoria, ciclo de feature com relatório |
| Especificação visual de origem (documento privado) | papéis de cor, anatomia dos componentes, fluxo lista → modal → edição |
| **Urban Pass** (React) | guia de tela, tabela que vira cartões, motor de recursos em React |
| **Fibro+** (Angular) | a versão mais completa: abas de relação, edição ampla, nunca ID cru, vocabulário visual único, console de dados, conta × operador |

## As ideias que seguram tudo

**No servidor**
1. O domínio vive em módulos; um módulo nunca importa a classe interna de outro.
2. Toda lógica em Actions; tudo auditado, com conta e pessoa; nada se apaga de verdade.
3. A API entrega o que a tela precisa: lista no servidor, detalhe completo, rótulo no lugar de ID.
4. As regras são executáveis: teste de arquitetura, testes de guarda, estilo.
5. Nenhuma entrega sem relatório; a documentação viva é sincronizada a partir deles.

**Na interface**
1. Lista → modal → edição. O modal mostra tudo e tem uma aba por relação.
2. Tudo se edita; o nível mais alto vê e corrige qualquer dado, dentro das telas normais.
3. Nunca ID cru; estado é badge; coisa é chip; a mesma palavra em toda tela.
4. Cor é exceção: charcoal e sand como base, duas cores de realce em dose pequena.
5. Tela complexa se explica com um guia no topo.

## Sobre as capturas do manual

As telas do Fibro+ usam dados fictícios criados para documentação; as do Urban Pass vêm do
ambiente de testes. Os dois sistemas são repositórios privados: aqui está só o padrão
extraído deles.
