// Ширина блока соцсетей в футере и раскладка по колонкам на разных ширинах окна
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const b = await pw.chromium.launch();
const p = await b.newPage();
await p.goto("http://localhost:5201/", { waitUntil: "load" });
const out = [];
for (const w of [768, 900, 1024, 1180, 1280, 1366, 1440, 1600, 1680, 1920, 2560]) {
  await p.setViewportSize({ width: w, height: 900 });
  await p.waitForTimeout(150);
  out.push(await p.evaluate((w) => { const l = document.querySelector(".final__links"); const cols = getComputedStyle(l).gridTemplateColumns.split(" ").length; return { w, box: Math.round(l.clientWidth), cols }; }, w));
}
console.table(out);
await b.close();
