# 01 — Tokens

Toda cor, raio, sombra e fonte do painel vem de variáveis CSS `--adm-*`, declaradas
**dentro da classe `.adm`** (posta no elemento raiz do painel e no hospedeiro das mensagens
enquanto o painel está aberto). Nada disso alcança o site público, o login ou a área do
usuário final.

Regra: **traduzir papéis, não valores.** Cada projeto troca as duas cores de realce (e,
se quiser, a temperatura dos neutros). Os papéis não mudam.

## 1. Papéis

### Neutros (rampa de 11 tons entre sand e charcoal)

| Token | Papel |
| --- | --- |
| `neutro-0` | superfície de cartão e de campo (creme claro, **nunca branco puro**) |
| `neutro-50` | faixa de título de grupo, linha em hover, caixa de valor em leitura |
| `neutro-100` | hover de botão neutro, campo desabilitado, badge neutro, divisor leve |
| `neutro-200` | divisores, borda de ação de linha |
| `neutro-300` | borda de campo e de botão neutro, halo de foco |
| `neutro-400` | hover de borda, ícone desabilitado |
| `neutro-500` | ícone neutro (**nunca texto**) |
| `neutro-600` | texto de apoio, legenda, ajuda de campo, título de grupo |
| `neutro-700` | texto secundário, rótulo |
| `neutro-800` | texto principal, botão secundário (Salvar) |
| `neutro-900` | charcoal: topo, cabeçalho de seção do menu |

O fundo da página é o **sand**; os cartões são `neutro-0`. O contraste entre os dois é o
que desenha a tela, não sombras.

### Realce 1 — `marca` (a cor da ação principal)

| Token | Papel |
| --- | --- |
| `marca-50` | fundo da linha com modal aberto, fundo do item atual do menu |
| `marca-200` | borda da linha aberta |
| `marca-300` | **botão primário** (um por tela), barras de gráfico |
| `marca-400` | hover do primário |
| `marca-500` | borda do primário |
| `marca-texto` | texto sobre o primário (branco se a cor for escura; `neutro-800` se for clara) |

### Realce 2 — `realce` (o detalhe que chama o olho)

Em dose pequena: ponto pulsante do item atual do menu, contador de pendência, pico de um
gráfico, o traço que se desenha sob o título da página. Tons `50`, `100`, `300`, `500`, `700`.
**Nunca** em botão, borda de cartão ou faixa lateral.

### Estados (4 famílias × 5 tons)

| Família | Matiz | Uso |
| --- | --- | --- |
| `sucesso` | verde | "Ativo", "Aprovado", "Sim", confirmação |
| `alerta` | **âmbar-laranja, nunca amarelo** | "Pendente", "Aguardando", "Vence em breve" |
| `erro` | vermelho | validação, falha, exclusão, "Recusado" |
| `info` | azul | "Em análise", "Em andamento", ajuda |

Tons: **50** fundo de alerta · **100** fundo de badge · **300** borda · **500** sólido
(ícone, botão; texto branco ≥ 4,5:1) · **700** texto (≥ 6,3:1 sobre 50/100).

As cores de realce do projeto **não podem** se confundir com um estado. Se a marca for
verde, o verde de sucesso continua valendo só em badge/alerta, e a marca só em ação.

## 2. Folha de tokens (ponto de partida)

Paleta-base charcoal `#1E1E1C` e sand `#D8CBB3`. Os valores de `marca` e `realce` abaixo
são um exemplo (cobre e petróleo); a skill `/identidade` os troca pelos do projeto.

