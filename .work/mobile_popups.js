// Мобилка 390: попап покупки (выбор, форма со схемой зала), заказ мерча, просмотр фото, шапка HUNT
async (page) => {
  const browser = page.context().browser();
  const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true, userAgent: UA });
  const p = await ctx.newPage();
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  await p.goto('http://localhost:5201/?' + Date.now(), { waitUntil: 'networkidle' });
  await p.waitForTimeout(2000);
  await p.tap('.cover__band .btn');
  await p.waitForTimeout(500);
  await p.screenshot({ path: dir + 'mp-pick.jpg', type: 'jpeg', quality: 50 });
  await p.tap('.buy__opt--site');
  await p.waitForTimeout(400);
  await p.screenshot({ path: dir + 'mp-form.jpg', type: 'jpeg', quality: 50 });
  const hall = await p.evaluate(() => { const r = document.querySelector('.hall').getBoundingClientRect(); const d = document.querySelector('.buy'); return { hallW: Math.round(r.width), hallH: Math.round(r.height), dlgW: Math.round(d.getBoundingClientRect().width), scrollH: d.scrollHeight, clientH: d.clientHeight }; });
  await p.keyboard.press('Escape');
  await p.evaluate(() => { const t = document.querySelector('.tee__order'); scrollTo({ top: t.getBoundingClientRect().top + scrollY - 300, behavior: 'instant' }); });
  await p.waitForTimeout(400);
  await p.tap('.tee__order');
  await p.waitForTimeout(400);
  await p.screenshot({ path: dir + 'mp-merch.jpg', type: 'jpeg', quality: 50 });
  await p.keyboard.press('Escape');
  await p.evaluate(() => { const k = document.querySelector('.krug--svoboda .krug__ph'); scrollTo({ top: k.getBoundingClientRect().top + scrollY - 300, behavior: 'instant' }); });
  await p.waitForTimeout(500);
  await p.tap('.krug--svoboda .krug__ph');
  await p.waitForTimeout(600);
  await p.screenshot({ path: dir + 'mp-lb.jpg', type: 'jpeg', quality: 50 });
  const lb = await p.evaluate(() => document.querySelector('.lb').open);
  await ctx.close();
  return { hall, lb };
}
