// Проверка v37: штамп «Нет в наличии» (ПК+телефон), схема зала на телефоне, касание организаторов, ники
async (page) => {
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('http://localhost:5201/?' + Date.now(), { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  const y = await page.evaluate(() => document.querySelector('.merch__row').getBoundingClientRect().top + scrollY);
  await page.evaluate((t) => scrollTo({ top: t - 120, behavior: 'instant' }), y);
  await page.waitForTimeout(1200);
  await page.screenshot({ path: dir + 'v37-merch.jpg', type: 'jpeg', quality: 50 });
  const desk = await page.evaluate(() => ({ btn: [...document.querySelectorAll('.tee__order')].map((b) => b.disabled + ':' + b.textContent), names: [...document.querySelectorAll('.slide figcaption')].map((f) => f.textContent.trim().slice(0, 60)) }));
  await page.hover('.org .org__stage');
  await page.waitForTimeout(600);
  const deskHover = await page.evaluate(() => getComputedStyle(document.querySelector('.org .org__ph--b')).opacity);

  const browser = page.context().browser();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const p = await ctx.newPage();
  p.on('pageerror', (e) => errs.push('m ' + e.message));
  await p.goto('http://localhost:5201/?' + Date.now(), { waitUntil: 'networkidle' });
  await p.waitForTimeout(1500);
  await p.tap('.cover__band .btn');
  await p.tap('.buy__opt--site');
  await p.waitForTimeout(400);
  await p.screenshot({ path: dir + 'v37-hall.jpg', type: 'jpeg', quality: 60, clip: { x: 0, y: 190, width: 390, height: 240 } });
  const hall = await p.evaluate(() => {
    const t = [...document.querySelectorAll('.hall text')]; const fix = document.querySelector('.hall__fix').getBoundingClientRect();
    const j = t.find((x) => x.textContent === 'СУДЬИ').getBoundingClientRect();
    const ring = document.querySelector('.hall [data-zone=ring]').getBoundingClientRect(); const arc = t.find((x) => x.textContent.includes('ПРОХОД')).getBoundingClientRect();
    return { judgesInside: j.left >= fix.left && j.right <= fix.right && j.top >= fix.top - 1 && j.bottom <= fix.bottom + 1, arcInsideRing: arc.left >= ring.left && arc.right <= ring.right && arc.top >= ring.top };
  });
  await p.keyboard.press('Escape');
  // мерч на телефоне
  await p.evaluate(() => { const e = document.querySelector('.merch-zone'); window.scrollTo({ top: e.getBoundingClientRect().top + scrollY + 120, behavior: 'instant' }); });
  await p.waitForTimeout(900);
  await p.screenshot({ path: dir + 'v37-m-merch.jpg', type: 'jpeg', quality: 50 });
  await p.tap('.merch-zone .tee:nth-child(2) .tee__order');
  await p.waitForTimeout(400);
  const mo = await p.evaluate(() => [...document.querySelectorAll('.buy--merch input[name=tee]')].map((i) => i.value + (i.disabled ? '(нет)' : '') + (i.checked ? '*' : '')));
  await p.keyboard.press('Escape');
  // организаторы: касание
  await p.evaluate(() => { const e = document.querySelector('.org'); window.scrollTo({ top: e.getBoundingClientRect().top + scrollY - 80, behavior: 'instant' }); });
  await p.waitForTimeout(500);
  await p.tap('.org .org__stage');
  await p.waitForTimeout(600);
  const tap1 = await p.evaluate(() => getComputedStyle(document.querySelector('.org .org__ph--b')).opacity);
  await p.tap('.org .ofr');
  await p.waitForTimeout(500);
  const ofr1 = await p.evaluate(() => [getComputedStyle(document.querySelector('.org .ofr img')).filter, document.querySelector('.lb').open]);
  await p.tap('.org .ofr');
  await p.waitForTimeout(500);
  const ofr2 = await p.evaluate(() => document.querySelector('.lb').open);
  await ctx.close();
  return { errs, desk, deskHover, hall, mo, tap1, ofr1, ofr2 };
}
