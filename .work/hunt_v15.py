"""v15: HUNT пересобран на их доске. Шапка = доска расследования (металлическая табличка, дата на бумажной ленте,
билет на нижней ленте, main event в полароидах), деревянный фон, пары турнира на бумажных лентах, настоящие булавки
и нитки (вырезаны с доски) у шортсов, фото из круга и архива, подписи «1/8 финала» у прошлого. python3 .work/hunt_v15.py"""
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
html = (R / "index.html").read_text()
css = (R / "style.css").read_text()
js = (R / "app.js").read_text()


def line(s, start, new):
    m = re.search(r"^" + re.escape(start) + r"[^\n]*\n", s, re.M)
    assert m, start
    return s[:m.start()] + new + s[m.end():]


# Окна полароидов на доске (px исходника 1254): центр x, центр y, ширина, высота, поворот, имя, фото
S = 1254
SLOTS = [
    (158, 178, 244, 254, -2, "Gokilla", "q-gokilla"),
    (1109, 148, 208, 206, 2, "Zeiman", "q-zeiman"),
    (167, 511, 200, 190, 17, "Микси", "q-miksi"),
    (1150, 468, 158, 168, 5, ".OTRIX", "q-otrix"),
    (168, 1030, 246, 242, -3, "Ями", "q-yami"),
    (1104, 815, 232, 232, -7, "Кения", "q-kenya"),
]
pct = lambda v: f"{v / S * 100:.2f}%"
slots = "\n".join(
    f'        <figure class="board__ph" style="--x:{pct(x)};--y:{pct(y)};--w:{pct(w)};--h:{pct(h)};--r:{r}deg">'
    f'<img src="assets/{f}.jpg" alt="{n}" width="415" height="465" loading="lazy"><figcaption>{n}</figcaption></figure>'
    for x, y, w, h, r, n, f in SLOTS)

head_old = re.search(r'    <section class="ev-head">.*?</section>\n', html, re.S).group(0)
head_new = f'''    <section class="ev-head">
      <div class="board">
        <img class="board__plate" src="assets/hunt-plate.png" alt="Кубок МЦ: HUNT, 1/4 финала" width="900" height="675">
        <p class="board__strip board__strip--date"><b>24 октября</b><span>Москва <i>·</i> 16+</span></p>
{slots}
        <button class="board__strip board__strip--ticket" data-ticket="quarter"><b>Купить билет</b><span>Bibilet</span></button>
        <p class="board__note">Main event <i>×3</i></p>
      </div>
      <p class="ev-head__sub">Четыре пары турнира, три баттла main event вне сетки и&nbsp;Deathmatch Clash в&nbsp;один вечер.</p>
    </section>
'''
html = html.replace(head_old, head_new)

# прошлый этап подписываем явно
html = html.replace('<h3 class="moments__h"><span class="tag">Моменты</span></h3>',
                    '<h3 class="moments__h"><span class="tag">Моменты <small>1/8 финала</small></span></h3>', 1)
html = html.replace('<h3 class="krug__h"><span class="tag">Из круга</span></h3>',
                    '<h3 class="krug__h"><span class="tag">Из круга <small>1/8 финала, 29 августа</small></span></h3>', 1)
assert html.count("<small>1/8 финала") == 2
html = re.sub(r"style\.css\?v=\d+", "style.css?v=26", html)
html = re.sub(r"app\.js\?v=\d+", "app.js?v=20", html)

# ---------- JS: настоящие нитки и булавки вместо SVG
js = re.sub(r"  // HUNT: красная нить провисает.*?new ResizeObserver\(thread\)\.observe\(row\);\n  }\n", "", js, flags=re.S)
assert "krug__thread" not in js
js = js.replace("\n// ---------- Анимации ----------", r'''
// HUNT: настоящая красная нитка (текстура с их доски) натянута от булавки к булавке; булавки тоже с доски.
// Слой кладётся в контейнер, который прокручивается (лента), иначе в сам блок.
const stringUp = (box, rowSel, cardSel) => {
  const row = $(rowSel, box);
  const layer = document.createElement("div");
  layer.className = "thr-layer";
  layer.setAttribute("aria-hidden", "true");
  const draw = () => {
    const host = getComputedStyle(row).display === "contents" ? box : row;
    if (layer.parentElement !== host) host.append(layer);
    const hr = host.getBoundingClientRect();
    const pts = $$(cardSel, box).map((el) => {
      const r = el.getBoundingClientRect();
      return [r.left + r.width / 2 - hr.left + host.scrollLeft, r.top - hr.top + host.scrollTop + 7];
    });
    layer.style.width = host.scrollWidth + "px";
    layer.style.height = host.scrollHeight + "px";
    layer.innerHTML = pts.slice(1).map(([x, y], i) => {
      const [px, py] = pts[i];
      const len = Math.hypot(x - px, y - py), ang = Math.atan2(y - py, x - px) * 180 / Math.PI;
      return `<i class="thr" style="left:${px}px;top:${py}px;width:${len}px;transform:rotate(${ang}deg)"></i>`;
    }).join("") + pts.map(([x, y]) => `<img class="pin" src="assets/pin.png" alt="" style="left:${x}px;top:${y}px">`).join("");
  };
  draw();
  addEventListener("load", draw);
  new ResizeObserver(draw).observe(box);
};
const huntMoments = $('[data-moments="hunt"]');
const huntKrug = $('[data-krug="hunt"]');
if (huntMoments) stringUp(huntMoments, ".moments__row", ".moment");
if (huntKrug) stringUp(huntKrug, ".krug__row", ".krug__ph");

// ---------- Анимации ----------''', 1)
js = js.replace('[".ev-head__word", "stamp"], [".ev-head__info, .ev-head .btn", "up"],', '[".board__plate", "stamp"], [".board__strip, .board__note", "pop"], [".ev-head__sub", "up"],', 1)
js = js.replace('[".moments--hunt .moment", "drop"], ', '', 1)
assert "board__plate" in js and '.moments--hunt .moment", "drop"' not in js

