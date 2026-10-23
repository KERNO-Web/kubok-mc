// Скрины всей мобильной страницы кусками по 1500px (iPhone 390, тач) + повторный свайп лент «Лучшие моменты»
async (page) => {
  const browser = page.context().browser();
  const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true, userAgent: UA });
  const p = await ctx.newPage();
  await p.goto('http://localhost:5201/?' + Date.now(), { waitUntil: 'networkidle' });
  await p.waitForTimeout(2500);
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); } scrollTo(0, 0); });
  await p.waitForTimeout(1500);
  const H = await p.evaluate(() => document.body.scrollHeight);
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  let n = 0;
  for (let y = 0; y < H; y += 1500) {
    n++;
    await p.screenshot({ path: dir + 'm-' + String(n).padStart(2, '0') + '.jpg', type: 'jpeg', quality: 55, fullPage: true, clip: { x: 0, y, width: 390, height: Math.min(1500, H - y) } });
  }
  // свайп «Лучших моментов»: палец в середину видимой части ленты
  const cdp = await ctx.newCDPSession(p);
  const res = [];
  for (const sel of ['.moments--hunt .moments__row', '.moments--svoboda .moments__row', '.moments--btb .moments__row']) {
    await p.evaluate((s) => { const r = document.querySelector(s); scrollTo(0, r.getBoundingClientRect().top + scrollY - 200); r.scrollLeft = 0; }, sel);
    await p.waitForTimeout(400);
    const info = await p.evaluate((s) => { const r = document.querySelector(s).getBoundingClientRect(); return { top: r.top, h: r.height }; }, sel);
    const y = Math.min(info.top + info.h / 2, 700), x0 = 340, x1 = 60;
    const hit = await p.evaluate(([px, py]) => { const e = document.elementFromPoint(px, py); return e ? e.tagName + '.' + String(e.className).slice(0, 30) : 'null'; }, [x0, y]);
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] });
    for (let k = 1; k <= 8; k++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 - (x0 - x1) * k / 8, y }] }); await p.waitForTimeout(16); }
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await p.waitForTimeout(700);
    const after = await p.evaluate((s) => document.querySelector(s).scrollLeft, sel);
    res.push(`${sel}: → ${Math.round(after)} (палец в ${hit}, высота ленты ${Math.round(info.h)})`);
  }
  await ctx.close();
  return { chunks: n, H, res };
}
