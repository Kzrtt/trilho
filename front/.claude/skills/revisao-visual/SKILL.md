---
name: revisao-visual
description: Revisão antes de entregar qualquer mudança de interface — roda testes e build, tira capturas em 1440 e 390 com o modal aberto, faz as varreduras de ID cru, texto cru e rolagem lateral, entra com cada nível de acesso e percorre a lista de conferência do padrão. Use ao terminar uma tela, antes de commit/push de front, ou quando o usuário pedir para revisar/validar/conferir o visual.
---

# Revisão visual

A fonte é `docs/padrao/15-VERIFICACAO.md`. Esta skill é a ordem de execução.

## 1. Código

Encadeie com `&&` (falha em um bloqueia o seguinte; nunca passe a saída por um filtro que
esconda o código de saída):

```
verificação de tipos && testes && build de produção
```

Formate **só os arquivos tocados**. Depois os greps:

- cor solta nos estilos tocados: `grep -nE "#[0-9a-fA-F]{3,8}\b"`;
- diálogo do navegador: `grep -rn "window\.\(alert\|confirm\|prompt\)"`;
- célula crua em tela à mão: `grep -rn "<td[^>]*>{{"` (ou o equivalente do framework).

## 2. Ambiente de captura

- API local com dados **fictícios** (nunca dados reais em captura).
- Front servido sem recarga a quente se já houve muitas edições.
- Roteiro do navegador automatizado escrito num arquivo na pasta de rascunho; sessão
  criada com uma resposta **real** do login no armazenamento.

## 3. Capturas

Para cada tela tocada, em **1440×900** e **390×844**: a lista; o modal aberto (cada aba);
o formulário; os estados de vazio e de erro quando mudaram. Monte lado a lado e **olhe**:
alinhamento, badges encostados, texto cortado, modal largo demais (meça em 1440 e 1920),
primário duplicado, cor fora de lugar.

## 4. Varreduras (todas as rotas, primeiro registro, cada aba)

1. **ID cru** → esperado zero.
2. **Texto cru** (`snake_case`, enum em inglês, `null`, `undefined`, data ISO) → zero.
3. **Rolagem lateral** em 320/360/390/430, com a rede de segurança desligada → zero.

Na primeira vez em cada projeto, prove cada detector fazendo-o falhar de propósito.

## 5. Níveis

Entre com **cada nível**: menu, botões, abas e campos batem com o arquivo de acesso; link
direto para tela proibida mostra o aviso. Como Admin: ver excluídos, editar dados,
excluir com prévia, restaurar.

## 6. Teclado e leitor

Tab chega em tudo na ordem visual; foco visível; modal prende e devolve o foco; Esc fecha.
Verificador automático de acessibilidade sem violação nova.

## 7. Relato

1. O que mudou.
2. O que foi conferido e o resultado (números dos testes, capturas anexas, varreduras zeradas).
3. O que **não** foi feito ou depende do back.
4. O que precisa de decisão do dono.

Só diga "pronto" se os itens 1 a 6 passaram. Ressalva vai escrita, não escondida.
