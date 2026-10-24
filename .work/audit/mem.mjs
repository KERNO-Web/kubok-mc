// Память картинок по папкам: натуральный размер против показанного (телефон 390, DPR 3)
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const w = Number(process.argv[2] || 390);
const browser = await pw.webkit.launch();
const ctx = await browser.newContext({ viewport: { width: w, height: 844 }, deviceScaleFactor: w < 768 ? 3 : 2, isMobile: w < 768, hasTouch: w < 768 });
const p = await ctx.newPage();
await p.goto(process.argv[3] || "http://localhost:5201/", { waitUntil: "load" });
const H = await p.evaluate(() => document.documentElement.scrollHeight);
for (let y = 0; y < H; y += 700) { await p.evaluate((y) => scrollTo({ top: y, behavior: "instant" }), y); await p.waitForTimeout(200); }
await p.waitForTimeout(1500);
const r = await p.evaluate(() => {
  const g = {};
  [...document.images].filter((i) => i.complete && i.naturalWidth).forEach((i) => {
    const k = i.src.replace(location.origin + "/", "").replace(/[^/]+$/, "") + (i.closest(".eps") ? " (eps)" : "");
    g[k] ??= { n: 0, mb: 0, shown: 0 };
    g[k].n++; g[k].mb += i.naturalWidth * i.naturalHeight * 4 / 1e6;
    g[k].shown = Math.max(g[k].shown, Math.round(i.getBoundingClientRect().width));
  });
  return Object.entries(g).map(([k, v]) => [k, v.n, Math.round(v.mb), v.shown]).sort((a, b) => b[2] - a[2]);
});
console.table(r);
await browser.close();