# ---------- CSS
INK, RED, PAPER = "#2b1d14", "#b8141b", "#e8dcc0"
css = line(css, ".event::before {", '.event::before { content: ""; position: absolute; inset: -20px; z-index: -1; background: radial-gradient(130% 90% at 50% 30%, transparent 35%, rgba(8, 4, 2, .7)), url("assets/hunt-wood.jpg") 50% 0 / cover; filter: brightness(.55) saturate(1.05); }\n')
css = line(css, ".ev-head {", f'''.ev-head {{ display: grid; justify-items: center; gap: 22px; padding: clamp(40px, 5vw, 70px) var(--gutter) 10px; max-width: 1440px; margin: 0 auto; }}
.board {{ position: relative; container-type: inline-size; width: min(100%, 900px, 92vh); aspect-ratio: 1; background: url("assets/hunt-board2.webp") 0 0 / 100% 100%; box-shadow: 0 40px 90px -30px rgba(0, 0, 0, .95); }}
.board__plate {{ position: absolute; left: 50%; top: 49%; width: 47%; height: auto; translate: -50% -50%; rotate: -2deg; filter: drop-shadow(0 2cqw 2.4cqw rgba(0, 0, 0, .75)); }}
.board__strip {{ position: absolute; display: flex; align-items: center; justify-content: center; gap: 2.4cqw; margin: 0; padding: 0; color: {INK}; font-family: var(--slab); text-transform: uppercase; background: none; }}
.board__strip b {{ font-weight: 900; line-height: 1; }}
.board__strip span {{ font: 700 2.1cqw/1 var(--slab); letter-spacing: .04em; color: #5b4636; }}
.board__strip--date {{ left: 28.3%; top: 11.4%; width: 46.3%; height: 7.6%; rotate: -.6deg; }}
.board__strip--date b {{ font-size: 4.7cqw; color: {RED}; letter-spacing: .01em; }}
.board__strip--date i {{ font-style: normal; color: {RED}; }}
.board__strip--ticket {{ left: 26.3%; top: 84.6%; width: 44.3%; height: 8.6%; cursor: pointer; transition: scale .25s var(--ease); }}
.board__strip--ticket b {{ padding: .8cqw 2cqw .6cqw; border: .45cqw solid {RED}; color: {RED}; font-size: 3.5cqw; rotate: -3deg; box-shadow: inset 0 0 0 .3cqw {PAPER}, inset 0 0 0 .5cqw {RED}; mix-blend-mode: multiply; }}
.board__strip--ticket:hover {{ scale: 1.04; }}
.board__strip--ticket:hover b {{ background: {RED}; color: {PAPER}; mix-blend-mode: normal; }}
.board__note {{ position: absolute; left: 50%; top: 75.5%; translate: -50% 0; rotate: 2deg; margin: 0; padding: .7cqw 1.6cqw .5cqw; background: var(--noise), {PAPER}; color: {INK}; font: 900 2.2cqw/1 var(--slab); text-transform: uppercase; box-shadow: 0 .8cqw 1.4cqw rgba(0, 0, 0, .55); }}
.board__note i {{ font-style: normal; color: {RED}; }}
.board__ph {{ position: absolute; left: var(--x); top: var(--y); width: var(--w); height: var(--h); margin: 0; translate: -50% -50%; rotate: var(--r); }}
.board__ph img {{ display: block; width: 100%; height: 100%; object-fit: cover; object-position: 50% 30%; filter: sepia(.25) contrast(1.08) brightness(.95); box-shadow: inset 0 0 0 1px rgba(0, 0, 0, .3); }}
.board__ph figcaption {{ position: absolute; left: 0; right: 0; top: calc(100% + .5cqw); text-align: center; color: {INK}; font: 900 2.3cqw/1 var(--slab); text-transform: uppercase; }}
.ev-head__sub {{ max-width: 52ch; text-align: center; color: #d8ccb6; font-size: 16px; }}
''')
for start in [".ev-head__word img", ".ev-head__line {", ".ev-head__line i", ".ev-head__sub {"]:
    if re.search(r"^" + re.escape(start), css, re.M) and start != ".ev-head__sub {":
        css = line(css, start, "")
