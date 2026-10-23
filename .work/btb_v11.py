"""v11 BTB: заголовок-картинка от Сергея (красный войлок + костяная обводка), фон-коллаж затемнён и размыт как у Св*боды,
палитра коллажа: чёрный / кость / красный. Фуксия, фиолет, жёлтый и фото толпы убраны. python3 .work/btb_v11.py"""
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
html = (R / "index.html").read_text()
css = (R / "style.css").read_text()
IMG = 'image-set(url("assets/btb-collage.webp") 1x, url("assets/btb-collage-2x.jpg") 2x)'
RED, BONE, INK = "#d3161d", "#ebe4d8", "#0b0a0a"


def line(s, start, new):
    m = re.search(r"^" + re.escape(start) + r"[^\n]*\n", s, re.M)
    assert m, start
    return s[:m.start()] + new + s[m.end():]


# HTML: заголовок картинкой, svg-фильтр больше не нужен
html = re.sub(r'<div class="btb__title">.*?</h2></div>',
              '<h2 class="btb__title"><img src="assets/btb-title.png" alt="Back to Basics" width="640" height="545"></h2>', html, flags=re.S)
html = re.sub(r'  <filter id="btb-ink".*?</filter>\n', "", html, flags=re.S)

css = line(css, '[data-skin="btb"]', f'[data-skin="btb"] {{ --bg: {INK}; --fg: #f4efe6; --muted: #b9b1a5; --accent: {RED}; }}\n')
css = line(css, ".btb { position: relative;",
           f".btb {{ position: relative; overflow: hidden; isolation: isolate; background: {INK}; }}\n"
           f'.btb::before {{ content: ""; position: absolute; inset: -16px; z-index: 0; pointer-events: none; background: linear-gradient(transparent 70%, {INK} 92%), {IMG} 50% 0 / cover no-repeat; filter: blur(4px) brightness(.42); }}\n')
css = line(css, ".btb .season__head {", ".btb .season__head { grid-template-columns: minmax(0, 1fr) clamp(220px, 21vw, 310px); align-items: center; }\n")
css = line(css, ".btb__head {", ".btb__head { grid-column: 1; grid-row: 1 / span 2; display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); grid-template-rows: 1fr auto auto auto 1fr; column-gap: clamp(28px, 4vw, 60px); }\n")
css = line(css, ".btb__title {", ".btb__title { grid-column: 1; grid-row: 1 / -1; align-self: center; margin: 0; }\n"
           ".btb__title img { display: block; width: 100%; max-width: 640px; height: auto; filter: drop-shadow(0 14px 28px rgba(0, 0, 0, .75)); }\n")
for start in [".btb__head::before", ".btb__word {", ".btb__word > span:nth-child(3)", ".btb__word > span {", ".btb__word i {", ".btb__crack {",
              ".btb__bar::before, .btb__bar::after", ".btb__bar::before {", "  .btb__head { --f:"]:
    css = line(css, start, "")
css = line(css, ".btb__bar {", f'.btb__bar {{ grid-column: 2; grid-row: 2; justify-self: start; padding: 9px 20px 7px; background: {RED}; color: {BONE}; font: 400 34px/1 "Anton", var(--disp); text-transform: uppercase; letter-spacing: .03em; box-shadow: inset 0 0 0 3px {RED}, inset 0 0 0 5px {BONE}, 0 10px 24px -8px rgba(0, 0, 0, .8); }}\n')
css = line(css, ".btb__when {", f'.btb__when {{ grid-column: 2; grid-row: 3; margin-top: 18px; padding-bottom: 12px; border-bottom: 2px solid {BONE}; color: {BONE}; font: 400 24px/1.15 "Anton", var(--disp); text-transform: uppercase; letter-spacing: .01em; }}\n')
css = line(css, ".btb__when i {", f".btb__when i {{ font-style: normal; color: {RED}; padding: 0 .2em; }}\n")
css = line(css, ".btb .season__poster {", f".btb .season__poster {{ rotate: 1.5deg; box-shadow: 0 0 0 5px {BONE}, 0 26px 50px -16px rgba(0, 0, 0, .9); }}\n")
css = line(css, ".btb .tile__k {", f'.btb .tile__k {{ font-family: "Anton", var(--disp); font-weight: 400; font-size: 16px; color: {RED}; }}\n'
           f".btb .tile {{ background: #121010; box-shadow: inset 0 3px 0 {RED}, 0 16px 34px -14px rgba(0, 0, 0, .9); }}\n"
           f".btb .tile img {{ border-top: 3px solid {RED}; }}\n")
css = line(css, "  .btb { background:",
           f"  .btb::before {{ inset: 0; filter: brightness(.42); background: linear-gradient(transparent 60vw, {INK} 110vw) 0 0 / 100% 110vw no-repeat, {IMG} 50% 0 / 100% auto no-repeat; }}\n"
           "  .btb__title img { max-width: 92vw; }\n")

(R / "index.html").write_text(re.sub(r"style\.css\?v=\d+", "style.css?v=20", html))
(R / "style.css").write_text(css)
print("ok")
