// Скрины каруселей «Из круга» 1440/390, проверка стрелки и открытия фото на весь экран.
async (page) => {
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  const res = {};
  for (const [w, h, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto('http://localhost:5201/?' + Date.now());
    const H = await page.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < H; y += 400) { await page.evaluate((v) => scrollTo(0, v), y); await page.waitForTimeout(50); }
    for (const key of ['hunt', 'svoboda', 'btb']) {
      const el = await page.$(`[data-krug="${key}"]`);
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(1600);
      await el.screenshot({ path: `${dir}krug-${key}-${tag}.png`, animations: 'disabled' });
    }
    res[tag] = await page.evaluate(() => ({ hw: document.documentElement.scrollWidth, sheet: !!document.querySelector('#krug') }));
  }
  await page.setViewportSize({ width: 1440, height: 900 });
  const box = await page.$('[data-krug="btb"]');
  await box.scrollIntoViewIfNeeded();
  await page.click('[data-krug="btb"] .krug__nav[data-dir="1"]');
  await page.waitForTimeout(900);
  res.count = await page.$eval('[data-krug="btb"] .krug__count', (e) => e.textContent);
  await page.click('[data-krug="btb"] .krug__ph >> nth=3');
  await page.waitForTimeout(900);
  await page.screenshot({ path: dir + 'krug-lb.png' });
  res.lb = await page.$eval('.lb', (d) => d.open + ' ' + d.querySelector('.lb__count').textContent);
  return { errs, res };
}
