"""v9: стиль ивентов только из их материалов. HUNT — доска 1/4 (их обложки), Св*бода — стена от Сергея + лист афиши,
BTB — обложки Back to Basics (чёрный, ч/б толпа, фуксия/фиолет, белый, жёлтый). Запуск один раз: python3 .work/skins_v9.py"""
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
html = (R / "index.html").read_text()
css = (R / "style.css").read_text()


def rep(s, old, new):
    assert old in s, old[:90]
    return s.replace(old, new)


def line(s, start, new):
    """заменить целую строку, начинающуюся с start"""
    m = re.search(r"^" + re.escape(start) + r"[^\n]*\n", s, re.M)
    assert m, start
    return s[:m.start()] + new + s[m.end():]


# ---------- HTML
html = rep(html, "&family=Sedgwick+Ave+Display&family=Permanent+Marker&family=Rubik+Spray+Paint", "")
html = re.sub(r'    <div class="sv__tags" aria-hidden="true">.*?</div>\n', "", html)
html = re.sub(r'  <filter id="hunt-grime".*?</filter>\n', "", html, flags=re.S)
html = rep(html, '<p class="ev-head__word">HUNT</p>',
           '<p class="ev-head__word"><img src="assets/hunt-logo.jpg" alt="Кубок МЦ: HUNT, 1/4 финала" width="285" height="180"></p>')
html = rep(html, '      <img class="season__poster" src="assets/poster-svoboda.jpg" alt="Афиша Св*бода" width="597" height="800" loading="lazy">\n', "")

# ---------- CSS: убрать придуманное
css = line(css, "  --dirt: url(", "")
for start in [".sv > .sv__tags", ".sv__tag {", ".sv__tag--sed", ".sv__tag--mark", ".sv__tag--spray",
              ".sv .tile:nth-child(4n+2)", ".sv .tile:nth-child(4n+3)", ".sv .tile:nth-child(4n+4)", "  .sv__tag:nth-child",
              ".ev-head__word { filter"]:
    css = line(css, start, "")

# ---------- HUNT: их доска 1/4 под тёмным фильтром, бумажные плашки, полароиды
css = line(css, ".event { position: relative;",
           '.event { position: relative; isolation: isolate; overflow: hidden; background: #140d09; }\n'
           '.event::before { content: ""; position: absolute; inset: -20px; z-index: -1; background: radial-gradient(120% 85% at 50% 35%, transparent 30%, rgba(0, 0, 0, .75)), url("assets/hunt-board.jpg") 50% 30% / cover; filter: blur(3px) brightness(.36) sepia(.25); }\n')
css = line(css, ".event::after {", '.event::after { content: ""; position: absolute; inset: 0; z-index: 5; pointer-events: none; background: var(--speck); opacity: .35; mix-blend-mode: screen; animation: grain .9s steps(5) infinite; }\n')
css = line(css, ".event img {", ".event .slide img { box-shadow: 0 18px 40px -14px rgba(0, 0, 0, .9); }\n")
css = line(css, ".event .gone img {", "")
css = line(css, ".ev-head__word {", ".ev-head__word img { width: clamp(220px, 22vw, 330px); height: auto; -webkit-mask: radial-gradient(closest-side, #000 72%, transparent); mask: radial-gradient(closest-side, #000 72%, transparent); }\n")
css = line(css, ".tag {", '.tag { display: inline-block; margin-bottom: 14px; padding: 9px 16px 7px; background: var(--noise), #e9e0ca; color: #8c1015; font: 900 19px/1 var(--slab); text-transform: uppercase; letter-spacing: .01em; box-shadow: inset 0 0 0 4px #e9e0ca, inset 0 0 0 6px #3b2f26, 0 8px 18px -8px rgba(0, 0, 0, .8); }\n')
css = line(css, ".tag--ink {", ".tag--ink { color: #1c1714; margin-top: 34px; }\n")
css = rep(css, "filter: grayscale(1); box-shadow: 0 0 0 3px #d9d0bf, 0 3px 10px 3px rgba(0, 0, 0, .6); }",
          "filter: grayscale(1) contrast(1.1); box-shadow: 0 0 0 4px #e9e0ca, 0 6px 14px 2px rgba(0, 0, 0, .7); }")
