"""v10: фоны Св*бода/BTB без мыла (webp 1x + Lanczos 2x для ретины), без размытия, затемнение только на переход,
Св*бода поднята, обложки карточками на фоне. python3 .work/bg_v10.py"""
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
p = R / "style.css"
css = p.read_text()


def line(s, start, new):
    m = re.search(r"^" + re.escape(start) + r"[^\n]*\n", s, re.M)
    assert m, start
    return s[:m.start()] + new + s[m.end():]


def bg(name, top):
    img = f'image-set(url("assets/{name}.webp") 1x, url("assets/{name}-2x.jpg") 2x)'
    return (f"linear-gradient(rgba(8, 8, 9, {top}), rgba(8, 8, 9, {top}) 72%, rgba(8, 8, 9, .85) 90%, #080809), "
            f'{img} 50% 0 / cover no-repeat, #080809')


css = line(css, ".sv { position: relative;", f".sv {{ position: relative; overflow: hidden; background: {bg('svoboda-street', 0)}; }}\n")
css = line(css, ".btb { position: relative;", f".btb {{ position: relative; overflow: hidden; background: {bg('btb-collage', .45)}; }}\n")
css = line(css, ".btb::before, .sv::before {", "")
css = line(css, ".sv .season__head {", ".sv .season__head { grid-template-columns: minmax(0, 1fr); justify-items: center; margin-top: clamp(0px, 2vw, 30px); }\n")
card = "{ background: #0d0c0f; padding-bottom: 12px; box-shadow: 0 16px 34px -14px rgba(0, 0, 0, .9); }\n"
css = line(css, ".sv .tile img {", ".sv .tile, .btb .tile " + card +
           ".sv .tile img, .btb .tile img { margin-bottom: 6px; }\n.sv .tile__k, .sv .tile__t, .btb .tile__k, .btb .tile__t { padding: 0 12px; }\n")
css = line(css, ".btb .tile img {", "")
# мобила: картинка на всю ширину сверху, ниже тёмный
css = css.replace("  .sv__bars span { font-size: 16px; }",
                  "  .sv__bars span { font-size: 16px; }\n  .sv, .btb { background-size: 100% auto, 100% auto; }")
p.write_text(css)
print("ok")
