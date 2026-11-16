// Marca d'água: o símbolo do trilho no canto, por baixo das páginas de conteúdo (qpdf --underlay).
const { chromium } = require(process.env.PLAYWRIGHT || '/home/kvrt/Projects/boilerplate-frontend-angular/node_modules/playwright');
const fs = require('fs');
const { execSync } = require('child_process');
(async () => {
  const dir = __dirname;
  const sym = JSON.parse(fs.readFileSync(dir + '/icons/icons.json', 'utf8'))['train-track'];
  const html = `<html><head><style>@page{size:A4;margin:0}body{margin:0}
    .w{position:absolute;right:6mm;bottom:12mm;width:56mm;height:56mm;opacity:.06;color:#1e1e1c}.w svg{width:100%;height:100%;stroke-width:1}</style></head>
    <body><div style="width:210mm;height:297mm;position:relative"><div class="w">${sym}</div></div></body></html>`;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html);
  await page.pdf({ path: dir + '/wm.pdf', preferCSSPageSize: true, printBackground: true });
  await browser.close();
  const pages = execSync(`pdftotext -layout ${dir}/manual-base.pdf -`).toString().split('\f');
  const keep = [];
  pages.forEach((t, i) => { if (i > 0 && t.includes('Trilho · Manual do padrão') && /\d+\s*$/.test(t.trim())) keep.push(i + 1); });
  execSync(`qpdf ${dir}/manual-base.pdf --underlay ${dir}/wm.pdf --to=${keep.join(',')} --repeat=1 -- "${dir}/Manual-do-Trilho.pdf"`);
  fs.unlinkSync(dir + '/wm.pdf'); fs.unlinkSync(dir + '/manual-base.pdf');
  console.log('marca em', keep.length, 'páginas');
})();
