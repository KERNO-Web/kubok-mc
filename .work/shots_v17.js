// v17: шапка HUNT, BTB, контакты (1440/390) + кадр обложки при прокрутке на 300px (параллакс).
async (page) => {
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  for (const [w, h, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto('http://localhost:5201/?' + Date.now());
    await page.waitForTimeout(2600);
    await page.evaluate(() => scrollTo(0, 300));
    await page.waitForTimeout(400);
    if (tag === 'd') await page.screenshot({ path: dir + 'v17-cover-scroll.png' });
    const H = await page.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < H; y += 400) { await page.evaluate((v) => scrollTo(0, v), y); await page.waitForTimeout(40); }
    await page.waitForTimeout(1000);
    for (const sel of ['.ev-head', '#btb .season__head', '#contacts']) {
      const el = await page.$(sel);
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(1300);
      await el.screenshot({ path: `${dir}v17-${sel.replace(/[^a-z]/g, '')}-${tag}.png`, animations: 'disabled' });
    }
  }
  return errs;
}
