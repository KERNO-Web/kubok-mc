// Скрины зон ивентов целиком: desktop 1440 и mobile 390. Вызов через Playwright run_code (filename).
async (page) => {
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  for (const [w, h, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto('http://localhost:5201/?' + Date.now());
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(1200);
    for (const id of ['event', 'svoboda', 'btb']) {
      const el = await page.$('#' + id);
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(900);
      await el.screenshot({ path: `${dir}v8-${id}-${tag}.png`, animations: 'disabled' });
    }
  }
  return 'ok';
}
