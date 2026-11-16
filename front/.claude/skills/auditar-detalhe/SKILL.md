---
name: auditar-detalhe
description: Audita uma ou todas as telas contra as leis de completude do painel — toda coluna do banco aparece no modal de detalhe, toda coluna editável está no formulário, toda relação tem aba, nenhum ID cru, nenhum texto cru. Compara banco, resposta da API e tela, e corrige encaixando cada campo na seção existente. Use quando o usuário disser que falta campo/dado num modal, que apareceu um ID, que algo não é editável, ou pedir uma revisão de completude das telas.
---

# Auditar detalhe (banco → API → tela)

O dono do produto **não vai apontar o que falta**: você procura. A falta pode estar na
API (o recurso omite a coluna) e não só na tela.

## Passo 1 — Levantar, por tabela

1. **Colunas do banco**: `information_schema.columns` (ou a migration/model). Nomes não são
   adivinháveis: leia.
2. **Vínculos**: quem esta tabela aponta e **quem aponta para ela** (o mapa de vínculos do
   back, se existir).
3. **API**: chame `GET /recurso` e `GET /recurso/{id}` como o nível mais alto e achate as chaves.
4. **Tela**: os campos do modal (configuração ou template), os campos do formulário, as abas.

## Passo 2 — A matriz

| Coluna | Na API (detalhe)? | No modal? Em qual seção | No formulário? | Observação |
| --- | --- | --- | --- | --- |

Ficam de fora de propósito: segredos (senha, token, códigos de recuperação), a data de
exclusão, colunas técnicas de busca. Chave primária e datas de controle aparecem no
modal (seção "Registro") e não são editáveis; a chave primária só aparece se for um
número com significado.

E a matriz de relações:

| Tabela que aponta para esta | Tem aba? | A linha abre o modal dela? | Permissão |
| --- | --- | --- | --- |

## Passo 3 — Corrigir

- **Falta na API**: acrescente ao recurso do back (se você tem o repositório) ou escreva
  o pedido (`docs/padrao/13-CONTRATO-COM-A-API.md` §12). Atualize o tipo do front com a chave exata.
- **Falta no modal**: um campo a mais **na seção existente que combina**. Seção nova só se
  nenhuma servir, e com nome de tema. **Nunca** seção genérica ("Outros dados", "Todos os
  campos", "Dados do registro"): isso já foi recusado mais de uma vez.
- **Falta no formulário**: o campo no grupo de mesmo nome, com o controle certo (vínculo =
  busca; conjunto fechado = select).
- **Falta aba**: declare a relação; a linha abre o modal do relacionado.
- **Modal precisa de campos que a lista não traz**: busque o detalhe ao abrir.
- **ID na tela**: troque pelo rótulo que a API devolve; se não devolve, peça.
- **Texto cru**: rótulo no mapa central; valor no mapa de badges; regra no "olhar do detalhe".

## Passo 4 — Provar

1. Matriz refeita: nenhuma linha sem destino.
2. Varreduras de ID e de texto cru (`docs/padrao/15-VERIFICACAO.md` §2 e §3) em **todas** as
   rotas, abrindo o primeiro registro e cada aba.
3. Capturas do modal em 1440 e 390.
4. Testes e build de produção verdes.

## Relato

A matriz antes e depois, o que mudou em cada tela, o que foi pedido ao back, e o que
ficou de fora com o motivo.
