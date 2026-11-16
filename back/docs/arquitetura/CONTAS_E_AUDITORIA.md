# Contas, níveis e responsabilização

> Quem entra, o que pode, o que enxerga e **quem responde** por cada ação. Complementa
> [`CORE.md`](CORE.md) (tenant e auditoria base).
>
> Implementação de referência: módulo `tenancy` do Fibro+ e
> `docs/dominio/ACESSO_E_TENANCY.md` de lá.

## 1. Nível × permissão × recorte

| Eixo | O que é | Onde é checado |
| --- | --- | --- |
| **Nível** (papel) | posição na hierarquia; o de cima contém o de baixo | quem cria/gere quem; o recorte dos dados |
| **Permissão** | chave que libera uma capacidade (`units.manage`, `audit.view`) | middleware `permission:` na rota |
| **Recorte** | de qual tenant/unidade a pessoa vê dados | `EntityScope` + escopo próprio do módulo |

- Cada nível nasce com um **modelo de permissões**; quem gere contas pode ajustar por conta.
- O login devolve `role`, `role_label` e `permissions[]`; a interface monta menu e botões
  com isso. A API continua sendo a autoridade (esconder na tela não substitui o 403).
- Permissão checada **fora** do módulo dono usa um helper do `core`
  (`StaffPermission::has($user, StaffPermission::X)`), para não importar o enum de outro módulo.
- A lista de contas mostra **só os níveis abaixo** de quem pergunta; só o nível mais alto
  se vê na lista (e, ao se editar, muda só o login).
- Registro de outro recorte responde **igual a registro inexistente** (404): "proibido"
  já confirmaria que ele existe.

### Receita para conferir a matriz real

Um teste descartável que percorre todas as rotas `GET` sem parâmetro, por nível, e grava
os códigos de resposta dá a matriz verdadeira. (Os nomes de middleware do `route:list`
não são confiáveis para isso.) Apague a sonda depois.

## 2. Conta = login; operador = pessoa

Quando o sistema precisa **responsabilizar pessoas**, a conta e a pessoa são tabelas diferentes:

- **Conta** (`users`): só o login e a credencial. Equipe entra por **login**; usuário
  final por documento.
- **Operador** (`operators`): a pessoa — nome, documento, contato. Dado pessoal mora **só
  aqui**, nunca duplicado na conta.
- **Vínculo** conta ↔ operador com histórico: um operador **vigente** por conta; trocar
  encerra o anterior e abre o novo; o histórico fica.
- Em toda resposta, a conta aparece como **"Nome do operador (login)"** (só o login, se
  não houver operador).
- Conta sem operador **continua funcionando**, vem marcada e pode ser corrigida pela tela.

## 3. Auditoria com responsável

Tudo o que o [`CORE.md`](CORE.md) já diz (observer, append-only, `$hidden`), mais:

- Toda linha de `audit_logs` grava **a conta e o operador vigente**
  (`aud_user_id` + `aud_operator_id`). O core resolve o operador por um **contrato**
  (`ActingOperator::idFor(?string $userId)`), implementado no módulo de contas e
  memorizado por requisição: o core não importa o módulo.
- **Toda inserção direta** em `audit_logs` (edição ampla, cascata, "entrar como")
  **preenche o operador** pelo mesmo contrato. Sem exceção.
- Mudança em massa não dispara observer: quem faz `update` em massa grava a auditoria à mão.
- Ação pelo console técnico grava o ator como `console:<id>`.
- **Conteúdo sensível não entra no diff**: registra-se **que houve** a ação (resposta
  enviada, documento aberto, senha redefinida), sem o conteúdo, o caminho do arquivo ou o hash.
- A trilha de um registro: `audit:query <tabela> <id>` e o endpoint de atividade do registro.
- A API de auditoria devolve `record_label` e `refs`: a tela nunca mostra id.
- Ninguém edita ou exclui trilha. Nem o nível mais alto.

## 4. Leitura de dado sensível

Para dado que pede justificativa (clínico, financeiro, sigiloso):

1. `POST …/{id}/access { reason }` (mínimo de caracteres) abre uma janela de tempo (ex.: 30 min).
2. As leituras mandam o identificador do motivo num cabeçalho; sem motivo vigente → **428**.
3. Cada leitura é gravada (quem, quando, o quê); existe o endpoint "quem viu".
4. Níveis de gestão que não precisam do conteúdo **não têm** a permissão de leitura sensível.
5. O nível mais alto lê sem digitar motivo, mas a abertura fica gravada como acesso administrativo.
6. Leitura pública por código (QR) também é gravada, com data, IP e aparelho.

## 5. O nível mais alto

- **Não pertence a um tenant.** Regra: ele nunca é barrado por isso. A borda
  (`ResolveTenantFromUser`) descobre o tenant pelo **alvo** da rota (o registro em
  `{id}`) ou pelo corpo (`unit_id`). Toda ação nova que precisa de tenant acrescenta o
  seu alvo a esse mapa, e é testada como o nível mais alto num banco PostgreSQL de rascunho.
  Não derive o tenant de um `entity_id` do corpo (quebra os fluxos de criação que o proíbem).
- **Vê excluídos** (`deleted=1`), edita qualquer coluna editável, exclui/restaura em
  cascata ([`DADOS.md`](DADOS.md)).
- **"Entrar como"**: `POST …/admin/impersonate` cria um token temporário (ex.: 2 h) para
  ver o sistema como outra conta; o início é auditado; a troca de senha obrigatória não
  se aplica a esse token.

## 6. Credenciais

- Senha é hash. Não existe "ver senha". Redefinir gera uma **provisória**, devolvida uma
  única vez, que obriga a troca antes de qualquer outra rota e derruba as outras sessões.
- "Esqueci a senha": link de uso único com validade; falha no envio responde 503 (a
  pessoa sabe que o e-mail não saiu).
- Login com usuário inexistente dá a **mesma** mensagem de senha errada.
- Limite de tentativas no login e nas áreas sensíveis.
- Token de API com hash; segredo nunca em resposta, log ou diff.

## 7. Minimização em tela

- Documento pessoal sai **mascarado** (`***.456.789-**`) para quem não precisa dele
  inteiro (`Masking::cpf`).
- Indicador agregado de grupo pequeno é suprimido (mínimo definido pelo produto).
- Canal público nunca devolve dado pessoal, texto livre nem classificação interna.

## 8. Comunicação que parte do sistema

- E-mail por evento + listener em fila; exceção documentada quando precisa ser síncrono
  (a pessoa está esperando o link).
- Tudo que escreve para o usuário final **por conta própria** (lembrete, aviso) é
  **opt-in**: nasce desligado, a pessoa liga, o rodapé desliga com um link assinado.
- Um registro de cada envio (tabela só de leitura).
- "Não chegou": confira o registro e a lista de bloqueio do provedor antes do código.

## 9. Lista de conferência

- [ ] Rota nova com `permission:`; nível mais alto testado sem tenant.
- [ ] Recorte testado: outro tenant responde 404 igual a inexistente.
- [ ] Mutação auditada com conta **e** operador; conteúdo sensível fora do diff.
- [ ] Inserção direta em `audit_logs` preenche o operador.
- [ ] Documento mascarado para quem não é o nível mais alto.
- [ ] Mensagens de erro em pt-BR, sem revelar existência.
