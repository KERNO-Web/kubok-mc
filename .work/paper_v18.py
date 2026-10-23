"""v18: бумага HUNT без растянутого кропа (CSS-бумага + рваные края маской + скотч), дата в две строки;
плавные переходы между ивентами (фоны растворяются в общий тёмный сверху и снизу). python3 .work/paper_v18.py"""
import pathlib, random, re, urllib.parse

R = pathlib.Path(__file__).resolve().parent.parent
css = (R / "style.css").read_text()
html = (R / "index.html").read_text()
random.seed(7)


def torn(n=46):
    """SVG-маска полосы с рваными верхом и низом (viewBox 1000x100, растягивается)."""
    top = [(0, random.uniform(2, 7))] + [(i * 1000 / n, random.uniform(0, 8)) for i in range(1, n)] + [(1000, random.uniform(2, 7))]
    bot = [(1000, random.uniform(92, 98))] + [((n - i) * 1000 / n, random.uniform(90, 100)) for i in range(1, n)] + [(0, random.uniform(92, 98))]
    pts = " ".join(f"{x:.0f},{y:.1f}" for x, y in top + bot)
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1000 100' preserveAspectRatio='none'><polygon points='{pts}'/></svg>"
    return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe="'/:=,. ") + '")'


def line(s, start, new):
    m = re.search(r"^" + re.escape(start) + r"[^\n]*\n", s, re.M)
    assert m, start
    return s[:m.start()] + new + s[m.end():]


PAPER = ("background: radial-gradient(120% 140% at 18% 30%, rgba(255, 250, 235, .55), transparent 55%), "
         "radial-gradient(90% 120% at 85% 80%, rgba(120, 80, 40, .22), transparent 60%), var(--noise), var(--noise), #e3d6ba;")
css = css.replace("  color-scheme: dark;\n}", f"  --torn: {torn()};\n  --torn2: {torn(30)};\n  color-scheme: dark;\n}}", 1)

css = line(css, ".ev-head__date {", f'''.ev-head__date {{ position: relative; display: grid; justify-items: center; gap: 8px; margin-top: 6px; padding: 18px clamp(26px, 3vw, 44px) 16px; {PAPER} color: #2b1d14; rotate: 1.2deg; -webkit-mask: var(--torn) 0 0 / 100% 100%; mask: var(--torn) 0 0 / 100% 100%; filter: drop-shadow(0 12px 14px rgba(0, 0, 0, .6)); }}
''')
css = line(css, ".ev-head__date b {", ".ev-head__date b { font: 900 clamp(34px, 3.8vw, 52px)/.95 var(--slab); text-transform: uppercase; color: #a8121a; white-space: nowrap; mix-blend-mode: multiply; letter-spacing: .01em; }\n")
css = line(css, ".ev-head__date span {", ".ev-head__date span { display: flex; align-items: center; gap: 12px; font: 700 clamp(13px, 1.1vw, 16px)/1 var(--slab); text-transform: uppercase; letter-spacing: .22em; color: #3a2a1e; white-space: nowrap; mix-blend-mode: multiply; }\n.ev-head__date span::before, .ev-head__date span::after { content: \"\"; width: 34px; height: 2px; background: currentColor; opacity: .55; }\n")
css = line(css, ".ev-head__date i {", ".ev-head__date i { font-style: normal; color: #a8121a; }\n")
# пары турнира: та же бумага
css = css.replace('background: url("assets/hunt-paper.jpg") 0 0 / 100% 100%; color: #2b1d14; rotate: -.5deg;',
                  f'{PAPER} -webkit-mask: var(--torn2) 0 0 / 100% 100%; mask: var(--torn2) 0 0 / 100% 100%; color: #2b1d14; rotate: -.5deg;', 1)
assert "hunt-paper.jpg" not in css

# ---------- плавные переходы: фон каждого ивента растворяется в общий тёмный
FADE = "linear-gradient(transparent, #000 clamp(120px, 16vh, 200px), #000 calc(100% - clamp(120px, 16vh, 200px)), transparent)"
FADE_TOP = "linear-gradient(transparent, #000 clamp(140px, 20vh, 240px))"
css += f'''
/* ---------- Переходы между ивентами: общий тёмный стык, фоны растворяются ---------- */
.event, .sv, .btb {{ background-color: #0c0a09; }}
.event::before {{ -webkit-mask: {FADE}; mask: {FADE}; }}
.ev-head {{ background: none; box-shadow: none; isolation: auto; }}
.ev-head::before {{ content: ""; position: absolute; inset: 0; z-index: -1; background: radial-gradient(60% 55% at 50% 50%, rgba(20, 10, 4, .35), transparent 70%), url("assets/hunt-board2.webp") 50% 50% / cover no-repeat; -webkit-mask: linear-gradient(transparent, #000 clamp(110px, 14vh, 180px), #000 calc(100% - 140px), transparent); mask: linear-gradient(transparent, #000 clamp(110px, 14vh, 180px), #000 calc(100% - 140px), transparent); }}
.sv::before, .btb::before {{ -webkit-mask: {FADE_TOP}; mask: {FADE_TOP}; }}
'''
# контакты: @kbkmc только у Telegram (и это же имя у YouTube-канала), у остальных — что там лежит
for site, sub in (("vk.com/kbkmc", "Сообщество"), ("youtube.com/@kbkmc", "Все баттлы"), ("boosty.to/kbkmc", "Поддержать Кубок")):
    html = re.sub(r'(<a href="https://(?:www\.)?' + re.escape(site) + r'".*?<i>)@kbkmc(</i>)', r"\g<1>" + sub + r"\2", html, count=1, flags=re.S)
assert html.count("<i>@kbkmc</i>") == 1
html = re.sub(r"style\.css\?v=\d+", "style.css?v=30", html)
(R / "style.css").write_text(css)
(R / "index.html").write_text(html)
print("ok")
