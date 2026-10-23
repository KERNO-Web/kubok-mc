// Мобилка 390: снимки экран за экраном (как листает человек) начиная с заданной высоты
async (page) => {
  const browser = page.context().browser();
  const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true, userAgent: UA });
  const p = await ctx.newPage();
  await p.goto('http://localhost:5201/?' + Date.now(), { waitUntil: 'networkidle' });
  await p.waitForTimeout(2000);
  const H = await p.evaluate(() => document.body.scrollHeight);
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  const start = 4300, step = 780;
  let n = 0;
  const shots = [];
  for (let y = start; y < H; y += step) {
    await p.evaluate((t) => window.scrollTo({ top: t, behavior: 'instant' }), y);
    await p.waitForTimeout(1100);
    n++;
    const f = 'mv-' + String(n).padStart(2, '0') + '.jpg';
    await p.screenshot({ path: dir + f, type: 'jpeg', quality: 50 });
    shots.push(f + '@' + y);
  }
  await ctx.close();
  return shots;
}
