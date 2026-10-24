// Сколько главного потока съедает отрисовка, пока страница стоит (WebKit, телефон).
// Для каждой точки страницы: 3 с простоя, суммируем «дыры» между кусочками JS дольше 6 мс (это время ушло на стиль/отрисовку).
// node .work/audit/busy.mjs [webkit|chromium] [css-подмена] [url]
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const eng = process.argv[2] || "webkit";
const css = process.argv[3] || "";
const url = process.argv[4] || "http://localhost:5201/";
const browser = await pw[eng].launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
const p = await ctx.newPage();
await p.goto(url, { waitUntil: "load" });
if (css) await p.addStyleTag({ content: css });
await p.evaluate(() => document.fonts.ready);
const H = await p.evaluate(() => document.documentElement.scrollHeight);
for (let y = 0; y < H; y += 700) { await p.evaluate((y) => scrollTo({ top: y, behavior: "instant" }), y); await p.waitForTimeout(150); }
const spots = [["cover", 0], ["event", 1400], ["krug-hunt", 4300], ["svoboda", 6200], ["btb", 9000], ["lower", 11200]];
const out = [];
for (const [name, y] of spots) {
  await p.evaluate((y) => scrollTo({ top: y, behavior: "instant" }), y);
  await p.waitForTimeout(800);
  const r = await p.evaluate(() => new Promise((done) => {
    const t0 = performance.now(); let last = t0, blocked = 0, frames = 0, longF = 0, lf = t0;
    const ch = new MessageChannel();
    ch.port1.onmessage = () => {
      const now = performance.now();
      if (now - last > 6) blocked += now - last;
      last = now;
      if (now - t0 < 3000) ch.port2.postMessage(0); else done({ blocked: Math.round(blocked), frames, longF });
    };
    const raf = (t) => { frames++; if (t - lf > 25) longF++; lf = t; if (performance.now() - t0 < 3000) requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
    ch.port2.postMessage(0);
  }));
  out.push({ name, ...r });
}
console.log(css ? "CSS: " + css.slice(0, 80) : "BASE");
console.table(out);
await browser.close();
