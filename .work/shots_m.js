// Скрины блоков «Моменты» 1440/390 + проверка запуска шортса по клику.
async (page) => {
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  for (const [w, h, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto('http://localhost:5201/?' + Date.now());
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(1000);
    for (const key of ['hunt', 'svoboda', 'btb']) {
      const el = await page.$(`[data-moments="${key}"]`);
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(900);
      await el.screenshot({ path: `${dir}mom-${key}-${tag}.png`, animations: 'disabled' });
    }
  }
  await page.setViewportSize({ width: 1440, height: 900 });
  const b = await page.$('[data-moments="svoboda"] [data-short]');
  await b.scrollIntoViewIfNeeded();
  await b.click();
  await page.waitForTimeout(2500);
  const src = await page.$eval('[data-moments="svoboda"] .is-on iframe', (f) => f.src);
  return { errs, src };
}
