# CLAUDE.md — Template Laravel Modular

Guia de padrões para qualquer pessoa (ou agente) que trabalhe neste repositório.
**Leia antes de escrever código.** Este arquivo é o contrato: a IA opera DENTRO
destas regras, e as regras são executáveis (Pest + Pint + ArchTest quebram se
forem violadas).

## Visão

> ⚠️ **PREENCHIDO PELO PRONTUÁRIO.** Enquanto este bloco existir, o projeto ainda
> é o template genérico. Rode a skill **`/prontuario`** para: entrevistar o dono
> do produto, gerar os documentos de domínio (`docs/dominio/`), definir os módulos
> iniciais, renomear projeto/namespace e reescrever esta seção com a visão real
> do sistema.

Enquanto isso, o sistema de referência é o **exemplo executável**: um fluxo de
pedidos (`orders`) que cobra pagamentos (`payments`) e notifica (`notifications`),
multi-tenant, assíncrono e auditado — exatamente a mecânica que qualquer sistema
construído sobre este template herda.

## A verdade mora na documentação

A documentação canônica vive em [`docs/`](docs/README.md) (se o projeto tiver uma
base externa — Notion, wiki — ela vence o repositório; registre isso aqui). **Se
este arquivo ou o código divergirem da documentação canônica, a documentação
vence.** Em caso de ambiguidade genuína ou lacuna, **pare e pergunte** — não
assuma. Decisões de produto pertencem ao dono do produto, não à IA.

## Stack definitiva

- **PHP 8.2+** (tipagem estrita em tudo)
- **Laravel 12**
- **PostgreSQL 16 próprio** em produção — sem Postgres-as-a-service (dev
  rápido: sqlite; `compose.yaml` sobe pg16+redis7)
- **Eloquent** como **única** camada de acesso a dados
- **Redis 7** (filas + cache) via `predis` — produção; filas **nomeadas** por
  prioridade de negócio
- **Laravel Horizon** — workers/filas (`php artisan horizon` em Linux/produção;
  no Windows dev use `queue:work`/`queue:listen` — `ext-pcntl` é Unix-only; o
  `composer.json` tem platform-fakes de `ext-pcntl`/`ext-posix` só para instalar)
- **internachi/modular** — arquitetura modular (módulos em `app-modules/`)
- **Pest** — testes (DB de teste = `sqlite :memory:`, fila `sync`)
- **Pint** — estilo (preset `laravel` + `declare_strict_types`)
- **Front-end**: qualquer SPA (React, Angular, Vue) consumindo a API — o backend
  não renderiza telas; opcionais documentados no README §Dependências (Filament,
  Inertia, Pulse, laravel/mcp...)

## Paradigma: arquitetura MODULAR (não por camadas)

