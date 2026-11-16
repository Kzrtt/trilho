// Renderiza manual.html em PDF (Chromium do Playwright). PLAYWRIGHT=/caminho/para/playwright troca a instalação usada.
const { chromium } = require(process.env.PLAYWRIGHT || '/home/kvrt/Projects/boilerplate-frontend-angular/node_modules/playwright');
(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + dir + '/manual.html', { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  await page.pdf({ path: dir + '/manual-base.pdf', preferCSSPageSize: true, printBackground: true });
  await browser.close();
  console.log('pdf ok');
})();
