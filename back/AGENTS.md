# AGENTS.md

> Base: [laravel-modular-template](https://github.com/Kzrtt/laravel-modular-template).

As regras deste repositório estão em [`CLAUDE.md`](CLAUDE.md) e valem para qualquer agente de
codificação (Claude Code, Codex, OpenCode, Cursor...). Leia-o inteiro antes de escrever código.

Resumo do que não se negocia:

1. A documentação em `docs/` é canônica; em dúvida de negócio, pergunte.
2. O domínio vive em `app-modules/<módulo>/`; um módulo nunca importa a classe interna de outro.
3. Toda lógica em Actions; controllers finos; Eloquent como única camada de dados.
4. Multi-tenant sempre (`Entityable` + `TenantContext::runAs()` em jobs).
5. Tudo auditado, com conta e operador; nada se apaga de verdade.
6. A API entrega o que o padrão do painel exige (regras 11 a 16).
7. Pest + Pint + ArchTest verdes; `composer lint && composer lint:check && composer test` antes de commitar.
8. Nenhuma entrega sem relatório em `docs/reports/` e entrada no `sync-state.json`.

As skills ficam em `.claude/skills/` (`prontuario`, `dominio`, `nova-feature`, `sync-docs`,
`novo-modulo`, `nova-tabela`, `novo-recurso-admin`). Agentes sem suporte a skills leem o
`SKILL.md` correspondente e seguem os passos.
