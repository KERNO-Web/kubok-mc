// Прозрачность призрака во время смены фото BTB по времени (WebKit) + кадр, когда призрак виден наполовину
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const b = await pw.webkit.launch();
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
const p = await ctx.newPage();
await p.goto("http://localhost:5201/", { waitUntil: "load" });
await p.locator('[data-krug="btb"]').scrollIntoViewIfNeeded();
await p.waitForTimeout(1500);
const samples = await p.evaluate(async () => {
  document.querySelector('[data-krug="btb"] .krug__nav[data-dir="1"]').click();
  const out = [], t0 = performance.now();
  while (performance.now() - t0 < 1400) {
    await new Promise((r) => requestAnimationFrame(r));
    const g = document.querySelector(".krug__ghost");
    out.push(Math.round(performance.now() - t0) + ":" + (g ? (+getComputedStyle(g).opacity).toFixed(2) : "-"));
  }
  return out.filter((_, i) => i % 6 === 0).join(" ");
});
console.log(samples);
await b.close();
