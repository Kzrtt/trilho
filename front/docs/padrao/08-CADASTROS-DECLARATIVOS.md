# 08 — Cadastros declarativos (o motor)

Cerca de 80% das telas de um sistema são **lista + detalhe + formulário** de uma tabela.
Essas telas **não são escritas uma a uma**: cada uma é um arquivo de configuração,
desenhado por páginas genéricas. Tela nova = um arquivo + uma linha no registro.

O que o motor garante sem ninguém escrever: busca, ordem, página, filtros e contagens na
URL; linha que abre o modal (`?ver=`), abas (`?aba=`); todos os campos no detalhe;
arquivar/restaurar com aviso do que está em uso; envio só do que mudou; erro 422 embaixo
do campo; pergunta ao sair com alteração; menu, rotas e guarda de permissão gerados do registro.

## 1. A convenção de API que o motor fala

`/api/v1/<área>/admin/<recurso>` (o back cria com a skill `/novo-recurso-admin`):

| Chamada | Significado |
| --- | --- |
| `GET /` | lista paginada: `page`, `per_page`, `q`, `order` (`campo` / `-campo`), `status` = `active` (padrão) / `archived` / `all`, filtros próprios. Resposta `{ data, meta: { total, page, per_page, last_page, counts: { active, archived } } }` |
| `GET /{id}` | `{ data }` com **todos** os campos e `usage` (referências vivas: `{ users: 12 }`) |
| `POST /` | cria (201) |
| `PATCH /{id}` | altera só os campos enviados; campo imutável depois de usado responde 422 naquele campo |
| `POST /{id}/archive`, `/restore` | o único jeito de "remover" |

Filhos são recursos próprios, listados com `?<pai>_id=<id>` e criados com o id do pai no corpo.

## 2. A configuração

```ts
export const UNITS = defineResource<Unit>({
  key: 'units',                                   // rota: /app/cadastros/units
  group: 'cadastros',                             // seção do menu
  icon: Building2,                                // o ícone desse tipo de registro, em todo lugar
  label: { singular: 'Unidade', plural: 'Unidades', gender: 'a' },   // "Nova unidade"
  description: 'Os locais de atendimento da entidade.',
  api: '/staff/admin/units',
  permissions: { read: ['units.manage'], write: ['units.manage'] },

  list: {
    searchPlaceholder: 'Buscar por nome ou sigla',
    empty: 'Nenhuma unidade cadastrada.',
    defaults: { order: 'name' },
    columns: [
      { header: 'Unidade', primary: true, sort: 'name', value: u => u.name, sub: u => u.city },
      { header: 'Sigla', chip: 'code', narrow: true, value: u => u.code },
      { header: 'Entidade', chip: 'ref', icon: Landmark, value: u => u.entity_name },
      { header: 'Situação', badge: u => activeBadge(u) },
    ],
    filters: [{ key: 'entity_id', label: 'Entidade', allLabel: 'Todas', options: l => l.entities(), when: isAdmin }],
  },

  detail: {
    title: u => u.name,
    subtitle: u => u.city,
    meta: [{ label: 'Entidade', value: u => u.entity_name }],
    sections: [
      { title: 'Identificação', icon: IdCard, fields: [
        { label: 'Nome', value: u => u.name, cols: 8 },
        { label: 'Sigla', value: u => u.code, cols: 4 },
      ]},
      { title: 'Registro', icon: Clock, fields: [
        { label: 'Criado em', value: u => u.created_at },
        { label: 'Última alteração', value: u => u.updated_at },
      ]},
    ],
  },

  form: {
    notice: 'Mudar o nome muda o que aparece nos documentos emitidos.',
    groups: [
      { title: 'Identificação', icon: IdCard, fields: [
        { name: 'name', label: 'Nome', required: true, max: 120, cols: 8 },
        { name: 'code', label: 'Sigla', required: true, max: 10, cols: 4,
          locked: u => u.usage?.users ? 'A sigla não muda depois que a unidade tem usuários.' : null },
        { name: 'entity_id', label: 'Entidade', kind: 'relation', only: 'create', when: isAdmin,
          relation: { search: q => entities.search(q) } },
      ]},
    ],
  },

  usage: { users: ['usuário', 'usuários'], patients: ['paciente', 'pacientes'] },
  children: [ /* listas-filhas: abas editadas no lugar */ ],
  related: [                                      // abas de relação
    { key: 'users', label: 'Usuários', api: '/staff/users', param: 'unit_id',
      columns: [...], empty: 'Nenhum usuário nesta unidade.',
      open: u => ({ commands: ['/app/users'], queryParams: { ver: u.id } }),
      permissions: ['users.manage'] },
  ],
});
```

