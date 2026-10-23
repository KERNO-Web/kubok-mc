"""v8: идентичность ивентов. HUNT — тёмный андерграунд, Св*бода — граффити-стена, BTB — ретро (v2: чёрный+фуксия, фотокопия).
Запуск: python3 .work/skins_v8.py (идемпотентно не делать — запускать один раз)"""
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
html = (R / "index.html").read_text()
css = (R / "style.css").read_text()


def rep(s, old, new):
    assert old in s, old[:80]
    return s.replace(old, new)


# --- шрифты для тегов граффити
html = rep(html, "family=Archivo:wdth,wght@62,900&display=swap",
           "family=Archivo:wdth,wght@62,900&family=Sedgwick+Ave+Display&family=Permanent+Marker&family=Rubik+Spray+Paint&display=swap")
html = html.replace('width="1360" height="384"', 'width="2000" height="667"')

# --- теги на стене Св*боды (слова с их афиши)
tags = [
    ("karma", "sed", "#c6ff1a", 2, 3, -8, 1.0),
    ("legacy", "mark", "#ff2fb3", 64, 1, 5, .8),
    ("CHAINS", "spray", "#ff7a1a", 80, 6, -4, .9),
    ("infinity", "sed", "#29d3ff", -1, 42, 10, .8),
    ("new era", "mark", "#ff3b3b", 48, 40, -6, .7),
    ("survival", "sed", "#a66bff", 86, 44, 7, .75),
    ("XXIII", "spray", "#ffe01a", 30, 76, -3, 1.0),
    ("selection", "sed", "#ff2fb3", 70, 88, -5, .85),
    ("da shift", "mark", "#29d3ff", 4, 93, 4, .8),
]
spans = "".join(
    f'<span class="sv__tag sv__tag--{f}" style="--x:{x}%;--y:{y}%;--r:{r}deg;--s:{s};--c:{c}">{t}</span>'
    for t, f, c, x, y, r, s in tags)
html = rep(html, '<section class="season sv" id="svoboda" data-skin="svoboda">\n',
           '<section class="season sv" id="svoboda" data-skin="svoboda">\n    <div class="sv__tags" aria-hidden="true">' + spans + '</div>\n')

# --- фильтр «затёртый штамп» для HUNT
html = rep(html, '  <filter id="btb-ink"', '''  <filter id="hunt-grime" x="-2%" y="-2%" width="104%" height="104%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="3" xChannelSelector="R" yChannelSelector="G" result="rough"/>
    <feTurbulence type="fractalNoise" baseFrequency=".055" numOctaves="4" seed="11" result="w"/>
    <feColorMatrix in="w" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -2.6 0 0 0 1.55" result="holes"/>
    <feComposite in="rough" in2="holes" operator="in"/>
  </filter>
  <filter id="btb-ink"''')

# --- скины
css = rep(css, '[data-skin="hunt"] { --bg: #d6cfbd; --fg: #1b1614; --muted: #5a4f45; --accent: #6c0d10; }',
          '[data-skin="hunt"] { --bg: #110e0c; --fg: #ebe3d4; --muted: #9b9083; --accent: #c3161d; }')
css = rep(css, '[data-skin="svoboda"] { --bg: #0b0a1c; --fg: #f3f2f8; --muted: #aaa7c8; --accent: #ff2f2f; }',
          '[data-skin="svoboda"] { --bg: #1d1714; --fg: #f6f3ee; --muted: #c9c1b6; --accent: #ff2f2f; }')
css = rep(css, '[data-skin="btb"] { --bg: #d9d6d0; --fg: #141414; --muted: #55524c; --accent: #c4232a; }',
          '[data-skin="btb"] { --bg: #070608; --fg: #f7f7f9; --muted: #c5bfcc; --accent: #ea0be0; }')

