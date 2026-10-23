// Аудит мобилки: новый контекст с тачем (iPhone 390 и Android 360), автопроверки вёрстки и свайпа каруселей
async (page) => {
  const browser = page.context().browser();
  const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
  const report = {};
  for (const [w, h] of [[390, 844], [360, 780]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, userAgent: UA });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', (e) => errs.push(e.message));
    p.on('response', (r) => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
    await p.goto('http://localhost:5201/?' + Date.now(), { waitUntil: 'networkidle' });
    await p.waitForTimeout(2500);
    // прогрузить ленивое
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 80)); } scrollTo(0, 0); });
    await p.waitForTimeout(1200);
    const checks = await p.evaluate(() => {
      const W = innerWidth;
      const vis = (e) => { const s = getComputedStyle(e); return s.display !== 'none' && s.visibility !== 'hidden' && +s.opacity > 0.05; };
      const name = (e) => (e.id ? '#' + e.id : '') + (e.className && e.className.baseVal === undefined ? '.' + String(e.className).trim().split(/\s+/).slice(0, 2).join('.') : '') || e.tagName;
      const inScroller = (e) => { for (let a = e.parentElement; a; a = a.parentElement) { const s = getComputedStyle(a); if (/(auto|scroll|hidden|clip)/.test(s.overflowX) && a.scrollWidth > a.clientWidth + 2 && a !== document.body && a !== document.documentElement) return true; } return false; };
      // 1. горизонтальный скролл страницы
      const docW = document.documentElement.scrollWidth;
      // 2. элементы, торчащие за экран (не внутри горизонтальных лент)
      const out = [];
      for (const e of document.querySelectorAll('body *')) {
        if (!vis(e) || e.closest('dialog') || e.closest('.lower__bg') || e.closest('.cover')) continue;
        const r = e.getBoundingClientRect();
        if (r.width < 4 || r.height < 4) continue;
        if ((r.right > W + 1 || r.left < -1) && !inScroller(e)) out.push(name(e) + ` [${Math.round(r.left)}..${Math.round(r.right)}]`);
      }
      // 3. текст, обрезанный по ширине
      const clipped = [...document.querySelectorAll('h1,h2,h3,p,b,span,a,button,figcaption,li,i,em')].filter((e) => vis(e) && e.children.length === 0 && e.textContent.trim() && e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflow !== 'visible').map((e) => name(e) + ': ' + e.textContent.trim().slice(0, 30));
      // 4. мелкие тап-зоны
      const small = [...document.querySelectorAll('a, button, [role=button], input, label')].filter((e) => { if (!vis(e) || e.closest('dialog')) return false; const r = e.getBoundingClientRect(); return r.width > 0 && (r.width < 40 || r.height < 40); }).map((e) => { const r = e.getBoundingClientRect(); return name(e) + ` ${Math.round(r.width)}x${Math.round(r.height)} «${e.textContent.trim().slice(0, 18)}»`; });
      // 5. ленты: можно ли листать
      const rows = [...document.querySelectorAll('.krug__row, .slides, .moments__row, .tiles, .merch__row, .eps')].map((r) => { const s = getComputedStyle(r); return { sel: name(r) + ' in ' + name(r.closest('section,.event,[data-moments],[data-krug]') || r), ox: s.overflowX, sw: r.scrollWidth, cw: r.clientWidth, ta: s.touchAction, disp: s.display }; });
      // 6. мелкий текст
      const tiny = [...new Set([...document.querySelectorAll('p,span,b,i,a,figcaption,small,li')].filter((e) => vis(e) && e.children.length === 0 && e.textContent.trim().length > 2 && parseFloat(getComputedStyle(e).fontSize) < 12).map((e) => name(e) + ' ' + getComputedStyle(e).fontSize))].slice(0, 15);
      // 7. наложения в Main Event и шапке HUNT
      const overlaps = [];
      const boxes = [...document.querySelectorAll('.extra__bar, .extra__view, .slide figcaption, .extra__nav--big, .bracket, .gone, .ev-head__plate, .ev-head__date, .ev-head__sub, .ev-head__btn, .season__head > *, .btb__head > *, .sv__left, .season__poster')].filter(vis);
      for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i].getBoundingClientRect(), b = boxes[j].getBoundingClientRect();
        if (boxes[i].contains(boxes[j]) || boxes[j].contains(boxes[i])) continue;
        const ix = Math.min(a.right, b.right) - Math.max(a.left, b.left), iy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (ix > 6 && iy > 6) overlaps.push(name(boxes[i]) + ' × ' + name(boxes[j]) + ` ${Math.round(ix)}x${Math.round(iy)}`);
      }
      return { docW, W, out: [...new Set(out)].slice(0, 30), clipped: clipped.slice(0, 15), small: [...new Set(small)].slice(0, 25), rows, tiny, overlaps, pageH: document.body.scrollHeight };
    });
    // 8. настоящий свайп пальцем по каждой ленте (CDP touch)
    const cdp = await ctx.newCDPSession(p);
    const swipes = [];
    const rowsSel = ['.moments--hunt .moments__row', '.krug--hunt .krug__row', '.extra .slides', '.moments--svoboda .moments__row', '.krug--svoboda .krug__row', '.moments--btb .moments__row', '.krug--btb .krug__row'];
    for (const sel of rowsSel) {
      const has = await p.$(sel);
      if (!has) { swipes.push(sel + ': нет'); continue; }
      await p.evaluate((s) => { const r = document.querySelector(s); r.scrollIntoView({ block: 'center' }); r.scrollLeft = 0; }, sel);
      await p.waitForTimeout(400);
      const box = await has.boundingBox();
      const y = box.y + Math.min(box.height / 2, 120), x0 = Math.min(box.x + box.width - 30, w - 30), x1 = 40;
      const before = await p.evaluate((s) => document.querySelector(s).scrollLeft, sel);
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] });
      for (let k = 1; k <= 8; k++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 - (x0 - x1) * k / 8, y }] }); await p.waitForTimeout(16); }
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      await p.waitForTimeout(700);
      const after = await p.evaluate((s) => document.querySelector(s).scrollLeft, sel);
      const top = await p.evaluate(([px, py]) => { const e = document.elementFromPoint(px, py); return e ? (e.className && String(e.className).slice(0, 40)) || e.tagName : 'null'; }, [x0, y]);
      swipes.push(`${sel}: ${before}→${Math.round(after)} (палец попадает в: ${top})`);
    }
    report[w] = { errs: errs.slice(0, 5), ...checks, swipes };
    await ctx.close();
  }
  return report;
}