### O que cada bloco vira

| Bloco | Vira |
| --- | --- |
| `key`, `group`, `icon`, `label`, `permissions` | item de menu, rotas (`/<key>`, `/novo`, `/<id>/editar`), guarda de acesso |
| `list.columns` | colunas da tabela (`primary` + `sub`, `badge`, `chip`, `sort`, `narrow`) |
| `list.filters` | o modal de filtros |
| `detail.title/subtitle/meta` | a ficha do modal |
| `detail.sections` | as seções de leitura (campos, tabela pequena, ou seção carregada à parte) |
| `form.groups` | os cartões do formulário (mesmos nomes das seções do detalhe) |
| `children` | abas de lista-filha |
| `related` | abas de relação |
| `usage` | as palavras do aviso antes de arquivar ("12 usuários e 3 médicos usam esta unidade") |
| `creatable: false` / `archivable: false` | catálogo que só troca rótulos; registro que não se arquiva |
| `guide` | o guia de tela daquele cadastro, quando precisar |

### Campo de formulário

`name` é **o nome do campo na API** (chave do corpo e do `errors` do 422).
`kind`: `text` (padrão), `textarea`, `number`, `select`, `switch`, `relation`, `list`, `rows`.
Opções: `required`, `max`, `cols`, `help`, `placeholder`, `pattern`, `mask`, `options` /
`loadOptions`, `only: 'create' | 'edit'`, `when(user)`, `locked(record)`, `showWhen(values)`,
`initial`, `omitEmpty`.

## 3. Lista de conferência de um cadastro novo

- [ ] Coluna principal com segunda linha; 4 a 6 colunas; status em badge; vínculo em chip.
- [ ] **Todas** as colunas da tabela nas seções do detalhe (inclui "Registro").
- [ ] **Todas** as colunas editáveis nos grupos do formulário.
- [ ] Uma aba `related` para cada tabela que aponta para esta.
- [ ] Vínculos como `relation`; conjuntos fechados como `select` com as palavras do mapa.
- [ ] `usage` com singular e plural de cada referência.
- [ ] Rótulos da tabela e das colunas no mapa central de rótulos.
- [ ] Teste do cadastro: lista, abre o modal, cria, edita, arquiva.

## 4. Quando o motor não basta

Telas com comportamento próprio (fila com decisão, quadro, editor, importação, painel)
são escritas à mão **com as mesmas peças** (`Adm*`), o mesmo controlador de lista e o
mesmo modal de detalhe. O motor cobre o comum; não impede ninguém de escrever uma página.
Sinal de que é tela à mão: a ação principal não é "criar/editar/arquivar".

Mesmo numa tela à mão, a configuração pode trazer um detalhe próprio (`modal`) no lugar
do genérico, mantendo lista, filtros e URL.

## 5. Gerador

Se o projeto tiver um gerador (schematic, plop, script), ele cria o arquivo de
configuração-esqueleto e o registra. O que sobra para quem escreve: ajustar campos ao que
a API devolve, traduzir rótulos, declarar relações.

## 6. Limites conscientes

- A API é a autoridade: o cliente confere obrigatório e tamanho; o resto volta como 422.
- Lista-filha edita no lugar (sem segundo modal).
- Recurso sem contrato de lista no servidor não é um cadastro do motor: é tela à mão.
