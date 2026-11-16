# Manual do Trilho

`Manual-do-Trilho.pdf` é o manual pronto. Para gerar de novo:

```bash
python3 -I build.py && node pdf.cjs && node wm.cjs
```

- `build.py` monta `manual.html` (conteúdo e estilo num arquivo só).
- `pdf.cjs` e `wm.cjs` usam o Playwright; aponte `PLAYWRIGHT=/caminho/node_modules/playwright` se o padrão não existir. A marca d'água precisa de `qpdf` e `pdftotext`.
- `img/`: capturas do Fibro+ (`fb-*`, dados fictícios) e do Urban Pass (`up-*`, ambiente de testes).
- `diagramas/`: fichas JSON e SVGs gerados com o projeto canvas, com as cores trocadas para a paleta do manual.
- `icons/icons.json`: ícones Lucide usados.
