# 09 — Acesso, menu e os poderes do Admin

## 1. Dois eixos: nível e permissão

- **Nível** (papel): a posição da pessoa na hierarquia (ex.: Admin da plataforma →
  Institucional → Gestor → Operador). O nível de cima faz tudo que o de baixo faz.
- **Permissão**: uma chave que libera uma capacidade (`units.manage`, `audit.view`). O
  login devolve a lista `permissions[]` daquela conta.

Regra: **tela e ação são liberadas por permissão**; o nível decide o **recorte dos
dados** (de qual entidade/unidade a pessoa vê) e quem pode criar/gerir quem.

Tudo num lugar só:

```ts
// quem pode abrir cada tela
canOpenRoute(route: string, user): boolean
// quem pode fazer cada ação
can(action: 'enrollments.decide' | 'cards.print' | ..., user): boolean
```

Nenhum componente decide permissão por conta própria com `if (role === ...)`.

## 2. Esconder, não desabilitar

- O que o nível **não pode fazer não aparece**: item de menu, botão, aba, campo.
- Desabilitado (com o motivo no `title`) é para ação que a pessoa **pode** fazer, mas não
  **neste registro, agora** (ex.: "Só um pedido em análise pode ser aprovado").
- A API é a autoridade: esconder na tela não substitui o 403. Tela aberta por link direto
  sem permissão mostra "Você não tem acesso a esta área", dentro da casca.

## 3. O menu

Uma definição ([`02`](02-CASCA.md), §3): seções → itens `{ label, route, permissions | roles, queryParams?, badge? }`.

- Os cadastros do motor entram sozinhos, pelo grupo declarado.
- Quem só tem uma unidade/entidade não vê seletor de unidade/entidade.
- Critério para uma tabela ter item de menu: **nenhuma outra tela a mostra**. Se ela já é
  editada numa aba de um pai, não entra.

## 4. Gestão de contas

- A tela de usuários mostra **só os níveis abaixo** de quem olha (o Admin vê também a si).
- Criar conta: nível escolhido entre os que a pessoa pode criar; a conta nasce com
  **senha provisória**, mostrada **uma vez**, com botão de copiar e o aviso de que não
  será exibida de novo.
- Senha provisória obriga a troca antes de qualquer outra tela.
- "Redefinir senha" gera outra provisória e derruba as sessões.
- Senha nunca é exibida nem editada; é hash.
- **Conta e pessoa são coisas diferentes** quando o sistema precisa responsabilizar:
  a conta é o login; o **operador** é a pessoa (nome, documento, contato). A conta aparece
  em toda parte como "Nome do operador (login)". Uma conta tem um operador vigente por
  vez; o histórico de vínculos fica. Conta sem operador continua funcionando, aparece com
  um badge e pode ser corrigida pela tela.

## 5. O que o nível mais alto (Admin) tem a mais

Sempre **dentro das telas normais**, nunca numa área separada:

| Poder | Onde aparece |
| --- | --- |
| **Ver todas as entidades** | filtro "Entidade" nas listas; coluna de entidade |
| **Ver excluídos** | alternador ao lado de "Atualizar lista"; a lista passa a mostrar os excluídos, com badge |
| **Editar dados** (todas as colunas editáveis do registro) | botão na faixa de ações de **todo** modal de registro editável; abre o diálogo com um campo tipado por coluna |
| **Excluir / Restaurar** em cascata | mesma faixa; antes de confirmar, a **prévia**: cada tabela afetada e quantos registros, e o que será mantido |
| **Entrar como** | faixa de ações do modal de uma conta: abre outra aba com uma sessão temporária daquela pessoa; a sessão do Admin não muda |
| **Tabelas sem tela** | itens de menu para as poucas tabelas que nenhuma tela mostra (sequências, registros de acesso), com a tela genérica de dados: mesma lista, mesmo modal, uma aba por tabela-filha |
| **Auditoria completa** | sem filtro de entidade obrigatório; documentos sem máscara |

Regras do "Editar dados":

- rótulos em português, nunca nome de coluna;
- vínculo com o campo de relação (busca por nome); enum e booleano com `select`;
- chave primária, datas de controle e segredos não aparecem;
- grava antes/depois na auditoria;
- tabelas de registro (auditoria, acessos) são **só leitura**: sem editar, sem excluir.

O Admin **nunca é barrado por falta de contexto** (ele não pertence a uma entidade): a
ação descobre a entidade pelo registro-alvo. Se uma ação falha para o Admin por isso, é
defeito do back.

## 6. Exclusão em cascata (a tela)

1. "Excluir" abre a **prévia**: "Isto vai excluir 1 pessoa, 3 documentos e 12 respostas.
   Ficam: 4 registros de acesso."
2. Confirmar exige a ação explícita (botão *Perigo*), com Cancelar à esquerda e afastado.
3. Se o total mudou entre a prévia e a confirmação, o servidor recusa (409) e a tela
   mostra a prévia nova.
4. O registro some das listas; o Admin o vê com "Ver excluídos" e pode **Restaurar**
   (que também tem prévia e traz de volta os pais excluídos).

Para os demais níveis, o que existe é **Arquivar/Restaurar** de cadastro (o registro sai
das escolhas novas; o que já existe continua).

## 7. Acesso sensível com motivo

Quando abrir um dado exige justificativa (dado clínico, financeiro, sigiloso):

- a tela pede o **motivo** (mínimo de caracteres) **antes** de buscar qualquer dado sensível;
- o motivo vale por um tempo (ex.: 30 min), só na memória da aba;
- vencido, a tela pede de novo;
- a tela mostra um aviso permanente de que o acesso é registrado;
- existe a aba "Quem viu" no registro, para quem tem a permissão de auditoria.

## 8. Sessão

- Sessão expirada (401): volta ao login guardando para onde ia; depois de entrar, retorna.
- Muitas tentativas (429): mensagem com o tempo de espera.
- Login com usuário inexistente dá a **mesma** mensagem de senha errada.
