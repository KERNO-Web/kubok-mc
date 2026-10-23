"""v14: «Из круга» каруселью в каждом ивенте (стиль ивента), просмотр фото на весь экран, старая ч/б плёнка #krug удалена.
python3 .work/krug_v14.py (один раз)"""
import json, pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
html = (R / "index.html").read_text()
css = (R / "style.css").read_text()
js = (R / "app.js").read_text()
krug = (R / ".work" / "krug.json").read_text()
BONE, RED = "#ebe4d8", "#d3161d"

# ---------- HTML
def block(key, head_cls):
    return (f'    <div class="krug krug--{key}" data-krug="{key}">\n'
            f'      <div class="krug__bar"><h3 class="krug__h"><span class="{head_cls}">Из круга</span></h3>'
            f'<span class="krug__count" aria-live="polite"></span>'
            f'<button class="krug__nav" data-dir="-1" aria-label="Назад">←</button><button class="krug__nav" data-dir="1" aria-label="Вперёд">→</button></div>\n'
            f'      <div class="krug__row" tabindex="0" aria-label="Фото из круга, листаются вбок"></div>\n    </div>\n')


def after_moments(s, key, head_cls):
    m = re.search(rf'    <div class="moments moments--{key}" data-moments="{key}">.*?\n    </div>\n', s, re.S)
    assert m, key
    return s[:m.end()] + block(key, head_cls) + s[m.end():]


html = after_moments(html, "hunt", "tag")
html = after_moments(html, "svoboda", "moments__pill")
html = after_moments(html, "btb", "moments__plate")
html = re.sub(r"  <!-- КАРКАС\. Из круга: плёнка едет вбок -->\n  <section class=\"sheet\".*?</section>\n\n", "", html, flags=re.S)
assert 'id="krug"' not in html
html = html.replace("<dialog class=\"drawer\"", '''<dialog class="lb" aria-label="Фото из круга">
    <img class="lb__img" alt="">
    <button class="lb__nav lb__nav--prev" data-dir="-1" aria-label="Предыдущее фото">←</button>
    <button class="lb__nav lb__nav--next" data-dir="1" aria-label="Следующее фото">→</button>
    <button class="lb__x" aria-label="Закрыть">×</button>
    <span class="lb__count"></span>
  </dialog>
<dialog class="drawer"''', 1)
assert 'class="lb"' in html
html = re.sub(r"style\.css\?v=\d+", "style.css?v=24", html)
html = re.sub(r"app\.js\?v=\d+", "app.js?v=18", html)

# ---------- JS: убрать плёнку, добавить карусели и просмотр
js = re.sub(r"\n// Ширина плёнки для горизонтального проезда.*?new ResizeObserver\(measure\)\.observe\(strip\);\n", "\n", js, flags=re.S)
assert "const strip" not in js
js = js.replace("const ARCHIVE = [", f"// Фото из круга по ивентам: [файл, ширина, высота], лучшие первыми (assets/krug/<ивент>/)\nconst KRUG = {krug};\n\nconst ARCHIVE = [", 1)
js = js.replace("\n// ---------- Анимации ----------", r'''
// Карусели «Из круга»: стрелки, счётчик, перетаскивание мышью, клик открывает фото на весь экран
const lb = $(".lb");
let lbList = [], lbIdx = 0;
const lbShow = (i) => {
  lbIdx = (i + lbList.length) % lbList.length;
  $(".lb__img", lb).src = lbList[lbIdx];
  $(".lb__count", lb).textContent = `${lbIdx + 1} / ${lbList.length}`;
};
$$(".lb__nav", lb).forEach((b) => b.addEventListener("click", () => lbShow(lbIdx + Number(b.dataset.dir))));
$(".lb__x", lb).addEventListener("click", () => lb.close());
lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") lbShow(lbIdx - 1); if (e.key === "ArrowRight") lbShow(lbIdx + 1); });

$$("[data-krug]").forEach((box) => {
  const key = box.dataset.krug;
  const row = $(".krug__row", box);
  const urls = KRUG[key].map(([f]) => `assets/krug/${key}/${f}.jpg`);
  row.innerHTML = KRUG[key].map(([f, w, h], i) => `
    <button class="krug__ph" data-i="${i}" aria-label="Открыть фото ${i + 1}">
      <img src="${urls[i]}" alt="" width="${w}" height="${h}" loading="lazy" draggable="false">
    </button>`).join("");
  const count = $(".krug__count", box);
  const items = $$(".krug__ph", row);
  const at = () => { const x = row.scrollLeft + 4; let i = 0; items.forEach((el, k) => { if (el.offsetLeft - row.offsetLeft <= x) i = k; }); return i; };
  const upd = () => { count.textContent = `${String(at() + 1).padStart(2, "0")} / ${items.length}`; };
  upd();
  row.addEventListener("scroll", upd, { passive: true });
  $$(".krug__nav", box).forEach((b) => b.addEventListener("click", () => {
    const i = Math.max(0, Math.min(items.length - 1, at() + Number(b.dataset.dir)));
    row.scrollTo({ left: items[i].offsetLeft - row.offsetLeft, behavior: "smooth" });
  }));
  // перетаскивание мышью; если тянули, клик не открывает фото
  let down = null, moved = false;
  row.addEventListener("pointerdown", (e) => { if (e.pointerType !== "mouse") return; down = { x: e.clientX, s: row.scrollLeft }; moved = false; row.classList.add("is-drag"); });
  addEventListener("pointermove", (e) => { if (!down) return; const dx = e.clientX - down.x; if (Math.abs(dx) > 5) moved = true; row.scrollLeft = down.s - dx; });
  addEventListener("pointerup", () => { if (!down) return; down = null; row.classList.remove("is-drag"); });
  row.addEventListener("click", (e) => {
    const b = e.target.closest(".krug__ph");
    if (!b || moved) return;
    lbList = urls;
    lb.dataset.skin = key;
    lbShow(Number(b.dataset.i));
    lb.showModal();
  });
});

// ---------- Анимации ----------''', 1)
js = js.replace('[".moments__h", "pop"],', '[".moments__h", "pop"], [".krug__h", "pop"], [".krug__ph", "side"],', 1)