O projeto é um **modular monolith** com `internachi/modular`. O domínio vive em
`app-modules/<módulo>/` — **não** em `app/Services`, `app/Controllers`, etc. Cada
módulo é um pacote Composer com namespace `Modules\<Modulo>\` e fronteira própria:
um módulo **nunca** importa a classe interna de outro; eles falam por **contratos**
e **eventos** declarados no módulo `core`. Detalhe completo em
[`docs/arquitetura/ARQUITETURA.md`](docs/arquitetura/ARQUITETURA.md).

Módulos atuais: `core` (shared kernel), `tenancy` (o tenant), e os **exemplos
removíveis** `orders`/`payments`/`notifications` (o fluxo de referência — remova-os
ao iniciar o sistema real, via `/prontuario`).

## As 10 regras de ouro

1. **A verdade mora na documentação.** `docs/` é canônico; em dúvida, pergunte —
   nunca assuma decisão de produto.
2. **Eloquent é a única camada de dados.** Sem SQL cru / query builder para regra
   de negócio; sem Postgres gerenciado de terceiros.
3. **Fronteira de módulo é sagrada.** Toda lógica vive em **Actions** dentro do
   módulo dono; os canais (REST, MCP, CLI) são adaptadores **finos** sobre as
   mesmas Actions. Comunicação entre módulos só por **contrato** (síncrono),
   **evento** (assíncrono) ou **read model/DTO** (leitura) — nunca importando o
   interno de outro módulo. O teste de arquitetura quebra o CI se a fronteira
   for furada **ou se um controller consultar dados** (Eloquent, `DB` ou model
   em `Http/Controllers`).
4. **Multi-tenancy sempre.** Todo model com escopo de tenant usa `Entityable` +
   `EntityScope` (ambos no `core`); nunca cruze tenants; restaure o contexto com
   `TenantContext::runAs()` em jobs, workers e em qualquer canal sem sessão HTTP.
5. **`declare(strict_types=1)` em todo arquivo PHP.** Tipagem estrita, garantida
   pelo Pint e verificada pelo ArchTest.
6. **Segredos nunca em claro.** Credenciais/segredos cifrados ou como hash;
   nenhuma credencial real no repositório; `.env.example` só com placeholders.
7. **Trabalho pesado é assíncrono e resiliente.** `POST` de operação demorada
   retorna **202** + Job em fila nomeada; jobs reprocessam em timeout/5xx
   (**nunca os capturam** — erro de transporte lança, recusa de negócio vira
   estado final); idempotência pela `ref` do cliente.
8. **Tudo auditável e imutável.** Mutações gravadas via **Observers** (que
   estendem o `AuditObserver` do core) em `audit_logs` (append-only); colunas
   sensíveis fora do diff via `$hidden` do observer.
9. **Padrões sempre verdes.** Pest + Pint + ArchTest barram cada mudança;
   convenções de nomenclatura (prefixo de 3 letras, UUID PK, SoftDeletes,
   FKs `{tabela_singular}_{pk}`) sem exceção.
10. **Nenhuma entrega termina sem relatório.** Toda feature fecha com um
    `docs/reports/vX.Y.Z/feat_*.md` e uma entrada `pending` no
    `docs/reports/sync-state.json`; a skill `/sync-docs` propaga os reports
    pendentes para a documentação evergreen (`SISTEMA.md`, `docs/dominio/`,
    este arquivo). Reports são fotografias datadas — não se atualizam
    retroativamente.

## As regras do painel (11 a 16)

Todo sistema feito com este kit tem uma interface que segue um padrão fixo (lista →
modal de detalhe com abas → formulário; nunca ID cru; tudo editável; exclusão lógica).
A API precisa entregar o que esse padrão exige. Detalhe em
[`docs/arquitetura/PAINEL.md`](docs/arquitetura/PAINEL.md),
[`DADOS.md`](docs/arquitetura/DADOS.md) e
[`CONTAS_E_AUDITORIA.md`](docs/arquitetura/CONTAS_E_AUDITORIA.md).

11. **Toda lista é paginada, buscada e ordenada no servidor** pelo `Listing` do core
    (`page`, `per_page` ≤ 100, `q` sem acento, `order` da lista permitida,
    `meta.counts`). Nenhum endpoint devolve "tudo" para a tela filtrar.
12. **O detalhe devolve todas as colunas visíveis**, com as datas de controle e o nome
    de cada vínculo. Um teste de contrato por recurso garante.
13. **A API nunca obriga a tela a mostrar um ID.** Todo lugar que menciona outro
    registro traz o rótulo legível (`*_name`, `labels`, `title`, `record_label`, `refs`).
14. **Todo vínculo se escolhe numa lista.** A API recebe o id de um registro existente,
    ativo e do mesmo tenant (qualquer outra coisa = 422 no campo) e oferece
    `options?q=`. Texto livre só para observação, motivo e o nome do que se cadastra.
15. **Não existe apagar.** Cadastro se arquiva (flag `*_active`); registro se exclui
    logicamente, em cascata, com prévia e `expected_total`; tudo se restaura. Os
    vínculos vivem **só** no `ForeignKeyMap`, e chave estrangeira segue o padrão
    `fk_<tabela>_<coluna>` deferrable (nunca `->constrained()`).
16. **Quem fez, responde.** Toda linha de auditoria grava a conta **e** o operador
    (a pessoa), inclusive as inserções diretas; conteúdo sensível fica fora do diff.
    O nível mais alto nunca é barrado por falta de tenant.

## Mapa de pastas

```
app/                          # app host ENXUTA: middlewares de borda,
                              #   exceção handler, providers globais. SÓ ISSO.
  Http/Middleware/            #   ResolveTenantFromHeader (PLACEHOLDER de auth —
                              #   substitua pelo middleware real de token)
app-modules/                  # <- todo o domínio vive aqui
  core/                       # shared kernel: Contracts, Events, DTOs, Exceptions,
                              #   Entityable, EntityScope, TenantContext,
                              #   AbstractAction, Input adapters, AuditLog,
                              #   AuditObserver, audit:query
  tenancy/                    # Entity (o tenant) — cresce com User/papéis/onboarding
  orders/                     # [EXEMPLO] Action → 202+Job → contrato → evento
  payments/                   # [EXEMPLO] implementa PaymentGateway (bind no provider)
  notifications/              # [EXEMPLO] ouve OrderPaid (listener queued)
config/app-modules.php        # config do internachi/modular (namespace Modules\)
config/models.php             # bindings de model cross-módulo (relações por config)
docs/                         # índice em docs/README.md
  arquitetura/                #   COMO: ARQUITETURA, MODULOS, CORE, COMUNICACAO,
                              #     FRONTEIRAS, IMPLEMENTACAO, BANCO, CODE_STYLE,
                              #     PAINEL, DADOS, CONTAS_E_AUDITORIA
  dominio/                    #   O QUE: regras de negócio (nasce do /prontuario)
  reports/                    #   entregas versionadas + SISTEMA.md (evergreen)
                              #     + sync-state.json (versionamento de contexto)