# --- HUNT: грязь, зерно, тёмный фильтр
css = rep(css, '.event { background-image: var(--noise); }',
          '''.event { position: relative; isolation: isolate; background: radial-gradient(130% 90% at 50% 40%, transparent 35%, rgba(0, 0, 0, .7)), var(--dirt), var(--noise), var(--noise), #110e0c; }
.event::after { content: ""; position: absolute; inset: 0; z-index: 5; pointer-events: none; background: var(--speck); opacity: .5; mix-blend-mode: screen; animation: grain .9s steps(5) infinite; }
@keyframes grain { 0% { background-position: 0 0; } 20% { background-position: -37px 21px; } 40% { background-position: 53px -44px; } 60% { background-position: -12px 61px; } 80% { background-position: 29px 9px; } }
@media (prefers-reduced-motion: reduce) { .event::after { animation: none; } }
.event img { filter: grayscale(.35) sepia(.18) contrast(1.18) brightness(.78); }
.event .gone img { filter: grayscale(1) contrast(1.2) brightness(.7); }
.ev-head__word { filter: url(#hunt-grime); text-shadow: 0 0 40px rgba(195, 22, 29, .25); }''')
css = rep(css, '.tag--ink { background: var(--fg); margin-top: 34px; }', '.tag--ink { background: var(--fg); color: #110e0c; margin-top: 34px; }')
css = rep(css, 'box-shadow: 0 0 0 3px #efe8d8, 0 0 0 4px var(--fg); }', 'box-shadow: 0 0 0 3px #d9d0bf, 0 3px 10px 3px rgba(0, 0, 0, .6); }')
css = rep(css, '.card img { width: 100%; box-shadow: 0 18px 40px -16px rgba(50, 28, 16, .55); }', '.card img { width: 100%; box-shadow: 0 18px 40px -16px rgba(0, 0, 0, .9); }')

# --- Св*бода: кирпичная стена, баллоны, теги
old = re.search(r"\.sv \{ position: relative; overflow: hidden; background:[^\n]*\n", css).group(0)
css = css.replace(old, '''.sv { position: relative; overflow: hidden; background:
  radial-gradient(28% 30% at 8% 12%, rgba(255, 47, 179, .55), transparent 70%),
  radial-gradient(26% 34% at 92% 8%, rgba(41, 211, 255, .5), transparent 70%),
  radial-gradient(30% 26% at 50% 55%, rgba(166, 107, 255, .4), transparent 70%),
  radial-gradient(24% 30% at 4% 70%, rgba(198, 255, 26, .38), transparent 70%),
  radial-gradient(28% 30% at 96% 72%, rgba(255, 122, 26, .45), transparent 70%),
  radial-gradient(30% 24% at 40% 98%, rgba(255, 47, 179, .4), transparent 70%),
  var(--noise),
  repeating-linear-gradient(0deg, rgba(0, 0, 0, .55) 0 3px, transparent 3px 34px),
  repeating-linear-gradient(90deg, rgba(0, 0, 0, .45) 0 3px, transparent 3px 76px) 0 0 / 152px 68px,
  repeating-linear-gradient(90deg, transparent 0 38px, rgba(0, 0, 0, .45) 38px 41px, transparent 41px 76px) 0 34px / 152px 68px,
  linear-gradient(#3a2a24, #2a1f1b); }
.sv__tags { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.sv__tag { position: absolute; left: var(--x); top: var(--y); rotate: var(--r); font-size: calc(clamp(44px, 6vw, 96px) * var(--s)); line-height: 1; white-space: nowrap; color: var(--c); -webkit-text-stroke: .04em rgba(0, 0, 0, .75); paint-order: stroke fill; text-shadow: 0 0 .35em color-mix(in srgb, var(--c) 55%, transparent); opacity: .92; }
.sv__tag--sed { font-family: "Sedgwick Ave Display", cursive; }
.sv__tag--mark { font-family: "Permanent Marker", cursive; }
.sv__tag--spray { font-family: "Rubik Spray Paint", sans-serif; }
''')
css = rep(css, '.sv .tile__k { color: #ff4a4a; }', '''.sv .tile__k { color: #ff2fb3; }
.sv .tile:nth-child(4n+2) .tile__k { color: #29d3ff; }
.sv .tile:nth-child(4n+3) .tile__k { color: #c6ff1a; }
.sv .tile:nth-child(4n+4) .tile__k { color: #ff7a1a; }
.sv .tile img { filter: saturate(1.3) contrast(1.05); box-shadow: 0 14px 30px -12px rgba(0, 0, 0, .8); }''')

