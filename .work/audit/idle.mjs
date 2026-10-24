// Перерисовки в простое (страница стоит, анимации идут): Chromium, телефон, CPU x4. node .work/audit/idle.mjs [url]
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const url = process.argv[2] || "http://localhost:5201/";
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
const p = await ctx.newPage();
const cdp = await ctx.newCDPSession(p);
await p.goto(url, { waitUntil: "load" });
await p.evaluate(() => document.fonts.ready);
const out = [];
for (const [name, y] of [["cover", 0], ["event", 1400], ["archive", 3000], ["svoboda", 6200], ["btb", 9000]]) {
  await p.evaluate((y) => scrollTo({ top: y, behavior: "instant" }), y);
  await p.waitForTimeout(1500);
  await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
  await browser.startTracing(p, { categories: ["devtools.timeline", "disabled-by-default-devtools.timeline"] });
  await p.waitForTimeout(3000);
  const ev = JSON.parse((await browser.stopTracing()).toString()).traceEvents;
  await cdp.send("Emulation.setCPUThrottlingRate", { rate: 1 });
  const f = (n) => ev.filter((e) => e.name === n && e.dur);
  out.push({ name, paints: f("Paint").length, paintMs: Math.round(f("Paint").reduce((s, e) => s + e.dur, 0) / 1000), rasterMs: Math.round(f("RasterTask").reduce((s, e) => s + e.dur, 0) / 1000) });
}
console.table(out);
await browser.close();