tests/                        # Unit/ Feature/ Arch/ da raiz; módulos têm tests/
.claude/skills/               # prontuario, dominio, nova-feature, sync-docs,
                              #   novo-modulo, nova-tabela, novo-recurso-admin
```

Cada módulo é um mini-Laravel (`src/`, `routes/`, `database/`, `tests/`). O que num
app normal fica em `app/Models`, `app/Jobs`, `app/Http`, aqui fica em
`app-modules/<modulo>/src/...`. Árvores completas em
[`docs/arquitetura/MODULOS.md`](docs/arquitetura/MODULOS.md).

## Fluxo canônico (o exemplo executável)

1. `POST /v1/orders` → middleware `resolve.tenant` popula o `TenantContext` →
   `OrderController` (fino) → `PlaceOrderAction` (sanitize→validate→authorize→handle)
   → **idempotência pela `ref`** → cria `Order` (status `processing_payment`;
   `Entityable` preenche o tenant; `OrderObserver` grava o audit_log) → despacha
   `ProcessOrderPaymentJob` na fila `orders` → responde **202**.
2. `ProcessOrderPaymentJob` (`tries=5`, backoff): **`TenantContext::runAs()`**
   restaura o tenant → guard de idempotência → chama o contrato `PaymentGateway`
   (implementação em `payments`, bind no provider):
   - **aprovado** → `paid` + evento `OrderPaid`;
   - **recusa de negócio** → `payment_failed` + motivo (estado final, sem retry);
   - **erro de transporte** → exceção sobe → a fila reprocessa (nunca capture).
3. `notifications` ouve `OrderPaid` (listener queued) e reage — `orders` não
   conhece os ouvintes.

Esse fluxo é o molde de QUALQUER operação de escrita relevante do sistema real.

## Comandos úteis

```bash
composer dev            # serve + queue:listen + pail + vite (concurrently)
composer test           # pest (Unit + Feature + Modules + Arch)
composer test:coverage  # pest --coverage --min=70
composer lint           # pint (corrige)
composer lint:check     # pint --test (CI / antes de commitar)
php artisan about       # status do ambiente (deve terminar sem erros)
php artisan modules:list
php artisan make:model X --module=<modulo>   # make:* com --module
php artisan audit:query <tabela> <id>        # trilha de auditoria de um registro
php artisan migrate
php artisan horizon     # workers (Linux/produção; Windows: queue:work)
docker compose up -d    # PostgreSQL 16 + Redis 7 locais
```

## Ciclo de feature (o "batimento")

Toda feature segue o mesmo ritual — a skill **`/nova-feature`** o executa:

```
tarefa definida → branch feat/... → implementar por blocos (teste junto)
  → Pest + Pint + ArchTest verdes → relatório em docs/reports/vX.Y.Z/feat_*.md
  → entrada "pending" no sync-state.json → merge --ff-only + push
  → (quando conveniente) /sync-docs propaga os reports pendentes p/ docs evergreen
```

Feature que muda o que a interface vê (campo, filtro, status, tabela, permissão)
fecha o relatório com a seção **"Para o front"** e atualiza `docs/api/openapi.yaml`
na mesma entrega.

Honestidade é invariante: **nunca** declare uma entrega completa se não estiver
100% (testes verdes, sem ressalvas ocultas); ressalvas vão EXPLÍCITAS no
relatório. Commits em português, imperativos, prefixados (`feat:`, `fix:`,
`chore:`, `docs:`, `refactor:`, `test:`); rode `composer lint:check && composer
test` antes de commitar.

## Skills disponíveis (.claude/skills/)

| Skill | Quando usar |
| --- | --- |
| `/prontuario` | **Primeira coisa num sistema novo**: entrevista o dono do produto, gera docs/dominio, renomeia projeto/namespace, remove exemplos |
| `/dominio` | Antes de responder/planejar qualquer coisa de negócio: carrega docs/dominio + SISTEMA.md para a sessão |
| `/nova-feature` | Executar o ciclo de feature completo (branch → código+testes → report → sync-state) |
| `/sync-docs` | Propagar reports pendentes (sync-state.json) para a documentação evergreen |
| `/novo-modulo` | Criar um módulo novo com TODAS as convenções (composer, provider, ArchTest, docs) |
| `/nova-tabela` | Toda migration que cria tabela ou vínculo: convenções + `ForeignKeyMap` + nome legível + observer + testes de guarda |
| `/novo-recurso-admin` | Expor uma tabela ao painel no contrato único (lista, detalhe completo, criar, editar, arquivar) e avisar o front |

## Estado atual

Template recém-nascido: shared kernel + tenancy + exemplo executável, **44 testes
/ 113 assertions verdes**, Pint verde, ArchTest verde. O retrato completo e
sempre-atual do sistema vive em
[`docs/reports/SISTEMA.md`](docs/reports/SISTEMA.md) — ao entregar features,
mantenha-o vivo via `/sync-docs` (regra de ouro nº 10).
