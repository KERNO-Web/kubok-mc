// v13: кадр интро обложки на 0.5с, затем прокрутка всей страницы (чтобы сработали появления) и скрины секций 1440/390.
async (page) => {
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  const out = {};
  for (const [w, h, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto('http://localhost:5201/?' + Date.now());
    await page.waitForTimeout(500);
    if (tag === 'd') await page.screenshot({ path: dir + 'v13-intro.png' });
    await page.waitForTimeout(1800);
    await page.screenshot({ path: `${dir}v13-cover-${tag}.png` });
    const H = await page.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < H; y += 400) { await page.evaluate((v) => scrollTo(0, v), y); await page.waitForTimeout(60); }
    await page.waitForTimeout(1500);
    for (const id of ['event', 'svoboda', 'btb', 'archive']) {
      const el = await page.$('#' + id);
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(1700);
      await el.screenshot({ path: `${dir}v13-${id}-${tag}.png`, animations: 'disabled' });
    }
    out[tag] = await page.evaluate(() => ({ rv: document.querySelectorAll('.rv').length, notIn: document.querySelectorAll('.rv:not(.in)').length, hw: document.documentElement.scrollWidth }));
  }
  return { errs, out };
}
