"""Заменяет стили сезонов на стили по их афишам + правит финал и мобильные правила. Запуск: python3 .work/css_seasons.py"""
import pathlib

p = pathlib.Path(__file__).resolve().parent.parent / "style.css"
s = p.read_text(encoding="utf-8")

NEW = r'''/* Св*бода: как их афиша. Стена (сама афиша, размытая) + белый лист, красная кисть с подтёками, чёрные трафаретные плашки */
.sv { position: relative; overflow: hidden; background-color: #1a1817; }
.sv > * { position: relative; z-index: 1; }
.sv__wall { position: absolute !important; z-index: 0 !important; inset: -40px; width: calc(100% + 80px); height: calc(100% + 80px); object-fit: cover; filter: blur(22px) brightness(.38) saturate(1.15); }
.sv .season__head { align-items: center; }
.sv__sheet { grid-column: 1; grid-row: 1 / span 2; justify-self: start; max-width: 860px; padding: clamp(22px, 3vw, 40px) clamp(24px, 3.4vw, 48px) clamp(26px, 3vw, 40px); background: #f2f0ec; color: #111; rotate: -1deg; box-shadow: 0 30px 60px -20px rgba(0, 0, 0, .7); }
.sv__word { font: 400 clamp(84px, 11vw, 184px)/.95 "Rubik Wet Paint", var(--disp); color: #d4161b; text-transform: uppercase; }
.sv__bars { display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 14px; }
.sv__bars span { background: #111; color: #fff; padding: 5px 12px 4px; font: 700 18px/1.1 var(--disp); text-transform: uppercase; }
.sv__text { color: #3c3a36; max-width: 52ch; }
.sv .season__poster { rotate: 2deg; }
.sv .tile__k { color: #ff4141; }

/* Back to Basics: как их афиша. Газетная бумага, полоса из логотипов, красный жирный узкий шрифт, фото фотокопией */
.btb { position: relative; background-image: var(--noise); }
.btb__strip { height: 30px; margin: calc(-1 * clamp(60px, 6vw, 90px)) calc(-1 * var(--gutter)) clamp(40px, 4vw, 60px); background: url("assets/logo-ink.svg") repeat-x left center / auto 20px, #e7e4de; border-block: 2px solid #141414; }
.btb .season__head { align-items: center; }
.btb__head { grid-column: 1; grid-row: 1 / span 2; }
.btb__word { display: grid; font: 700 clamp(84px, 9.4vw, 158px)/.84 var(--disp); text-transform: uppercase; color: var(--accent); text-shadow: 3px 3px 0 #141414; letter-spacing: -.005em; }
.btb__bar { display: inline-block; margin: 18px 0 12px; padding: 5px 18px 4px; background: var(--accent); color: #fff; font: 700 24px/1.1 var(--disp); text-transform: uppercase; }
.btb__when { font: 500 20px/1.25 var(--disp); text-transform: uppercase; }
.btb__when i { font-style: normal; color: var(--accent); padding: 0 .2em; }
.btb__text { margin-top: 6px; color: var(--muted); max-width: 52ch; }
.btb .season__poster { rotate: 1.5deg; }
.btb .tile img { filter: grayscale(1) contrast(1.35); box-shadow: 0 0 0 2px #141414; }
.btb .tile:hover img { filter: none; }

'''
a = s.index("/* Св*бода:")
b = s.index("/* ОРГАНИЗАТОРЫ */")
s = s[:a] + NEW + s[b:]

s = s.replace(".final__word { font: 700 min(19vw, 300px)/.8 var(--disp); text-transform: uppercase; letter-spacing: -.01em; transform: skewX(-8deg); transform-origin: left bottom; white-space: nowrap; }",
              ".final__logo { width: min(44vw, 560px); height: auto; }")
s = s.replace("  .cover__logo span:first-child { font-size: 15vw; }\n  .cover__logo span:last-child { font-size: 33vw; }",
              "  .cover__logo { width: 58vw; }")
s = s.replace("  .sv .season__word { font-size: 17vw; }\n  .btb .season__word { font-size: 15vw; }",
              "  .sv__word { font-size: 20vw; }\n  .btb__word { font-size: 19vw; }\n  .sv__sheet, .btb__head { grid-row: 1; }\n  .season__poster { grid-row: 1; }")
p.write_text(s, encoding="utf-8")
print("ok")
