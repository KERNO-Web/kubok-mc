// Контакт-листы фото ивентов с номерами: страница генерится из списка превью .work/pv.
async (page) => {
  const fs = require('fs');
  const dir = '/Users/sergey-mac/Vibecode/kubok-mc/.work/';
  const files = fs.readdirSync(dir + 'pv').filter((f) => f.endsWith('.jpg')).sort();
  for (const folder of ['HUNT', 'SVOBODA', 'BTB']) {
    const list = files.filter((f) => f.startsWith(folder + '__'));
    const html = `<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#111;display:grid;grid-template-columns:repeat(5,1fr);gap:4px;font:bold 22px monospace;color:#ff0}div{position:relative}img{width:100%;height:190px;object-fit:cover;display:block}b{position:absolute;left:4px;top:2px;background:#000;padding:0 4px}</style>` +
      list.map((f, i) => `<div><img src="http://localhost:5201/.work/pv/${f}"><b>${i + 1}</b></div>`).join('');
    fs.writeFileSync(dir + 'contact.html', html);
    await page.setViewportSize({ width: 1500, height: 900 });
    await page.goto('http://localhost:5201/.work/contact.html?' + Date.now());
    await page.waitForTimeout(1200);
    await page.screenshot({ path: `${dir}zoom/contact-${folder}.png`, fullPage: true });
    fs.writeFileSync(`${dir}zoom/contact-${folder}.txt`, list.map((f, i) => `${i + 1} ${f}`).join('\n'));
  }
  return files.length;
}
