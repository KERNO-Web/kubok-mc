"""Переходы без mask (в рендере Chrome маска на ::before не срабатывала): тёмный градиент поверх картинки
первым слоем фона того же ::before. python3 .work/seams_v18b.py"""
import pathlib, re

p = pathlib.Path(__file__).resolve().parent.parent / "style.css"
css = p.read_text()
C = "#0c0a09"
BOTH = f"linear-gradient({C}, rgba(12, 10, 9, 0) 260px, rgba(12, 10, 9, 0) calc(100% - 260px), {C})"
TOP = f"linear-gradient({C}, rgba(12, 10, 9, .6) 120px, rgba(12, 10, 9, 0) 320px)"
HEAD = f"linear-gradient({C} 20px, rgba(12, 10, 9, 0) 240px, rgba(12, 10, 9, 0) calc(100% - 160px), {C})"


def line(s, start, new):
    m = re.search(r"^" + re.escape(start) + r"[^\n]*\n", s, re.M)
    assert m, start
    return s[:m.start()] + new + s[m.end():]


css = line(css, ".event::before { -webkit-mask:", "")
css = line(css, ".sv::before, .btb::before { -webkit-mask:", "")
# первым слоем добавляем затемнение краёв
css = css.replace(".event::before { content: \"\"; position: absolute; inset: -20px; z-index: -1; background: ",
                  f".event::before {{ content: \"\"; position: absolute; inset: -20px; z-index: -1; background: {BOTH}, ", 1)
css = re.sub(r"(\.ev-head::before \{[^}]*?background: )", r"\g<1>" + HEAD + ", ", css, count=1)
css = re.sub(r"-webkit-mask: linear-gradient\(transparent, #000 220px, #000 calc\(100% - 140px\), transparent\); mask: linear-gradient\(transparent, #000 220px, #000 calc\(100% - 140px\), transparent\); ", "", css)
for sel in (".sv::before {", ".btb::before {"):
    css = re.sub(r"(^" + re.escape(sel) + r"[^\n]*?background: )", r"\g<1>" + TOP + ", ", css, count=1, flags=re.M)
assert css.count("rgba(12, 10, 9, .6) 120px") == 2 and "mask: linear-gradient(transparent, #000 220px" not in css
p.write_text(css)
print("ok")
