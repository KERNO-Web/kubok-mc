// Скрины экранов сверху вниз: node .work/audit/shots.mjs [webkit|chromium] [w] [h] [tag] [url]
// Кладёт в .work/audit/shots/<tag>-NN.png, плюс отчёт о памяти картинок.
import { createRequire } from "module";
import fs from "fs";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const eng = process.argv[2] || "webkit";
const w = Number(process.argv[3] || 390), h = Number(process.argv[4] || 844);
const tag = process.argv[5] || "m";
const url = process.argv[6] || "http://localhost:5201/";
const mobile = w < 768;
const dir = "/Users/sergey-mac/Vibecode/kubok-mc/.work/audit/shots/";
fs.mkdirSync(dir, { recursive: true });
const browser = await pw[eng].launch();
const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: mobile ? 3 : 1, isMobile: mobile, hasTouch: mobile });
const p = await ctx.newPage();
await p.goto(url, { waitUntil: "load" });
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(2200);
const H = await p.evaluate(() => document.documentElement.scrollHeight);
let k = 0;
for (let y = 0; y < H; y += h) {
  await p.evaluate((y) => scrollTo({ top: y, behavior: "instant" }), y);
  await p.waitForTimeout(900);
  await p.screenshot({ path: `${dir}${tag}-${String(k++).padStart(2, "0")}.png`, scale: "css" });
}
const mem = await p.evaluate(() => {
  const imgs = [...document.images].filter((i) => i.complete && i.naturalWidth);
  const px = imgs.reduce((s, i) => s + i.naturalWidth * i.naturalHeight, 0);
  return { n: imgs.length, decodedMB: Math.round(px * 4 / 1e6), top: imgs.map((i) => [i.naturalWidth * i.naturalHeight, i.src.replace(location.origin, "")]).sort((a, b) => b[0] - a[0]).slice(0, 8).map(([a, s]) => Math.round(a * 4 / 1e6) + "MB " + s) };
});
console.log(JSON.stringify({ H, shots: k, mem }));
await browser.close();
