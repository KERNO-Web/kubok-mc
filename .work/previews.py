"""Уменьшенные превью материалов ивентов для разбора стиля. python3 .work/previews.py"""
import subprocess, pathlib

R = pathlib.Path(__file__).resolve().parent.parent
OUT = R / ".work" / "zoom"
FILES = ["yt/sg3dTXCI8GQ.jpg", "yt/LsVvuYnQ_A4.jpg", "hunt-main.jpg", "frame-svoboda.jpg", "cypher-svoboda.jpg",
         "arch-svoboda.jpg", "arch-btb.jpg", "hunt-board.jpg", "hunt-top16.jpg", "poster-after.jpg"]
for f in FILES:
    src = R / "assets" / f
    dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(src)], capture_output=True, text=True).stdout.split()
    out = OUT / ("pv-" + f.replace("/", "-"))
    subprocess.run(["sips", "-Z", "560", str(src), "--out", str(out)], capture_output=True)
    print(f, dims[-3], "x", dims[-1])
