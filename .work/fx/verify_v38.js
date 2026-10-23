// Проверка v38 на ПК: HUNT (виньетка, царапины), Св*бода (растр), BTB (аберрация в начале и после оседания)
async (page) => {
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  page.on('response', (r) => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('http://localhost:5201/?' + Date.now(), { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  const go = async (sel, off) => { const y = await page.evaluate((s) => document.querySelector(s).getBoundingClientRect().top + scrollY, sel); await page.evaluate((t) => scrollTo({ top: t, behavior: 'instant' }), y + off); };
  await go('.ev-grid', -80); await page.waitForTimeout(1500);
  await page.screenshot({ path: dir + 'v38-hunt.jpg', type: 'jpeg', quality: 70 });
  const vigOn = await page.evaluate(() => getComputedStyle(document.querySelector('.fx-vig')).opacity);
  await go('.moments--hunt', -60); await page.waitForTimeout(1200);
  await page.screenshot({ path: dir + 'v38-hunt2.jpg', type: 'jpeg', quality: 70, clip: { x: 0, y: 0, width: 720, height: 450 } });
  await go('#svoboda', 60); await page.waitForTimeout(1300);
  await page.screenshot({ path: dir + 'v38-sv.jpg', type: 'jpeg', quality: 70 });
  await go('.btb__head', -100); await page.waitForTimeout(250);
  const dxStart = await page.evaluate(() => document.querySelector('#ca-title feOffset').getAttribute('dx'));
  await page.screenshot({ path: dir + 'v38-btb-start.jpg', type: 'jpeg', quality: 70 });
  await page.waitForTimeout(1600);
  const dxEnd = await page.evaluate(() => document.querySelector('#ca-title feOffset').getAttribute('dx'));
  await page.screenshot({ path: dir + 'v38-btb-end.jpg', type: 'jpeg', quality: 70 });
  const vigOff = await page.evaluate(() => getComputedStyle(document.querySelector('.fx-vig')).opacity);
  return { errs, vigOn, vigOff, dxStart, dxEnd };
}
