// Диагностика свайпа «Лучших моментов» и Main Event на тач-телефоне: какой стиль блокирует жест
async (page) => {
  const browser = page.context().browser();
  const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true, userAgent: UA });
  const p = await ctx.newPage();
  await p.goto('http://localhost:5201/?' + Date.now(), { waitUntil: 'networkidle' });
  await p.waitForTimeout(2000);
  const cdp = await ctx.newCDPSession(p);
  const swipe = async (sel, css) => {
    await p.evaluate(([s, c]) => {
      document.getElementById('diag')?.remove();
      if (c) { const st = document.createElement('style'); st.id = 'diag'; st.textContent = c; document.head.append(st); }
      const r = document.querySelector(s); window.scrollTo({ top: r.getBoundingClientRect().top + scrollY - 150, behavior: 'instant' }); r.scrollLeft = 0;
    }, [sel, css]);
    await p.waitForTimeout(500);
    const b = await p.evaluate((s) => { const r = document.querySelector(s).getBoundingClientRect(); return { top: r.top, h: r.height, left: r.left, w: r.width }; }, sel);
    const y = Math.round(b.top + Math.min(b.h / 2, 300)), x0 = Math.round(Math.min(b.left + b.w - 20, 360)), x1 = Math.max(20, Math.round(b.left + 10));
    const hit = await p.evaluate(([px, py]) => { const e = document.elementFromPoint(px, py); return e ? e.tagName + '.' + String(e.className).slice(0, 24) : 'null'; }, [x0, y]);
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] });
    for (let k = 1; k <= 10; k++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 - (x0 - x1) * k / 10, y }] }); await p.waitForTimeout(16); }
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await p.waitForTimeout(600);
    const after = await p.evaluate((s) => Math.round(document.querySelector(s).scrollLeft), sel);
    return `${after} (палец ${x0}→${x1} y${y} в ${hit})`;
  };
  const out = {};
  const m = '.moments--svoboda .moments__row';
  out.base = await swipe(m, '');
  out.no3d = await swipe(m, '.moment__frame{transform:none!important;transform-style:flat!important}');
  out.noSnap = await swipe(m, '.moments__row{scroll-snap-type:none!important}');
  out.hunt = await swipe('.moments--hunt .moments__row', '');
  out.huntNo3d = await swipe('.moments--hunt .moments__row', '.moment__frame{transform:none!important;transform-style:flat!important}');
  out.slides = await swipe('.extra .slides', '');
  out.slidesInfo = await p.evaluate(() => { const g = document.querySelector('.ev-grid'); return getComputedStyle(g).gridTemplateColumns; });
  await ctx.close();
  return out;
}
