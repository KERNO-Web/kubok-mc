// Снимок середины смены фото в BTB (WebKit, телефон): призрак старого фото гаснет поверх нового
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const b = await pw.webkit.launch();
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
const p = await ctx.newPage();
await p.goto("http://localhost:5201/", { waitUntil: "load" });
const box = p.locator('[data-krug="btb"]');
await box.scrollIntoViewIfNeeded();
await p.waitForTimeout(1500);
await p.tap('[data-krug="btb"] .krug__nav[data-dir="1"]');
await p.waitForTimeout(450);
await p.locator('[data-krug="btb"] .krug__ph:not([hidden])').first().screenshot({ path: "/Users/sergey-mac/Vibecode/kubok-mc/.work/audit/shots/btb-mid.png" });
await p.waitForTimeout(1500);
await p.locator('[data-krug="btb"] .krug__ph:not([hidden])').first().screenshot({ path: "/Users/sergey-mac/Vibecode/kubok-mc/.work/audit/shots/btb-end.png" });
console.log(await p.evaluate(() => [document.querySelector('[data-krug="btb"] .krug__count').textContent, document.querySelectorAll(".krug__ghost").length]));
await b.close();
