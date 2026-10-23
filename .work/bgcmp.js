// BTB со старым и новым (фиолетовым) коллажем: подмена фона на лету, два скрина.
async (page) => {
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/zoom/';
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('http://localhost:5201/?' + Date.now());
  await page.evaluate(() => document.fonts.ready);
  const el = await page.$('#btb');
  await el.scrollIntoViewIfNeeded();
  await page.waitForTimeout(800);
  await el.screenshot({ path: dir + 'bg-old.png', animations: 'disabled' });
  await page.addStyleTag({ content: '.btb::before { background-image: linear-gradient(transparent 70%, #0b0a0a 92%), image-set(url("assets/btb-collage2.webp") 1x, url("assets/btb-collage2-2x.jpg") 2x) !important; }' });
  await page.waitForTimeout(1200);
  await el.screenshot({ path: dir + 'bg-new.png', animations: 'disabled' });
  return 'ok';
}
