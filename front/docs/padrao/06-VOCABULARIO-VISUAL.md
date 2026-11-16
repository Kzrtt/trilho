# 06 — Vocabulário visual

A mesma informação tem **a mesma cara em todo lugar**: lista, campo do modal, tabela
dentro de aba, auditoria, painel. "Texto cru" onde cabe um destes é defeito.

## 1. Os cinco jeitos de mostrar um valor

| O valor é... | Mostra-se como | Exemplo |
| --- | --- | --- |
| um **estado** ou valor de vocabulário fixo | **badge** (pílula com cor, ícone e texto) | (✓ Ativa) (◷ Pendente) (✕ Recusado) |
| uma **coisa**: registro vinculado, código, documento | **chip** | (⌂ UBS Centro) `123.456.789-00` |
| uma **data** | data formatada | 12/03/2026 · 12/03/2026 14:30 |
| um **texto escrito por alguém** (motivo, observação) | citação: bloco com aspas/recuo | "Paciente mudou de bairro." |
| todo o resto | texto | |

A decisão é tomada **num lugar só** (o "olhar do detalhe"): uma função que recebe o
rótulo/tipo da coluna e o valor e devolve o jeito de mostrar. Todas as peças que exibem
valor passam por ela. Coluna nova com nome diferente? Acrescente a regra **lá**.

```ts
type Look =
  | { kind: 'text' }
  | { kind: 'badge'; state: 'sucesso' | 'alerta' | 'erro' | 'info' | 'neutro'; icon? }
  | { kind: 'chip'; chip: 'ref' | 'code'; icon? }
  | { kind: 'date' }
  | { kind: 'quote' };

function lookFor(label: string, value: unknown): Look
```

## 2. Badge

Pílula: fundo tom 100, borda tom 300, texto tom 700, **ícone à esquerda** na cor do texto.
12px/600, sem quebra.

| Família | Palavras típicas | Ícone |
| --- | --- | --- |
| sucesso | Ativo, Aprovado, Vigente, Concluído, Pago, Sim | check em círculo |
| alerta | Pendente, Aguardando, Rascunho, Vence em breve | relógio |
| erro | Recusado, Cancelado, Expirado, Bloqueado | x em círculo |
| info | Em análise, Em andamento | ampulheta |
| neutro | Inativo, Arquivado, Encerrado, **qualquer palavra fora do mapa** | traço em círculo |

Regras:

- **Um mapa central por vocabulário** (status de cada entidade, papéis, tipos, ações da
  auditoria): valor da API → `{ texto em pt-BR, família, ícone }`. Lista, modal, auditoria
  e painel leem o mesmo mapa. Antes de criar um rótulo, procure o valor no código e
  reaproveite: mapas divergentes já mostraram "Convidado" numa tela e "Convite enviado" na outra.
- Valor fora do mapa sai **neutro** com o próprio texto, e isso é um aviso de que falta
  acrescentá-lo.
- "Sim/Não" sozinho numa ficha vira "Rótulo: Sim".
- O mesmo "Não" pode ser alerta num campo e neutro em outro: a sobrescrita é por campo.
- Papéis/níveis têm badge próprio, com ícone por nível.
- Badges vizinhos **nunca se encostam**: grupo em `flex` com `gap: 6px`.

## 3. Chip

| Tipo | Uso | Visual |
| --- | --- | --- |
| `ref` | registro vinculado (unidade, pessoa, entidade) | ícone do tipo + **nome**; clicável: abre o modal daquele registro |
| `code` | código, documento, número, login, sigla | monoespaçado, fundo `neutro-100` |

- Cada tipo de registro tem **um** ícone, o mesmo do menu e da ficha do modal.
- Vários vínculos numa célula: um chip para cada, com `gap`.
- Documento pessoal (CPF) aparece **mascarado** para quem não é Admin: `***.456.789-**`.

## 4. Nunca ID cru (lei 5)

Em nenhum lugar da interface aparece um identificador interno (UUID, ULID, sequência).

- **Vínculo** mostra o nome útil do outro registro, que a API devolve junto (rótulo).
- Registro sem nome próprio (uma linha de vínculo, um log) tem rótulo **composto**:
  "Dra. Ana · UBS Centro", "Maria Souza · Lembrete · 12/03/2026".
- Sem nenhum dado para compor: "Registro sem nome". O ID, não.
- Na **auditoria**: o registro aparece pelo rótulo; nos valores antes/depois, vínculo
  aparece pelo nome; identificador solto vira "Registro vinculado"; a chave do próprio
  registro some do diff.
- Só aparece "Nº" quando é um número **com significado para a pessoa** (número do
  documento, do protocolo).

Varredura obrigatória antes de entregar: abrir toda tela e o primeiro modal de cada uma e
procurar texto com cara de ID (ver [`15`](15-VERIFICACAO.md)).

## 5. Rótulos em português

- Nenhum nome de coluna do banco, valor de enum ou nome de tabela aparece na tela.
- Um **mapa de rótulos** central: tabela → nome no plural; coluna → rótulo; fragmentos
  comuns (`created_at` → "Criado em"). Coluna sem entrada cai num tradutor de fragmentos;
  se ainda sobrar inglês, é defeito: acrescente a entrada.
- Tom: frase curta, sem jargão. "Situação", não "Status do registro". "Excluir", não "Deletar".
- Primeira letra maiúscula só na primeira palavra ("Criado em", "Nova unidade").
- Gênero certo: "Nova unidade", "Novo médico" (o cadastro declara o gênero).

## 6. Datas, números, vazio

| Dado | Formato |
| --- | --- |
| data | `dd/mm/aaaa` |
| data e hora | `dd/mm/aaaa hh:mm` (24h) |
| recente (painel, atividade) | "há 5 min", "ontem", com a data completa no `title` |
| número | milhar com ponto, decimal com vírgula |
| dinheiro | `R$ 1.234,56` |
| vazio | "—" apagado; na coluna principal, "Não informado" em itálico |
| dia sem dado numa série | **lacuna**, nunca zero |

## 7. Ícones

- **Uma biblioteca**, um traço (Lucide por padrão).
- Todo botão, badge, alerta e erro de campo tem ícone. Seção do menu tem; item do menu não.
- Tamanhos: 12px em badge e botão pequeno; 14–15px em botão e menu; 16px em alerta; 20px
  na ficha do modal.
- Mapa de ações: Novo `plus` · Editar `pencil` · Arquivar/Excluir `trash-2`/`archive` ·
  Restaurar `rotate-ccw` · Atualizar `refresh-cw` · Voltar `arrow-left` · Buscar `search` ·
  Filtros `sliders-horizontal` · Imprimir `printer` · Baixar `download` · Abrir `chevron-right` ·
  Sair `log-out`.
- Botão só de ícone: sempre `title` + `aria-label`.

## 8. Botões (resumo)

| Tipo | Quando | Visual |
| --- | --- | --- |
| **Primário** | a ação principal, **uma por tela** (Novo; Editar no modal) | fundo `marca-300` |
| **Secundário** | Salvar/Confirmar | fundo `neutro-800`, texto claro |
| **Neutro** | todo o resto | fundo `neutro-0`, borda `neutro-300` |
| **Perigo discreto** | Excluir, Arquivar, Revogar, Sair | fundo `erro-50`, texto `erro-700` |
| **Perigo** | o botão final de uma confirmação destrutiva | fundo `erro-500` |
| **Sucesso** | Aprovar | fundo `sucesso-500` |
| **Desabilitado** | ação que não vale agora | `neutro-100`, com o motivo no `title` |
