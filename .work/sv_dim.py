"""Св*бода: фон стены затемнён и слегка размыт (через ::before с filter). python3 .work/sv_dim.py"""
import pathlib, re

p = pathlib.Path(__file__).resolve().parent.parent / "style.css"
css = p.read_text()
IMG = 'image-set(url("assets/svoboda-street.webp") 1x, url("assets/svoboda-street-2x.jpg") 2x)'


def line(s, start, new):
    m = re.search(r"^" + re.escape(start) + r"[^\n]*\n", s, re.M)
    assert m, start
    return s[:m.start()] + new + s[m.end():]


css = line(css, ".sv { position: relative;",
           ".sv { position: relative; overflow: hidden; isolation: isolate; background: #080809; }\n"
           f'.sv::before {{ content: ""; position: absolute; inset: -16px; z-index: 0; pointer-events: none; background: linear-gradient(transparent 72%, #080809 92%), {IMG} 50% 0 / cover no-repeat; filter: blur(4px) brightness(.5); }}\n')
css = line(css, "  .sv { background:",
           f"  .sv::before {{ inset: 0; background: linear-gradient(transparent 55vw, #080809 100vw) 0 0 / 100% 100vw no-repeat, {IMG} 50% 0 / 100% auto no-repeat; }}\n")
p.write_text(css)
print("ok")
