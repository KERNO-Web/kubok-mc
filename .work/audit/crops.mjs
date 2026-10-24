// Кропы элементов (WebKit, телефон 3x, без анимаций): node .work/audit/crops.mjs <tag> <sel1,sel2,...>
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const [tag, sels] = process.argv.slice(2);
const browser = await pw.webkit.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true, reducedMotion: "reduce" });
const p = await ctx.newPage();
await p.goto("http://localhost:5201/", { waitUntil: "load" });
await p.evaluate(() => document.fonts.ready);
let k = 0;
for (const sel of sels.split(",")) {
  const el = p.locator(sel).first();
  await el.scrollIntoViewIfNeeded();
  await p.waitForTimeout(700);
  await el.screenshot({ path: `/Users/sergey-mac/Vibecode/kubok-mc/.work/audit/shots/crop-${tag}-${k++}.png` });
}
await browser.close();
