// Крупные кропы мест с шумом/зерном до и после: node .work/audit/look.mjs <tag> [eng] [url]
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const tag = process.argv[2], eng = process.argv[3] || "webkit", url = process.argv[4] || "http://localhost:5201/";
const dir = "/Users/sergey-mac/Vibecode/kubok-mc/.work/audit/shots/";
const browser = await pw[eng].launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true, reducedMotion: "reduce" });
const p = await ctx.newPage();
await p.goto(url, { waitUntil: "load" });
await p.evaluate(() => document.fonts.ready);
const bg = await p.evaluate(() => [getComputedStyle(document.querySelector(".tag")).backgroundImage.slice(0, 120), getComputedStyle(document.body, "::after").backgroundImage.slice(0, 120), getComputedStyle(document.body, "::after").animationName]);
console.log(JSON.stringify(bg));
for (const [sel, n] of [[".ev-head__date", "date"], [".archive .vp__t", "vpt"], [".bracket__list li", "pair"]]) {
  const el = p.locator(sel).first();
  await el.scrollIntoViewIfNeeded();
  await p.waitForTimeout(600);
  await el.screenshot({ path: `${dir}look-${tag}-${n}.png` });
}
await browser.close();
