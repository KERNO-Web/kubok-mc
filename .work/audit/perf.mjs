// Замер плавности прокрутки по разделам: Chromium как телефон, CPU замедлен в 4 раза.
// node .work/audit/perf.mjs [url] [css-для-отключения-эффектов]
// Для каждого раздела: медленная прокрутка через него, доля кадров дольше 25 мс, время отрисовки (Paint+Raster) из трейса, площадь слоёв.
import { createRequire } from "module";
import fs from "fs";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const url = process.argv[2] || "http://localhost:5201/";
const extraCss = process.argv[3] || "";
const browser = await pw.chromium.launch({ args: ["--enable-gpu-rasterization"] });
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
const p = await ctx.newPage();
const cdp = await ctx.newCDPSession(p);
await p.goto(url, { waitUntil: "load" });
if (extraCss) await p.addStyleTag({ content: extraCss });
await p.evaluate(() => document.fonts.ready);
// прогреть: пролистать всё, чтобы картинки загрузились
const H = await p.evaluate(() => document.documentElement.scrollHeight);
for (let y = 0; y < H; y += 600) { await p.evaluate((y) => scrollTo({ top: y, behavior: "instant" }), y); await p.waitForTimeout(120); }
await p.evaluate(() => scrollTo({ top: 0, behavior: "instant" }));
await p.waitForTimeout(1500);
await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
const secs = await p.evaluate(() => ["cover", "#event .ev-head", "#event .ev-grid", "#archive", ".moments--hunt", ".krug--hunt", "#svoboda", ".krug--svoboda", "#btb", ".krug--btb", ".lower", ".merch-zone", "#contacts"].map((s) => {
  const el = document.querySelector(s.startsWith("#") || s.startsWith(".") ? s : "." + s);
  const r = el.getBoundingClientRect();
  return [s, Math.round(r.top + scrollY), Math.round(r.height)];
}));
const out = [];
for (const [name, top, h] of secs) {
  await p.evaluate((y) => scrollTo({ top: y, behavior: "instant" }), Math.max(0, top - 400));
  await p.waitForTimeout(400);
  await browser.startTracing(p, { categories: ["devtools.timeline", "disabled-by-default-devtools.timeline"] });
  // прокрутка по 6px за кадр, как пальцем
  const res = await p.evaluate(async ([from, to]) => {
    const d = [];
    let last = performance.now(), y = from;
    await new Promise((done) => {
      const f = (t) => { d.push(t - last); last = t; y += 6; scrollTo({ top: y, behavior: "instant" }); if (y < to) requestAnimationFrame(f); else done(); };
      requestAnimationFrame(f);
    });
    d.shift();
    const long = d.filter((x) => x > 25).length;
    const sorted = [...d].sort((a, b) => a - b);
    return { frames: d.length, long, p95: Math.round(sorted[Math.floor(d.length * .95)] || 0), max: Math.round(sorted[d.length - 1] || 0) };
  }, [Math.max(0, top - 400), Math.min(top + Math.min(h, 1600), top + h)]);
  const buf = await browser.stopTracing();
  const ev = JSON.parse(buf.toString()).traceEvents;
  const sum = (n) => Math.round(ev.filter((e) => e.name === n && e.dur).reduce((s, e) => s + e.dur, 0) / 1000);
  out.push({ name, ...res, paint: sum("Paint"), raster: sum("RasterTask"), layout: sum("Layout"), style: sum("UpdateLayoutTree"), script: sum("FunctionCall") });
}
await cdp.send("Emulation.setCPUThrottlingRate", { rate: 1 });
console.table(out);
await browser.close();
