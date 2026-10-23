// Проверка мобильных фиксов v35: снимки ключевых экранов (390) + свайпы + проверка меню
async (page) => {
  const browser = page.context().browser();
  const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
  const W = 360;
  const ctx = await browser.newContext({ viewport: { width: W, height: 780 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true, userAgent: UA });
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', (e) => errs.push(e.message));
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  await p.goto('http://localhost:5201/?' + Date.now(), { waitUntil: 'networkidle' });
  await p.waitForTimeout(2200);
  const at = async (sel, off, file) => {
    await p.evaluate(([s, o]) => { const e = document.querySelector(s); window.scrollTo({ top: e.getBoundingClientRect().top + scrollY + o, behavior: 'instant' }); }, [sel, off]);
    await p.waitForTimeout(1300);
    await p.screenshot({ path: dir + file, type: 'jpeg', quality: 50 });
  };
  await p.screenshot({ path: dir + 'v35s-cover.jpg', type: 'jpeg', quality: 50, clip: { x: 0, y: 560, width: W, height: 284 } });
  await at('.ev-head', -60, 'v35s-head.jpg');
  await at('.ev-grid', -70, 'v35s-grid.jpg');
  await at('.extra', -70, 'v35s-main.jpg');
  await at('.btb .season__poster', -420, 'v35s-btb.jpg');
  await at('.merch-zone', -60, 'v35s-merch.jpg');
  // меню
  await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
  await p.waitForTimeout(300);
  await p.tap('.mast__burger');
  await p.waitForTimeout(500);
  await p.screenshot({ path: dir + 'v35s-menu.jpg', type: 'jpeg', quality: 50 });
  await p.tap('.mast__nav a[href="#archive"]');
  await p.waitForTimeout(1200);
  const menu = await p.evaluate(() => [document.querySelector('.mast').classList.contains('is-open'), Math.round(document.querySelector('#archive').getBoundingClientRect().top)]);
  // свайпы настоящим касанием
  const cdp = await ctx.newCDPSession(p);
  const swipe = async (sel) => {
    await p.evaluate((s) => { const r = document.querySelector(s); window.scrollTo({ top: r.getBoundingClientRect().top + scrollY - 150, behavior: 'instant' }); r.scrollLeft = 0; }, sel);
    await p.waitForTimeout(500);
    const b = await p.evaluate((s) => { const r = document.querySelector(s).getBoundingClientRect(); return { top: r.top, h: r.height, left: r.left, w: r.width }; }, sel);
    const y = Math.round(b.top + Math.min(b.h / 2, 300)), x0 = Math.round(Math.min(b.left + b.w - 20, W - 30)), x1 = Math.max(20, Math.round(b.left + 10));
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] });
    for (let k = 1; k <= 10; k++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 - (x0 - x1) * k / 10, y }] }); await p.waitForTimeout(16); }
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await p.waitForTimeout(600);
    return sel + ' → ' + (await p.evaluate((s) => Math.round(document.querySelector(s).scrollLeft), sel));
  };
  const sw = [];
  for (const s of ['.extra .slides', '.moments--hunt .moments__row', '.krug--hunt .krug__row', '.moments--svoboda .moments__row', '.moments--btb .moments__row', '.merch-zone .merch__row']) sw.push(await swipe(s));
  // наложения и вылеты
  const lay = await p.evaluate(() => {
    const W = innerWidth, bad = [];
    for (const e of document.querySelectorAll('.bracket__list b, .gone figcaption, .slide figcaption b')) { if (e.scrollWidth > e.clientWidth + 2) bad.push('обрезан: ' + e.textContent.trim()); }
    const b = [...document.querySelectorAll('.bracket__list li')].map((li) => { const [l, r] = li.querySelectorAll('b'); const vs = li.querySelector('i').getBoundingClientRect(); return l.getBoundingClientRect().right <= vs.left + 1 && r.getBoundingClientRect().left >= vs.right - 1; });
    return { docW: document.documentElement.scrollWidth, W, bad, bracketOk: b.every(Boolean), grid: getComputedStyle(document.querySelector('.ev-grid')).gridTemplateColumns };
  });
  await ctx.close();
  return { errs, menu, sw, lay };
}