# старый .ev-head__sub (второе вхождение) убрать
subs = [m.start() for m in re.finditer(r"^\.ev-head__sub \{", css, re.M)]
if len(subs) > 1:
    css = line(css[:subs[1]], "", "") if False else css[:subs[1]] + css[css.index("\n", subs[1]) + 1:]
css = line(css, "  .ev-head { grid-template-columns: minmax(0, 1fr); }", "  .ev-head { padding-inline: 8px; }\n")
css = line(css, "  .ev-head .btn { justify-self: start; }", "")

# ярлыки с настоящей булавкой
css = line(css, ".tag {", f'.tag {{ position: relative; display: inline-block; margin-bottom: 14px; padding: 9px 16px 7px; background: var(--noise), {PAPER}; color: {RED}; font: 900 19px/1 var(--slab); text-transform: uppercase; letter-spacing: .01em; rotate: -1deg; box-shadow: 0 8px 18px -8px rgba(0, 0, 0, .8); }}\n'
           '.tag::before { content: ""; position: absolute; left: -9px; top: -13px; width: 20px; height: 30px; background: url("assets/pin.png") center / contain no-repeat; filter: drop-shadow(2px 5px 3px rgba(0, 0, 0, .6)); }\n'
           f'.tag small {{ margin-left: 8px; font: 700 14px/1 var(--slab); color: #6b5442; }}\n')
css = line(css, ".tag--ink {", f".tag--ink {{ color: {INK}; margin-top: 34px; rotate: .8deg; }}\n")

# пары турнира на бумажных лентах с доски
css = line(css, ".bracket__list li {", f'.bracket__list {{ display: grid; gap: 12px; }}\n.bracket__list li {{ display: grid; grid-template-columns: 56px minmax(0, 1fr) auto minmax(0, 1fr) 56px; align-items: center; gap: 14px; padding: 12px 18px; background: url("assets/hunt-paper.jpg") 0 0 / 100% 100%; color: {INK}; rotate: -.5deg; filter: drop-shadow(0 8px 10px rgba(0, 0, 0, .55)); }}\n.bracket__list li:nth-child(2n) {{ rotate: .6deg; }}\n')
css = line(css, ".bracket__list li:first-child {", "")
css = line(css, ".bracket__list i {", f".bracket__list i {{ font: 900 26px var(--slab); font-style: normal; text-transform: uppercase; color: {RED}; }}\n")
css = line(css, "  .bracket__list li {", "  .bracket__list li { grid-template-columns: 36px minmax(0, 1fr) auto minmax(0, 1fr) 36px; gap: 8px; padding: 10px 10px; }\n")

# настоящие нитки и булавки вместо нарисованных
for start in [".moments--hunt .moment::before", ".krug--hunt .krug__ph::before", ".krug__thread {", ".krug__thread path"]:
    css = line(css, start, "")
css = line(css, ".archive::before, .archive::after {", '.archive::before, .archive::after { content: ""; position: absolute; top: -16px; width: 22px; height: 34px; background: url("assets/pin.png") center / contain no-repeat; filter: drop-shadow(2px 6px 3px rgba(0, 0, 0, .6)); }\n')
css = css.replace("/* СЕЗОНЫ: общее */", '''/* HUNT: настоящая нитка и булавки */
.thr-layer { position: absolute; left: 0; top: 0; z-index: 3; pointer-events: none; }
.thr { position: absolute; height: 9px; margin-top: -4.5px; transform-origin: 0 50%; background: url("assets/thread.png") 0 50% / auto 9px repeat-x; filter: drop-shadow(0 5px 2px rgba(0, 0, 0, .5)); }
.pin { position: absolute; width: 22px; height: auto; translate: -50% -60%; filter: drop-shadow(2px 7px 3px rgba(0, 0, 0, .6)); }
.moments--hunt { position: relative; }
.moments--hunt .moments__row { position: relative; }

/* СЕЗОНЫ: общее */''', 1)

(R / "index.html").write_text(html)
(R / "style.css").write_text(css)
(R / "app.js").write_text(js)
print("ok")
