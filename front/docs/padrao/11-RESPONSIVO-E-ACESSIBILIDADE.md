# 11 — Responsivo e acessibilidade

O painel é pensado para o computador (alvo 1366×768) e **funciona inteiro no celular**.

## 1. Quebras

| Largura | O que muda |
| --- | --- |
| ≥ 900px | casca completa: topo + menu lateral fixo |
| < 900px | menu vira **gaveta pela esquerda**; formulário em uma coluna; some o subtítulo do topo |
| < 760px | modal ocupa a tela; ficha empilha; campos de leitura em uma coluna |
| < 640px | **tabela vira cartões**; barra de ações empilha; paginação simplifica (‹ 3 de 12 ›) |

## 2. Só rolagem vertical (lei 16)

Rolagem lateral no celular é **defeito**, não estilo.

- Tabela vira cartões (cada célula recebe o rótulo do cabeçalho); nada de tabela que rola de lado.
- **Abas quebram de linha** (`flex-wrap`); nunca `overflow-x: auto`.
- Passos do guia e da linha do tempo quebram de linha.
- Texto longo sem espaço (e-mail, código, nome de arquivo): `overflow-wrap: anywhere` e
  `min-width: 0` nos filhos de `flex`/`grid`.
- Rede de segurança: `html, body { overflow-x: clip }`. Ela **esconde**, não corrige; ache a causa.

Auditoria: com a rede desligada, em 320, 360, 390 e 430px, em toda rota e com o modal
aberto, nenhum elemento pode passar da largura da tela (roteiro em [`15`](15-VERIFICACAO.md)).

## 3. Toque

- Alvo mínimo de 40×40px para o que se toca.
- Nada depende de `hover`: o que aparece no hover também aparece no foco e tem alternativa visível.
- Arrastar sempre tem um botão/menu equivalente.
- Campo com o teclado certo (`inputmode="numeric"`, `type="email"`, `tel`).
- Modal e gaveta respeitam a barra do navegador (`100dvh`).

## 4. Teclado

- Tudo que se faz com o mouse se faz com o teclado, na ordem visual.
- **Foco sempre visível**: borda `neutro-800` + halo de 3px, ou contorno de 2px afastado
  2px sobre fundo colorido. Nunca `outline: 0` sem substituto.
- **Modal**: foco entra na caixa ao abrir, fica preso (Tab/Shift+Tab ciclam), Esc fecha,
  o foco volta para quem abriu.
- **Menu do perfil**: setas ↑/↓, Esc. **Guia**: setas ←/→, Home/End.
- Linha de tabela: a seta é um `button` de verdade; Enter/Espaço abrem.

## 5. Leitor de tela

| Peça | Marcação |
| --- | --- |
| Menu | `<nav aria-label="Menu principal">`; seção = `button` com `aria-expanded`; item atual `aria-current="page"` |
| Modal | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` = título |
| Confirmação | `role="alertdialog"` |
| Seta da linha | `aria-haspopup="dialog"`, `aria-label="Abrir detalhes de <nome>"` |
| Botão só de ícone | `title` + `aria-label` |
| Ícone decorativo | `aria-hidden="true"` |
| Abas | `role="tablist"`/`tab`/`tabpanel`, `aria-selected` |
| Campo | `<label for>`; erro ligado por `aria-describedby`, `aria-invalid` |
| Toast | `role="status"`; erro `role="alert"` |
| Guia | passo com `aria-expanded`; texto em região `aria-live="polite"` |
| Tabela | `<th scope="col">`; coluna ordenada com `aria-sort` |

## 6. Cor e contraste

- Texto ≥ 4,5:1; título grande ≥ 3:1; componente e foco ≥ 3:1.
- `neutro-500` só em ícone; texto pequeno a partir de `neutro-600`.
- **Estado = cor + ícone + texto** (lei 9).
- Ao trocar as cores de realce, conferir: texto sobre `marca-300`; `marca-300` sobre
  `marca-50` (item atual do menu); badge `realce`.

## 7. Movimento

Toda animação tem o desligamento:

```css
@media (prefers-reduced-motion: reduce) {
  .adm *, .adm *::before, .adm *::after { animation: none !important; transition: none !important; }
}
```

Número que conta ao entrar na tela mostra o valor final de imediato com movimento
reduzido e quando não há suporte ao observador de interseção.

## 8. Idioma e leitura

- `lang="pt-BR"` no documento.
- Frases curtas, voz ativa. Sem abreviação que não seja de uso comum.
- Zoom de 200% sem perder conteúdo nem função.

## 9. Impressão

O que se imprime (ficha de registro, relatório, lista): sem topo, menu, botões, abas e
guia; com cabeçalho de impressão (sistema, entidade, data, quem imprimiu); cores de
estado mantidas com texto (não depender do fundo colorido).
