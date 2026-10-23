// Замер плавности прокрутки: шагами по 40px за кадр сверху вниз, считаем кадры дольше 25 мс
async (page) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('http://localhost:5201/?' + Date.now());
  await page.waitForTimeout(2500);
  return page.evaluate(async () => {
    const res = {};
    for (const [name, from, to] of [['cover', 0, 1800], ['all', 0, document.body.scrollHeight - innerHeight]]) {
      scrollTo(0, from);
      await new Promise((r) => setTimeout(r, 400));
      const d = [];
      let last = performance.now(), y = from;
      await new Promise((done) => {
        const step = (t) => {
          d.push(t - last); last = t; y += 40; scrollTo(0, y);
          if (y < to) requestAnimationFrame(step); else done();
        };
        requestAnimationFrame(step);
      });
      d.shift();
      const long = d.filter((x) => x > 25).length;
      res[name] = { frames: d.length, long, avg: +(d.reduce((a, b) => a + b, 0) / d.length).toFixed(1), max: Math.round(Math.max(...d)) };
    }
    return res;
  });
}