```css
.adm {
  /* Base */
  --adm-charcoal: #1e1e1c;
  --adm-sand: #d8cbb3;
  --adm-neutro-0: #fbf9f4;
  --adm-neutro-50: #f4efe5;
  --adm-neutro-100: #ece5d6;
  --adm-neutro-200: #ded3bd;
  --adm-neutro-300: #c9baa0;
  --adm-neutro-400: #a39682;
  --adm-neutro-500: #7f7667;
  --adm-neutro-600: #625b50;
  --adm-neutro-700: #46423a;
  --adm-neutro-800: #2b2a26;
  --adm-neutro-900: #1e1e1c;

  /* Realce 1: ação principal */
  --adm-marca-50: #eaf2f2;
  --adm-marca-200: #b9d3d4;
  --adm-marca-300: #1f5e63;
  --adm-marca-400: #184d51;
  --adm-marca-500: #123c40;
  --adm-marca-texto: #ffffff;

  /* Realce 2: detalhe */
  --adm-realce-50: #fbeee7;
  --adm-realce-100: #f6dccf;
  --adm-realce-300: #c8643a;
  --adm-realce-500: #a34d28;
  --adm-realce-700: #76361b;

  /* Estados: 50 fundo de alerta · 100 badge · 300 borda · 500 sólido · 700 texto */
  --adm-sucesso-50: #effaf0; --adm-sucesso-100: #d9f6dd; --adm-sucesso-300: #9bdda8;
  --adm-sucesso-500: #02853c; --adm-sucesso-700: #03642b;
  --adm-alerta-50: #fff5ee;  --adm-alerta-100: #fee8da;  --adm-alerta-300: #feb98b;
  --adm-alerta-500: #a75605;  --adm-alerta-700: #7e3f02;
  --adm-erro-50: #fff4f2;    --adm-erro-100: #ffe6e3;    --adm-erro-300: #ffb5ac;
  --adm-erro-500: #b6433c;    --adm-erro-700: #89322c;
  --adm-info-50: #f0f8ff;    --adm-info-100: #dfeffe;    --adm-info-300: #9cd1fe;
  --adm-info-500: #0674b6;    --adm-info-700: #02578b;

  /* Papéis derivados: o resto da interface só usa estes */
  --adm-fundo: var(--adm-sand);
  --adm-card-borda: #cdbfa5;
  --adm-sombra: 0 1px 3px rgba(30, 30, 28, 0.08);
  --adm-sombra-alta: 0 24px 64px rgba(30, 30, 28, 0.26);   /* modal e dropdown */
  --adm-texto: var(--adm-neutro-800);
  --adm-texto-suave: var(--adm-neutro-700);                /* rótulos */
  --adm-texto-apagado: var(--adm-neutro-600);              /* legendas, ajuda */
  --adm-foco-borda: var(--adm-neutro-800);
  --adm-foco-anel: var(--adm-neutro-300);
  --adm-raio: 6px;          /* controles */
  --adm-raio-card: 10px;    /* cartões e palco */
  --adm-raio-modal: 12px;

  /* Casca: topo e menu têm tons próprios */
  --adm-topo-fundo: var(--adm-charcoal);
  --adm-topo-borda: var(--adm-sand);
  --adm-topo-texto: #f3ede0;
  --adm-topo-apagado: #b8ad98;
  --adm-topo-hover: #35342f;
  --adm-topo-item: #403e38;
  --adm-topo-filete: #4a4740;
  --adm-topo-foco: #e8dfcd;
  --adm-menu-texto: #f1eadb;
  --adm-menu-secao: var(--adm-charcoal);
  --adm-menu-secao-hover: #2f2e2a;
  --adm-menu-largura: 14rem;

  --adm-fonte: var(--font-body);
  --adm-fonte-titulo: var(--font-heading);

  color: var(--adm-texto);
  font-family: var(--adm-fonte);
  -webkit-font-smoothing: antialiased;
}
```

Como gerar a rampa de um realce a partir de uma cor `C`: `300` = `C` (precisa de ≥ 4,5:1
contra o texto que vai por cima); `400` e `500` = `C` escurecida 12% e 24%; `200` = `C`
a 30% sobre `neutro-0`; `50` = `C` a 9% sobre `neutro-0`; `700` = `C` escurecida 40%.
Confira o contraste com uma ferramenta, não a olho.

## 3. Tipografia

| Uso | Fonte | Tamanho/peso |
| --- | --- | --- |
| Títulos (página, ficha do modal) | `--font-heading` (Poppins por padrão) | página 22px/650; ficha 18px/650 |
| Interface | `--font-body` (Nunito Sans por padrão) | tabela e menu 13px; campo 14px; apoio 12px |
| Título de grupo/seção | corpo | 12px/700, caixa-alta, `letter-spacing: .06em` |
| Códigos (CPF, número, sigla) | `--font-mono` (IBM Plex Mono) | 12,5px |

Pode trocar a família. **Não troque a escala**: 11–14px na interface, 18–22px nos títulos.

## 4. Medidas que se repetem

| Elemento | Medida |
| --- | --- |
| Topo | 64px de altura |
| Menu lateral | 14rem (224px) |
| Palco | cartão `neutro-0`, borda `card-borda`, raio 10px, padding 20px |
| Botão de barra | padding 7px 12px, 12px/600, raio 6px |
| Botão do modal | 34px de altura, 13px/600 |
| Campo de formulário | 38px de altura, 14px |
| Campo de busca/filtro | 34px de altura, 13px |
| Seta da linha | 30×30px, raio 6px |
| Badge | pílula, padding 3px 9px 3px 7px, 12px/600 |
| Modal | largura máx. 1320px, altura máx. `100vh - 32px`, raio 12px |
| Grade de formulário e de leitura | 12 colunas, `column-gap` 16–20px |
| Quebra da casca | 900px (menu vira gaveta) |
| Quebra de tabela | 640px (linhas viram cartões) |
| Quebra do modal | 760px (ficha empilha; campos em 1 coluna) |

## 5. Movimento

Leve e com função: entrada do modal (`opacity` + `translateY(6px)`, 160ms), abrir seção do
menu (180ms), pulso do ponto do item atual, traço do título que se desenha, números que
contam ao entrar na tela. **Toda** animação tem o desligamento em
`@media (prefers-reduced-motion: reduce)`.

## 6. Proibido

- Hex solto em componente. Faltou um papel? Crie o token.
- Branco puro como superfície e preto puro como texto.
- Gradiente decorativo, sombra para "dar profundidade" a cartão comum.
- A cor de realce como texto sobre fundo claro sem conferir contraste.
- Faixa colorida na borda esquerda de cartão, linha ou item.
