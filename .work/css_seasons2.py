"""Стили шапок сезонов по их афишам, v6. Запуск: python3 .work/css_seasons2.py"""
import pathlib

p = pathlib.Path(__file__).resolve().parent.parent / "style.css"
s = p.read_text(encoding="utf-8")

NEW = r'''/* Св*бода: их надпись кистью (вектор с афиши) прямо на стене, чёрные трафаретные плашки, афиша в чёрной раме */
.sv { position: relative; overflow: hidden; background-color: #1a1817; }
.sv > * { position: relative; z-index: 1; }
.sv__wall { position: absolute !important; z-index: 0 !important; inset: -40px; width: calc(100% + 80px); height: calc(100% + 80px); object-fit: cover; filter: blur(22px) brightness(.34) saturate(1.15); }
.sv .season__head { grid-template-columns: minmax(0, 1fr) clamp(220px, 22vw, 330px); align-items: end; }
.sv__left { grid-column: 1; grid-row: 1 / span 2; }
.sv__title img { width: min(100%, 980px); height: auto; filter: drop-shadow(0 6px 0 rgba(0, 0, 0, .35)); }
.sv__bars { display: flex; flex-wrap: wrap; gap: 8px; margin: 22px 0 12px; }
.sv__bars span { background: #0c0c0c; color: #fff; padding: 7px 14px 6px; font: 700 20px/1 var(--disp); text-transform: uppercase; letter-spacing: .02em; box-shadow: 0 0 0 1px rgba(255, 255, 255, .18); }
.sv__text { color: #d8d4cc; font-size: 17px; }
.sv .season__poster { rotate: 2deg; border: 10px solid #0c0c0c; box-shadow: 0 30px 60px -18px rgba(0, 0, 0, .8); }
.sv .tile__k { color: #ff4a4a; }

/* Back to Basics: их заголовок (Anton, красный с тёмной обводкой и жёсткой тенью), газетная бумага, рамка из логотипов */
.btb { position: relative; background-image: var(--noise); }
.btb__strip { height: 30px; margin: calc(-1 * clamp(60px, 6vw, 90px)) calc(-1 * var(--gutter)) clamp(40px, 4vw, 60px); background: url("assets/logo-ink.svg") repeat-x left center / auto 20px, #e7e4de; border-block: 2px solid #141414; }
.btb__strip--bottom { margin: clamp(50px, 5vw, 70px) calc(-1 * var(--gutter)) calc(-1 * clamp(70px, 7vw, 100px)); }
.btb .season__head { grid-template-columns: minmax(0, 1fr) clamp(220px, 21vw, 310px); align-items: end; }
.btb__head { grid-column: 1; grid-row: 1 / span 2; display: grid; grid-template-columns: auto minmax(0, 1fr); column-gap: clamp(28px, 4vw, 60px); align-items: end; }
.btb__word { grid-column: 1; grid-row: 1 / span 4; display: grid; font: 400 clamp(96px, 10.4vw, 172px)/.86 "Anton", var(--disp); text-transform: uppercase; color: #d4262c; -webkit-text-stroke: 2px #1a1414; paint-order: stroke fill; text-shadow: 5px 5px 0 #1a1414; letter-spacing: .005em; }
.btb__bar { grid-column: 2; grid-row: 1; display: block; padding: 8px 18px 7px; background: #d4262c; color: #fff; font: 400 34px/1 "Anton", var(--disp); text-transform: uppercase; letter-spacing: .02em; box-shadow: 4px 4px 0 #1a1414; }
.btb__when { grid-column: 2; grid-row: 2; margin-top: 18px; padding-bottom: 12px; border-bottom: 2px solid #141414; font: 400 24px/1.15 "Anton", var(--disp); text-transform: uppercase; letter-spacing: .01em; }
.btb__when i { font-style: normal; color: #d4262c; padding: 0 .2em; }
.btb__text { grid-column: 2; grid-row: 3; margin-top: 10px; color: #3d3a35; max-width: 46ch; }
.btb .season__poster { rotate: 1.5deg; box-shadow: 6px 6px 0 #141414; }
.btb .tile img { filter: grayscale(1) contrast(1.35); box-shadow: 0 0 0 2px #141414; }
.btb .tile:hover img { filter: none; }
.btb .tile__k { font-family: "Anton", var(--disp); font-weight: 400; font-size: 16px; color: #d4262c; }

'''
a = s.index("/* Св*бода:")
b = s.index("/* ОРГАНИЗАТОРЫ */")
s = s[:a] + NEW + s[b:]

# мобильные правки
s = s.replace("  .sv__word { font-size: 14vw; }\n  .sv .season__head { grid-template-columns: minmax(0, 1fr); }\n  .sv__sheet { max-width: 100%; }\n",
              "  .sv .season__head, .btb .season__head { grid-template-columns: minmax(0, 1fr); }\n  .sv__bars span { font-size: 16px; }\n")
s = s.replace("  .btb__word { font-size: 19vw; }\n  .sv__sheet, .btb__head { grid-row: 1; }\n  .season__poster { grid-row: 1; }",
              "  .btb__word { font-size: 22vw; }\n  .btb__head { grid-row: 1; }\n  .season__poster { grid-column: 1; grid-row: 2; width: 52%; justify-self: end; margin-top: -10px; }")
p.write_text(s, encoding="utf-8")
print("ok")
