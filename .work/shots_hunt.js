// HUNT целиком 1440/390 после прокрутки (появления сработали) + крупный кадр доски.
async (page) => {
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  for (const [w, h, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto('http://localhost:5201/?' + Date.now());
    const H = await page.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < H; y += 400) { await page.evaluate((v) => scrollTo(0, v), y); await page.waitForTimeout(50); }
    await page.waitForTimeout(1200);
    const b = await page.$('.board');
    await b.scrollIntoViewIfNeeded();
    await page.waitForTimeout(1500);
    await b.screenshot({ path: `${dir}h-board-${tag}.png` });
    const ev = await page.$('#event');
    await page.waitForTimeout(500);
    await ev.screenshot({ path: `${dir}h-event-${tag}.png`, animations: 'disabled' });
  }
  return errs;
}
