"""v7: заголовки сезонов с афиш. BTB — вектор букв с афиши; Св*бода — настоящая краска (RGBA) + вектор для обрезки.
Запуск: python3 .work/titles2.py"""
import subprocess, pathlib, re

W = pathlib.Path(__file__).resolve().parent
A = W.parent / "assets"
Z = W / "zoom"
Z.mkdir(exist_ok=True)


def sw(*args):
    r = subprocess.run(["swift", *map(str, args)], capture_output=True, text=True)
    print(r.stdout.strip(), r.stderr.strip()[:300])


def fit_viewbox(svg, color):
    s = svg.read_text().replace('fill="#fff"', f'fill="{color}"')
    nums = [float(n) for pair in re.findall(r"[ML]([\d.]+) ([\d.]+)", s) for n in pair]
    xs, ys = nums[0::2], nums[1::2]
    vb = (min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
    s = re.sub(r'viewBox="[^"]+"', 'viewBox="%.1f %.1f %.1f %.1f"' % vb, s)
    svg.write_text(s)
    print(svg.name, "viewBox", ["%.0f" % v for v in vb])
    return vb


# BTB: красные буквы заголовка, x15..370, y28..366, x5
sw(W / "paint.swift", "mask", A / "poster-btb.jpg", Z / "btb-mask.png", 21, 30, 372, 334, 5)
sw(W / "vectorize.swift", Z / "btb-mask.png", Z / "btb-raw.svg")
(Z / "btb-raw.svg").replace(Z / "btb-letters.svg")
fit_viewbox(Z / "btb-letters.svg", "#fff")

# Св*бода: краска x4 + маска для контура
SV = (128, 166, 340, 96)
sw(W / "paint.swift", "paint", A / "poster-svoboda.jpg", A / "svoboda-paint.png", *SV, 4)
sw(W / "paint.swift", "mask", A / "poster-svoboda.jpg", Z / "sv-mask4.png", *SV, 4)