# ---------- CSS: убрать плёнку
css = re.sub(r"/\* ИЗ КРУГА: плёнка \*/\n.*?\n}\n", "", css, flags=re.S)
assert ".sheet {" not in css
css = css.replace("/* СЕЗОНЫ: общее */", f'''/* ИЗ КРУГА: карусель фото в каждом ивенте */
.krug {{ max-width: 1440px; margin: clamp(48px, 5vw, 76px) auto 0; }}
.moments--hunt + .krug {{ margin-top: 0; padding: 0 var(--gutter) clamp(60px, 6vw, 90px); }}
.krug__bar {{ display: flex; align-items: center; gap: 10px; margin-bottom: 18px; }}
.krug__h {{ margin: 0 auto 0 0; }}
.krug__h .tag {{ margin: 0; }}
.krug__count {{ font: 500 16px var(--disp); color: var(--muted); margin-right: 6px; font-variant-numeric: tabular-nums; }}
.krug__nav {{ width: 46px; height: 46px; font: 700 20px var(--disp); transition: background-color .2s, color .2s, translate .2s; }}
.krug__nav:active {{ translate: 0 2px; }}
.krug__row {{ --h: clamp(220px, 25vw, 360px); display: flex; gap: clamp(14px, 1.4vw, 22px); overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; overscroll-behavior-x: contain; padding: 16px 4px 26px; cursor: grab; user-select: none; }}
.krug__row::-webkit-scrollbar {{ display: none; }}
.krug__row.is-drag {{ cursor: grabbing; scroll-snap-type: none; }}
.krug__ph {{ flex: none; scroll-snap-align: start; padding: 0; cursor: zoom-in; background: none; transition: translate .35s var(--ease); }}
.krug__row.is-drag .krug__ph {{ cursor: grabbing; }}
.krug__ph img {{ display: block; height: var(--h); width: auto; pointer-events: none; transition: filter .35s; }}
.krug__ph:hover {{ translate: 0 -6px; }}

/* HUNT: снимки на доске — кремовая рамка, наклон, булавка */
.krug--hunt .krug__nav {{ background: #e9e0ca; color: #8c1015; box-shadow: inset 0 0 0 2px #3b2f26; }}
.krug--hunt .krug__ph {{ position: relative; padding: 9px 9px 26px; background: var(--noise), #e9e0ca; box-shadow: 0 16px 30px -12px rgba(0, 0, 0, .9); rotate: -1.2deg; }}
.krug--hunt .krug__ph:nth-child(2n) {{ rotate: 1.3deg; translate: 0 10px; }}
.krug--hunt .krug__ph:nth-child(2n):hover {{ translate: 0 4px; }}
.krug--hunt .krug__ph::before {{ content: ""; position: absolute; z-index: 1; left: 50%; top: -8px; width: 16px; height: 16px; translate: -50% 0; border-radius: 50%; background: radial-gradient(circle at 35% 32%, #ff7a7a, #c3161d 50%, #5c070b); box-shadow: 0 4px 6px rgba(0, 0, 0, .55); }}
.krug--hunt .krug__ph img {{ height: calc(var(--h) - 35px); filter: sepia(.2) contrast(1.06) brightness(.92); }}
.krug--hunt .krug__ph:hover img {{ filter: none; }}

/* Св*бода: чёрная рама, как лист афиши */
.krug--svoboda .krug__nav {{ background: #111; color: #fff; border-radius: 50%; box-shadow: 0 0 0 2px rgba(255, 255, 255, .16); }}
.krug--svoboda .krug__nav:hover {{ background: #ff2f2f; }}
.krug--svoboda .krug__ph {{ border: 7px solid #0e0e0e; box-shadow: 0 22px 40px -14px rgba(0, 0, 0, .95); }}
.krug--svoboda .krug__ph img {{ height: calc(var(--h) - 14px); }}
.krug--svoboda .krug__ph:hover {{ box-shadow: 0 0 0 3px #ff2f2f, 0 22px 40px -14px rgba(0, 0, 0, .95); }}

/* BTB: костяная рамка и красные стрелки */
.krug--btb .krug__nav {{ background: {RED}; color: {BONE}; box-shadow: inset 0 0 0 2px {RED}, inset 0 0 0 3.5px {BONE}; }}
.krug--btb .krug__ph {{ box-shadow: 0 0 0 4px {BONE}, 0 22px 40px -14px rgba(0, 0, 0, .95); }}
.krug--btb .krug__ph:hover {{ box-shadow: 0 0 0 4px {RED}, 0 22px 40px -14px rgba(0, 0, 0, .95); }}

/* Просмотр фото на весь экран */
.lb {{ width: 100vw; height: 100vh; height: 100dvh; max-width: none; max-height: none; margin: 0; padding: 0; border: 0; background: rgba(6, 6, 7, .94); color: #fff; }}
.lb::backdrop {{ background: transparent; }}
.lb[open] {{ display: grid; place-items: center; animation: lbIn .3s var(--ease); }}
@keyframes lbIn {{ from {{ opacity: 0; }} }}
.lb__img {{ max-width: min(92vw, 1280px); max-height: 84vh; width: auto; height: auto; box-shadow: 0 30px 80px rgba(0, 0, 0, .8); }}
.lb[data-skin="hunt"] .lb__img {{ border: 10px solid #e9e0ca; border-bottom-width: 34px; }}
.lb[data-skin="svoboda"] .lb__img {{ border: 10px solid #0e0e0e; outline: 2px solid rgba(255, 255, 255, .12); }}
.lb[data-skin="btb"] .lb__img {{ outline: 5px solid {BONE}; }}
.lb__nav, .lb__x {{ position: absolute; width: 54px; height: 54px; font: 700 24px var(--disp); color: #fff; background: rgba(255, 255, 255, .08); transition: background-color .2s; }}
.lb__nav:hover, .lb__x:hover {{ background: {RED}; }}
.lb__nav--prev {{ left: 18px; top: 50%; translate: 0 -50%; }}
.lb__nav--next {{ right: 18px; top: 50%; translate: 0 -50%; }}
.lb__x {{ right: 18px; top: 18px; font-size: 32px; }}
.lb__count {{ position: absolute; left: 50%; bottom: 18px; translate: -50% 0; font: 500 16px var(--disp); color: rgba(255, 255, 255, .7); }}

/* СЕЗОНЫ: общее */''', 1)
css = css.replace("@media (max-width: 767px) {", '''@media (max-width: 767px) {
  .krug__row { --h: 230px; margin: 0 calc(-1 * var(--gutter)); padding-inline: var(--gutter); scroll-padding-inline: var(--gutter); }
  .krug__nav { display: none; }
  .lb__nav { top: auto; bottom: 10px; translate: none; }''', 1)

(R / "index.html").write_text(html)
(R / "style.css").write_text(css)
(R / "app.js").write_text(js)
print("ok")