# --- BTB: ретро-флаер, чёрный + фуксия + фотокопия
css = rep(css, '.btb { position: relative; background-image: var(--noise); }',
          '.btb { position: relative; background: radial-gradient(rgba(234, 11, 224, .07) 1px, transparent 1.5px) 0 0 / 6px 6px, var(--speck), #070608; }')
css = rep(css, 'background: url("assets/logo-ink.svg") repeat-x left center / auto 20px, #e7e4de; border-block: 2px solid #141414; }',
          'background: url("assets/logo-ink.svg") repeat-x left center / auto 20px, #ea0be0; border-block: 2px solid #f7f7f9; }')
css = css.replace('-webkit-text-stroke: .052em #d0cec7;', '-webkit-text-stroke: .052em #f7f7f9;')
css = css.replace('color: #c8242b; filter: url(#btb-ink); }', 'color: #ea0be0; filter: url(#btb-ink); }')
css = css.replace('filter: grayscale(1) contrast(1.6) brightness(.58); box-shadow: 0 0 0 clamp(4px, .5vw, 7px) #e9e7e1; }',
                  'filter: grayscale(1) contrast(2.3) brightness(.85); box-shadow: 0 0 0 clamp(4px, .5vw, 7px) #f7f7f9; }')
css = rep(css, 'background: #d4262c; color: #fff; font: 400 34px/1 "Anton", var(--disp); text-transform: uppercase; letter-spacing: .02em; box-shadow: 4px 4px 0 #1a1414; }',
          'background: #ea0be0; color: #fff; font: 400 34px/1 "Anton", var(--disp); text-transform: uppercase; letter-spacing: .02em; box-shadow: 5px 5px 0 #f7f7f9; }')
css = rep(css, 'border-bottom: 2px solid #141414; font: 400 24px/1.15 "Anton"', 'border-bottom: 2px solid #f7f7f9; font: 400 24px/1.15 "Anton"')
css = rep(css, '.btb__when i { font-style: normal; color: #d4262c;', '.btb__when i { font-style: normal; color: #ea0be0;')
css = rep(css, '.btb__text { grid-column: 2; grid-row: 4; margin-top: 10px; color: #3d3a35;', '.btb__text { grid-column: 2; grid-row: 4; margin-top: 10px; color: var(--muted);')
css = rep(css, '.btb .season__poster { rotate: 1.5deg; box-shadow: 6px 6px 0 #141414; }', '.btb .season__poster { rotate: 1.5deg; box-shadow: 8px 8px 0 #ea0be0; }')
css = rep(css, '.btb .tile img { filter: grayscale(1) contrast(1.35); box-shadow: 0 0 0 2px #141414; }', '.btb .tile img { filter: grayscale(1) contrast(1.7) brightness(1.05); box-shadow: 0 0 0 2px #f7f7f9; }')
css = rep(css, 'font-size: 16px; color: #d4262c; }', 'font-size: 16px; color: #ea0be0; }')

# --- общие текстуры
css = rep(css, '  color-scheme: dark;\n}', '''  --speck: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='s'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.95' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1.6 -.92'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23s)'/%3E%3C/svg%3E");
  --dirt: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='900' height='900'%3E%3Cfilter id='d'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.008' numOctaves='5' seed='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .22 0 0 0 0 .14 0 0 0 0 .08 0 0 0 1.5 -.55'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23d)'/%3E%3C/svg%3E");
  color-scheme: dark;
}''')

(R / "index.html").write_text(re.sub(r"style\.css\?v=\d+", "style.css?v=18", html))
(R / "style.css").write_text(css)
print("ok")
