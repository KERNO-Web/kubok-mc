"""v17: HUNT — доска только фоном шапки (пустые полароиды не трогаем), контент по центру на дереве;
BTB без полос из лого; иконки соцсетей в контактах; параллакс логотипа в обложке (скролл + мышь). python3 .work/fix_v17.py"""
import json, pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
html = (R / "index.html").read_text()
css = (R / "style.css").read_text()
js = (R / "app.js").read_text()
icons = json.loads((R / ".work" / "icons.json").read_text())


def drop(s, start):
    return re.sub(r"^" + re.escape(start) + r"[^\n]*\n", "", s, flags=re.M)


# ---------- HUNT
head = re.search(r'    <section class="ev-head">.*?</section>\n', html, re.S).group(0)
html = html.replace(head, '''    <section class="ev-head">
      <div class="ev-head__in">
        <img class="ev-head__plate" src="assets/hunt-plate.png" alt="Кубок МЦ: HUNT, 1/4 финала" width="900" height="675">
        <p class="ev-head__date"><b>24 октября</b><span>Москва <i>·</i> 16+</span></p>
        <p class="ev-head__sub">Четыре пары турнира, три баттла main event вне сетки и&nbsp;Deathmatch Clash в&nbsp;один вечер.</p>
        <button class="btn btn--accent ev-head__btn" data-ticket="quarter">Купить билет</button>
      </div>
    </section>
''')
for start in [".board ", ".board__", ".ev-head__sub {", ".ev-head {"]:
    while re.search(r"^" + re.escape(start), css, re.M):
        css = drop(css, start)
css = css.replace("/* HUNT: настоящая нитка и булавки */", '''/* HUNT: шапка на их доске (доска = фон, контент на дереве по центру) */
.ev-head { position: relative; display: grid; place-items: center; min-height: clamp(620px, 92vh, 980px); padding: clamp(70px, 8vw, 110px) var(--gutter) clamp(50px, 6vw, 80px); background: radial-gradient(60% 55% at 50% 50%, rgba(20, 10, 4, .35), transparent 70%), url("assets/hunt-board2.webp") 50% 50% / cover no-repeat; box-shadow: inset 0 -60px 80px -30px #140d09, inset 0 60px 80px -30px #140d09; }
.ev-head__in { display: grid; justify-items: center; gap: 18px; width: min(100%, 560px); text-align: center; }
.ev-head__plate { width: min(100%, 470px); height: auto; rotate: -2deg; filter: drop-shadow(0 22px 26px rgba(0, 0, 0, .75)); }
.ev-head__date { display: inline-flex; align-items: baseline; gap: 14px; margin-top: 4px; padding: 12px 24px 10px; background: url("assets/hunt-paper.jpg") 0 0 / 100% 100%; color: #2b1d14; rotate: 1.2deg; filter: drop-shadow(0 10px 12px rgba(0, 0, 0, .6)); }
.ev-head__date b { font: 900 clamp(30px, 3.4vw, 46px)/1 var(--slab); text-transform: uppercase; color: #b8141b; white-space: nowrap; }
.ev-head__date span { font: 700 clamp(15px, 1.4vw, 19px)/1 var(--slab); text-transform: uppercase; color: #5b4636; white-space: nowrap; }
.ev-head__date i { font-style: normal; color: #b8141b; }
.ev-head__sub { max-width: 46ch; color: #f3e9d6; font: 500 18px/1.4 var(--text); text-shadow: 0 2px 12px rgba(0, 0, 0, .95), 0 0 24px rgba(0, 0, 0, .8); }
.ev-head__btn { min-height: 58px; padding: 0 34px; font-size: 21px; box-shadow: 0 14px 30px -10px rgba(0, 0, 0, .9); }

/* HUNT: настоящая нитка и булавки */''', 1)
css = drop(css, "  .ev-head { padding-inline: 8px; }")
js = js.replace('[".board__plate", "stamp"], [".board__strip, .board__note", "pop"], [".ev-head__sub", "up"],',
                '[".ev-head__plate", "stamp"], [".ev-head__date", "pop"], [".ev-head__sub, .ev-head__btn", "up"],', 1)
assert ".ev-head__plate" in js

# ---------- BTB: полосы из лого убрать
html = re.sub(r'    <div class="btb__strip[^"]*" aria-hidden="true"></div>\n', "", html)
assert "btb__strip" not in html
css = drop(drop(css, ".btb__strip {"), ".btb__strip--bottom")

# ---------- Контакты: логотипы соцсетей
NAMES = {"t.me": "telegram", "vk.com": "vk", "youtube": "youtube", "boosty": "boosty"}
def add_icon(m):
    a = m.group(0)
    key = next(v for k, v in NAMES.items() if k in a)
    return a.replace("<span>", f'<svg class="soc" viewBox="0 0 24 24" aria-hidden="true"><path d="{icons[key]}"/></svg><span>', 1)
nav = re.search(r'<nav class="final__links".*?</nav>', html, re.S).group(0)
html = html.replace(nav, re.sub(r"<a [^>]*>.*?</a>", add_icon, nav, flags=re.S))
assert html.count('class="soc"') == 4
css = drop(css, ".final__links a span::after")
css = css.replace(".final__links a { display: grid; gap: 6px;", ".final__links a { display: grid; grid-template-columns: auto minmax(0, 1fr); align-items: center; column-gap: 14px; row-gap: 4px;", 1)
css = css.replace(".final__links a i {", ".final__links .soc { grid-row: 1 / span 2; width: 40px; height: 40px; fill: currentColor; transition: scale .3s var(--ease), rotate .3s var(--ease); }\n.final__links a:hover .soc { scale: 1.12; rotate: -6deg; }\n.final__links a i {", 1)

# ---------- Обложка: параллакс логотипа (скролл сильнее + за мышью)
css = css.replace(".anim .cover__logo { translate: 0 calc(var(--hp, 0) * 12vh);",
                  ".anim .cover__logo { translate: calc(var(--mx, 0) * -26px) calc(var(--hp, 0) * -34vh + var(--my, 0) * -18px); scale: calc(1 + var(--hp, 0) * .18); opacity: calc(1 - var(--hp, 0) * 1.1);", 1)
css = css.replace(".anim .cover__bg, .anim .cover__fg { translate: 0 calc(var(--hp, 0) * 22vh);",
                  ".anim .cover__bg { translate: calc(var(--mx, 0) * 10px) calc(var(--hp, 0) * 26vh + var(--my, 0) * 8px); }\n.anim .cover__fg { translate: calc(var(--mx, 0) * 22px) calc(var(--hp, 0) * 26vh + var(--my, 0) * 12px); }\n.anim .cover__bg, .anim .cover__fg {", 1)
assert "--mx" in css
js = js.replace("  hero();\n", '''  hero();
  // за мышью: фон, логотип и люди смещаются на разную глубину
  cover.addEventListener("pointermove", (e) => {
    if (e.pointerType !== "mouse") return;
    cover.style.setProperty("--mx", (e.clientX / innerWidth - .5).toFixed(3));
    cover.style.setProperty("--my", (e.clientY / innerHeight - .5).toFixed(3));
  });
  cover.addEventListener("pointerleave", () => { cover.style.setProperty("--mx", 0); cover.style.setProperty("--my", 0); });
''', 1)
assert "--mx" in js

html = re.sub(r"style\.css\?v=\d+", "style.css?v=29", html)
html = re.sub(r"app\.js\?v=\d+", "app.js?v=22", html)
(R / "index.html").write_text(html)
(R / "style.css").write_text(css)
(R / "app.js").write_text(js)
print("ok")