css = line(css, ".gone img {", ".gone img { width: 100%; aspect-ratio: 1; object-fit: cover; filter: grayscale(1) brightness(.75); box-shadow: 0 0 0 5px #e9e0ca, 0 8px 18px rgba(0, 0, 0, .7); }\n")
css = rep(css, "  .bracket__list img { width: 36px; height: 36px; box-shadow: 0 0 0 2px #efe8d8, 0 0 0 3px var(--fg); }",
          "  .bracket__list img { width: 36px; height: 36px; box-shadow: 0 0 0 3px #e9e0ca; }")

# ---------- Св*бода: стена от Сергея, лист под камерами
m = re.search(r"\.sv \{ position: relative; overflow: hidden; background:.*?\}\n", css, re.S)
css = css[:m.start()] + '.sv { position: relative; overflow: hidden; background: linear-gradient(rgba(10, 9, 11, 0) 30%, rgba(10, 9, 11, .55) 48%, rgba(10, 9, 11, .9) 62%, #0a090b 80%), url("assets/svoboda-wall.jpg") 50% 0 / 100% auto no-repeat, #0a090b; }\n' + css[m.end():]
css = line(css, ".sv .season__head {", ".sv .season__head { grid-template-columns: minmax(0, 1fr); justify-items: center; margin-top: clamp(130px, 19vw, 290px); }\n")
css = rep(css, ".sv__left { grid-column: 1; grid-row: 1 / span 2; align-self: stretch;", ".sv__left { grid-column: 1; grid-row: 1 / span 2; width: min(100%, 940px);")
css = line(css, ".sv__title img {", ".sv__title img { display: block; width: 100%; height: auto; margin: 0 auto; mix-blend-mode: multiply; }\n")
css = line(css, ".sv .season__poster {", "")
css = line(css, ".sv .tile__k {", ".sv .tile__k { color: #ff3b3b; }\n")
css = line(css, ".sv .tile img {", ".sv .tile img { box-shadow: 0 14px 30px -12px rgba(0, 0, 0, .8); }\n")
css = line(css, "  .sv .season__poster {", "")

# ---------- BTB: как их обложки
css = line(css, ".btb {", ".btb { position: relative; background: var(--speck), #060607; }\n")
css = rep(css, 'background: url("assets/logo-ink.svg") repeat-x left center / auto 20px, #ea0be0; border-block: 2px solid #f7f7f9; }',
          'background: url("assets/logo-ink.svg") repeat-x left center / auto 20px, #e7e4de; border-block: 2px solid #060607; }')
css = rep(css, "-webkit-text-stroke: .052em #f7f7f9;", "-webkit-text-stroke: .052em #060607;")
css = rep(css, 'color: #ea0be0; filter: url(#btb-ink); }', 'color: #f7f7f9; filter: url(#btb-ink); }\n.btb__word > span:nth-child(3) { color: #fdc931; }')
css = rep(css, "filter: grayscale(1) contrast(2.3) brightness(.85); box-shadow: 0 0 0 clamp(4px, .5vw, 7px) #f7f7f9; }",
          "filter: grayscale(1) contrast(1.5) brightness(.85); box-shadow: -16px 16px 0 #ea0be0, 16px -16px 0 #39088e; }")
css = line(css, ".btb__bar {", '.btb__bar { grid-column: 2; grid-row: 2; display: flex; align-items: center; gap: 16px; color: #fdc931; font: 400 34px/1 "Anton", var(--disp); text-transform: uppercase; letter-spacing: .02em; }\n.btb__bar::before, .btb__bar::after { content: ""; flex: 1; height: 4px; background: #fdc931; }\n.btb__bar::before { flex: 0 0 28px; }\n')
css = rep(css, ".btb__when i { font-style: normal; color: #ea0be0;", ".btb__when i { font-style: normal; color: #fdc931;")
css = line(css, ".btb .tile img {", ".btb .tile img { box-shadow: 0 14px 30px -12px rgba(0, 0, 0, .9); }\n")
css = line(css, ".btb .tile:hover img {", "")
css = rep(css, "font-size: 16px; color: #ea0be0; }", "font-size: 16px; color: #fdc931; }")

(R / "index.html").write_text(re.sub(r"style\.css\?v=\d+", "style.css?v=19", html))
(R / "style.css").write_text(css)
print("ok")
