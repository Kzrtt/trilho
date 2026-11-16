# 15 — Verificação

Nada é "pronto" porque compilou. Toda entrega de tela passa por esta conferência, e o
relato final diz o que foi conferido.

## 1. Lista de conferência

### Lista
- [ ] Coluna principal em duas linhas; 4 a 6 colunas; sem coluna de ID.
- [ ] Status em badge; vínculo em chip com nome; datas `dd/mm/aaaa`.
- [ ] Busca, filtros, ordem, página e tamanho na URL; recarregar mantém.
- [ ] Um botão primário na tela.
- [ ] Vazio sem filtro, vazio com filtro, carregando e erro existem e têm texto.
- [ ] Contagens da linha do tempo batem com a lista.

### Modal de detalhe
- [ ] Linha e seta abrem; `?ver=` na URL; recarregar abre o mesmo registro.
- [ ] **Todas** as colunas da tabela aparecem (banco → API → modal), em seções por tema.
- [ ] Nenhuma seção genérica; seção "Registro" com as datas de controle.
- [ ] Uma aba para cada tabela relacionada; a linha da aba abre o modal do relacionado.
- [ ] Editar leva ao formulário com **todas** as colunas editáveis.
- [ ] Esc, X e fundo fecham; o foco volta; a página destrava a rolagem.
- [ ] Largura ≤ 1320px em 1440 **e** em 1920.

### Formulário
- [ ] Grupos com os mesmos nomes das seções do detalhe; linhas somam 12.
- [ ] Obrigatório em negrito; vínculo por busca; conjunto fechado em select.
- [ ] Enviar vazio: erro embaixo de cada campo; corrigir: some.
- [ ] 422 do servidor cai no campo certo; salvar envia só o que mudou.
- [ ] Sair com alteração pergunta.

### Vocabulário
- [ ] **Nenhum ID** em nenhuma tela (varredura §2).
- [ ] Nenhuma palavra em inglês, nome de coluna ou valor de enum cru (varredura §3).
- [ ] A mesma palavra para o mesmo estado em todas as telas.
- [ ] Badges e chips vizinhos não se encostam.

### Acesso
- [ ] Entrar com **cada nível**: o menu, os botões e as abas batem com a matriz.
- [ ] Link direto para tela sem permissão mostra o aviso, não tela quebrada.
- [ ] Admin: ver excluídos, editar dados, excluir com prévia, restaurar.

### Celular e acessibilidade
- [ ] 390×844: sem rolagem lateral, com e sem modal (varredura §4).
- [ ] Tabela em cartões; abas e passos quebram de linha; gaveta pela esquerda.
- [ ] Teclado: chega em tudo, foco visível, modal prende o foco.
- [ ] Verificador automático de acessibilidade (axe) sem violação nova.

### Código
- [ ] Só tokens (`grep -nE "#[0-9a-fA-F]{3,8}\b"` nos estilos tocados não acha cor solta).
- [ ] Só peças do kit; nada de `alert`/`confirm` (`grep -rn "window\.\(alert\|confirm\)"`).
- [ ] Sem célula crua (`grep -rn "<td[^>]*>{{"` nas telas à mão).
- [ ] Verificação de tipos, testes e **build de produção** verdes, nesta ordem, encadeados com `&&`.

## 2. Varredura de ID

Com o navegador automatizado (Playwright), logado como o nível mais alto: visitar **toda
rota** do painel, abrir o **primeiro registro** de cada lista e cada aba do modal, e
procurar nós de texto com cara de identificador.

```js
const ID = /^(?:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|[0-9A-HJKMNP-TV-Z]{26})$/i;
const hits = await page.evaluate((src) => {
  const re = new RegExp(src, 'i'), out = [];
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = walk.nextNode()); ) {
    const t = n.textContent.trim();
    if (re.test(t)) out.push(t + ' @ ' + n.parentElement.closest('[class]')?.className);
  }
  return out;
}, ID.source);
```

Resultado esperado: zero. Prove que a varredura funciona fazendo-a falhar de propósito uma vez.

## 3. Varredura de texto cru

No mesmo passeio, procurar: `snake_case` (`/\b[a-z]+_[a-z_]+\b/`), valores de enum
conhecidos (`pending`, `active`, `draft`...), `null`, `undefined`, `[object Object]`,
`NaN`, datas ISO (`/\d{4}-\d{2}-\d{2}T/`).

## 4. Varredura de rolagem lateral

Desligar a rede de segurança (`html, body { overflow-x: visible !important }`), e em
320, 360, 390 e 430px, por rota e com o modal aberto:

```js
const over = await page.evaluate(() => {
  const w = document.documentElement.clientWidth;
  return [...document.querySelectorAll('body *')]
    .filter(el => el.getBoundingClientRect().right > w + 1)
    .filter(el => !el.closest('[data-clip]'))
    .slice(0, 10).map(el => el.tagName + '.' + el.className);
});
```

Injetar também um texto longo sem espaços em títulos e células. Prove o detector com uma
`div` de 700px.

## 5. Capturas

Para cada tela tocada: 1440×900 e 390×844, com a lista, com o modal aberto e, se houver,
com o formulário. **Olhe as capturas** (montagem lado a lado ajuda). Recortes em
resolução cheia para detalhes pequenos (topo, badges).

Dicas de quem já tropeçou:

- área autenticada pode nunca chegar a "rede ociosa": navegue esperando o `commit` e mais
  um tempo fixo, ou espere por um elemento da tela;
- ponha no armazenamento do navegador uma resposta **real** de login;
- servidor de desenvolvimento com recarga a quente envelhece depois de muitas edições:
  reinicie antes de capturar;
- defeito que só aparece no pacote de produção existe: valide exportações e bibliotecas
  CommonJS com o build de produção.

## 6. Comparação com a referência

Na primeira tela de um projeto novo, compare lado a lado com a tela equivalente do
sistema de referência: casca, cabeçalho, barra, tabela, modal, formulário. A diferença
deve ser só as cores de realce, o logo e o conteúdo.

## 7. O relato da entrega

1. o que mudou (telas e peças);
2. o que foi conferido (testes, build, capturas, varreduras), com o resultado;
3. o que **não** foi feito ou depende do back;
4. o que precisa de decisão do dono.
