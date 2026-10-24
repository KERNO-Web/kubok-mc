// Аудит: грузит сайт как iPhone (WebKit или Chromium), собирает ошибки, 404, переполнение по ширине, вес страницы.
// node .work/audit/load.mjs [webkit|chromium] [url] [w] [h]
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const eng = process.argv[2] || "webkit";
const url = process.argv[3] || "http://localhost:5201/";
const w = Number(process.argv[4] || 390), h = Number(process.argv[5] || 844);
const mobile = w < 768;
const browser = await pw[eng].launch();
const ctx = await browser.newContext({
  viewport: { width: w, height: h }, deviceScaleFactor: mobile ? 3 : 2, isMobile: mobile && eng !== "firefox", hasTouch: mobile,
  userAgent: mobile ? "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" : undefined,
});
const p = await ctx.newPage();
const errs = [], fails = [];
p.on("console", (m) => { if (["error", "warning"].includes(m.type())) errs.push(m.type() + ": " + m.text()); });
p.on("pageerror", (e) => errs.push("pageerror: " + e.message));
p.on("requestfailed", (r) => fails.push("FAIL " + r.url() + " " + r.failure()?.errorText));
p.on("response", (r) => { if (r.status() >= 400) fails.push(r.status() + " " + r.url()); });
await p.goto(url, { waitUntil: "load" });
await p.waitForTimeout(1500);
// проскроллить всю страницу, чтобы лениво загрузилось всё
const H = await p.evaluate(() => document.documentElement.scrollHeight);
for (let y = 0; y < H; y += h * 0.8) { await p.evaluate((y) => scrollTo(0, y), y); await p.waitForTimeout(250); }
await p.waitForTimeout(1500);
const info = await p.evaluate(() => {
  const de = document.documentElement;
  const wide = [...document.querySelectorAll("body *")].filter((el) => {
    const r = el.getBoundingClientRect();
    if (r.width === 0) return false;
    let a = el; while (a && a !== document.body) { const cs = getComputedStyle(a); if (cs.position === "fixed" || /hidden|clip|auto|scroll/.test(cs.overflowX)) return false; a = a.parentElement; }
    return r.right > innerWidth + 1 || r.left < -1;
  }).slice(0, 20).map((el) => el.tagName + "." + String(el.className).slice(0, 40) + " L" + Math.round(el.getBoundingClientRect().left) + " R" + Math.round(el.getBoundingClientRect().right));
  const res = performance.getEntriesByType("resource");
  const bytes = res.reduce((s, r) => s + (r.encodedBodySize || 0), 0);
  const big = res.filter((r) => r.encodedBodySize > 300e3).map((r) => (r.encodedBodySize / 1e6).toFixed(2) + "MB " + r.name.replace(location.origin, ""));
  const imgs = [...document.images].filter((i) => i.complete && i.naturalWidth === 0 && i.src).map((i) => "BROKEN " + i.src);
  return { sw: de.scrollWidth, cw: de.clientWidth, H: de.scrollHeight, wide, nres: res.length, mb: (bytes / 1e6).toFixed(1), big, imgs };
});
console.log(JSON.stringify({ eng, w, info, errs, fails }, null, 1));
await browser.close();
