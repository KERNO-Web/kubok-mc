// Мерч и контакты 1440/390 + проверка переключения стороны футболки.
async (page) => {
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  const res = {};
  for (const [w, h, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto('http://localhost:5201/?' + Date.now());
    const H = await page.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < H; y += 400) { await page.evaluate((v) => scrollTo(0, v), y); await page.waitForTimeout(40); }
    await page.waitForTimeout(1200);
    for (const id of ['merch', 'contacts']) {
      const el = await page.$('#' + id);
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(1300);
      await el.screenshot({ path: `${dir}v16-${id}-${tag}.png`, animations: 'disabled' });
    }
    res[tag] = await page.evaluate(() => document.documentElement.scrollWidth);
  }
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.click('.tee >> nth=0 >> button[data-side="back"]');
  await page.waitForTimeout(700);
  res.side = await page.$eval('.tee', (t) => t.dataset.side);
  const el = await page.$('#merch');
  await el.screenshot({ path: dir + 'v16-merch-back.png', animations: 'disabled' });
  return { errs, res };
}
