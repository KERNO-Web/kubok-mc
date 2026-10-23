"""Крупные кропы афиш для разбора шрифта/текстуры. python3 .work/zoom.py"""
import subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / ".work" / "zoom"
OUT.mkdir(exist_ok=True)

# (файл, имя, x, y, w, h, масштаб)
JOBS = [
    ("poster-btb.jpg", "btb-back", 20, 30, 280, 120, 4),
    ("poster-btb.jpg", "btb-basics", 20, 245, 340, 115, 4),
    ("poster-btb.jpg", "btb-k", 180, 30, 100, 110, 7),
    ("poster-btb.jpg", "btb-acap", 50, 380, 300, 120, 3),
    ("poster-svoboda.jpg", "sv-title", 125, 155, 345, 110, 4),
    ("poster-svoboda.jpg", "sv-c", 130, 160, 110, 100, 7),
]

for src, name, x, y, w, h, s in JOBS:
    tmp = OUT / f"{name}.png"
    subprocess.run(["sips", "-s", "format", "png", "-c", str(h), str(w), "--cropOffset", str(y), str(x),
                    str(ROOT / "assets" / src), "--out", str(tmp)], check=True, capture_output=True)
    subprocess.run(["sips", "-z", str(h * s), str(w * s), str(tmp)], check=True, capture_output=True)
    print(tmp)
