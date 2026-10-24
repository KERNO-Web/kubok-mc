// Прогон взаимодействий на телефоне (WebKit): меню, билеты, просмотр фото, доски, плееры, Main Event.
// node .work/audit/interact.mjs [webkit|chromium] [url]
import { createRequire } from "module";
import fs from "fs";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const eng = process.argv[2] || "webkit";
const url = process.argv[3] || "http://localhost:5201/";
const dir = "/Users/sergey-mac/Vibecode/kubok-mc/.work/audit/shots/";
const browser = await pw[eng].launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
const p = await ctx.newPage();
const errs = [];
p.on("pageerror", (e) => errs.push("pageerror: " + e.message));
p.on("console", (m) => { if (m.type() === "error") errs.push("console: " + m.text()); });
await p.route(/youtube|bibilet/, (r) => r.fulfill({ status: 200, contentType: "text/html", body: "<body style='background:#333'>stub</body>" }));
await p.goto(url, { waitUntil: "load" });
await p.waitForTimeout(1200);
const log = [];
const shot = async (n) => p.screenshot({ path: dir + "i-" + n + ".png", scale: "css" });
const swipe = async (sel, dx) => {
  const box = await p.locator(sel).first().boundingBox();
  const x = box.x + box.width / 2, y = box.y + box.height / 2;
  await p.evaluate(([sel, x, y, dx]) => {
    const el = document.querySelector(sel);
    const ev = (type, touches, changed) => { const e = new Event(type, { bubbles: true }); Object.defineProperty(e, "touches", { value: touches }); Object.defineProperty(e, "changedTouches", { value: changed }); return e; };
    const t = (cx) => ({ identifier: 1, target: el, clientX: cx, clientY: y });
    el.dispatchEvent(ev("touchstart", [t(x)], [t(x)]));
    el.dispatchEvent(ev("touchend", [], [t(x + dx)]));
  }, [sel, x, y, dx]);
};
// меню
await p.tap(".mast__burger");
await p.waitForTimeout(400);
log.push(["menu open", await p.evaluate(() => document.documentElement.classList.contains("menu-open"))]);
await shot("menu");
await p.tap(".mast__nav a[href='#btb']");
await p.waitForTimeout(1200);
log.push(["menu closed after link", await p.evaluate(() => !document.documentElement.classList.contains("menu-open")), "scrollY", await p.evaluate(() => Math.round(scrollY))]);
// билеты
await p.evaluate(() => scrollTo({ top: 0, behavior: "instant" }));
await p.waitForTimeout(300);
await p.tap(".cover__band [data-ticket]");
await p.waitForTimeout(500);
await shot("buy-pick");
await p.tap(".buy__opt--site");
await p.waitForTimeout(400);
await shot("buy-form");
await p.tap(".buy:not(.buy--merch) .buy__go");
await p.waitForTimeout(300);
log.push(["buy invalid fields", await p.evaluate(() => document.querySelectorAll(".buy .fld.is-bad").length)]);
await p.fill(".buy:not(.buy--merch) input[name=name]", "Тест");
await p.fill(".buy:not(.buy--merch) input[name=contact]", "@test");
await p.fill(".buy:not(.buy--merch) input[name=email]", "t@t.ru");
await p.tap(".buy:not(.buy--merch) [data-q='1']");
await p.tap(".buy:not(.buy--merch) .buy__go");
await p.waitForTimeout(400);
log.push(["buy done", await p.evaluate(() => document.querySelector(".buy").dataset.step), await p.evaluate(() => document.querySelector(".buy .buy__done-text").textContent)]);
await shot("buy-done");
await p.tap(".buy:not(.buy--merch) .buy__close");
await p.waitForTimeout(300);
// bibilet
await p.tap(".cover__band [data-ticket]");
await p.waitForTimeout(300);
await p.tap(".buy__opt[data-go='bibilet']");
await p.waitForTimeout(900);
await shot("drawer");
log.push(["drawer open", await p.evaluate(() => document.querySelector(".drawer").open)]);
await p.tap(".drawer__x");
await p.waitForTimeout(300);
// афиши
await p.locator(".ev-head [data-posters]").scrollIntoViewIfNeeded();
await p.tap(".ev-head [data-posters]");
await p.waitForTimeout(700);
await shot("posters");
await swipe(".lb", -120);
await p.waitForTimeout(400);
log.push(["lb after swipe", await p.evaluate(() => document.querySelector(".lb__count").textContent)]);
await p.tap(".lb__x");
await p.waitForTimeout(300);
// доски фото
for (const k of ["hunt", "svoboda", "btb"]) {
  const sel = `[data-krug="${k}"] .krug__row`;
  await p.locator(sel).scrollIntoViewIfNeeded();
  await p.waitForTimeout(500);
  const before = await p.evaluate((k) => document.querySelector(`[data-krug="${k}"] .krug__count`).textContent, k);
  await swipe(sel, -120);
  await p.waitForTimeout(2200);
  const after = await p.evaluate((k) => document.querySelector(`[data-krug="${k}"] .krug__count`).textContent, k);
  await p.tap(`[data-krug="${k}"] .krug__nav[data-dir="1"]`);
  await p.waitForTimeout(2200);
  const after2 = await p.evaluate((k) => document.querySelector(`[data-krug="${k}"] .krug__count`).textContent, k);
  const vis = await p.evaluate((k) => [...document.querySelectorAll(`[data-krug="${k}"] .krug__ph:not([hidden]) img`)].map((i) => i.src.split("/").slice(-1)[0] + (i.complete && i.naturalWidth ? "" : " NOTLOADED")), k);
  log.push(["board " + k, before, "→swipe", after, "→arrow", after2, vis.join(",")]);
  await shot("board-" + k);
  await p.tap(`[data-krug="${k}"] .krug__ph:not([hidden])`);
  await p.waitForTimeout(600);
  log.push(["lb " + k, await p.evaluate(() => document.querySelector(".lb").open), await p.evaluate(() => document.querySelector(".lb__img").src.split("/").slice(-2).join("/"))]);
  await shot("lb-" + k);
  await p.tap(".lb__x");
  await p.waitForTimeout(300);
}
// Main Event стрелки
await p.locator(".extra__view").scrollIntoViewIfNeeded();
await p.tap(".extra__nav--r");
await p.waitForTimeout(900);
log.push(["main event", await p.evaluate(() => document.querySelector(".extra__count").textContent)]);
// плеер HUNT: следующий, запуск
await p.locator("#archive .vp__nav [data-ep-step='1']").scrollIntoViewIfNeeded();
await p.tap("#archive .vp__nav [data-ep-step='1']");
await p.waitForTimeout(200);
log.push(["player next", await p.evaluate(() => document.querySelector("#archive .vp__n").textContent)]);
await p.tap("#archive .vp__poster");
await p.waitForTimeout(500);
log.push(["player iframe", await p.evaluate(() => !!document.querySelector("#archive .vp__screen iframe"))]);
await p.tap("#archive .stage[data-stage='1']");
await p.waitForTimeout(200);
log.push(["stage 1/4", await p.evaluate(() => document.querySelector("#archive .stage-panel").textContent.trim())]);
await shot("stage14");
// шортс
await p.locator(".moments--svoboda .moment__frame").first().scrollIntoViewIfNeeded();
await p.tap(".moments--svoboda .moment__frame");
await p.waitForTimeout(500);
log.push(["short iframe", await p.evaluate(() => !!document.querySelector(".moments--svoboda iframe"))]);
// мерч
await p.locator(".tee:not(.tee--sold) .tee__order").scrollIntoViewIfNeeded();
await p.tap(".tee:not(.tee--sold) .tee__order");
await p.waitForTimeout(500);
await shot("merch");
log.push(["merch dlg", await p.evaluate(() => document.querySelector(".buy--merch").open)]);
await p.tap(".buy--merch .buy__x");
// организаторы
await p.locator(".org__grid .ofr").first().scrollIntoViewIfNeeded();
await p.tap(".org__grid .ofr");
await p.waitForTimeout(300);
log.push(["org first tap colors", await p.evaluate(() => document.querySelector(".org__grid .ofr").classList.contains("is-color"))]);
await p.tap(".org__grid .ofr");
await p.waitForTimeout(500);
log.push(["org second tap lb", await p.evaluate(() => document.querySelector(".lb").open)]);
await p.tap(".lb__x");
for (const l of log) console.log(JSON.stringify(l));
console.log("ERRORS", JSON.stringify(errs));
await browser.close();
