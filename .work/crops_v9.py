"""v9: текстуры из их материалов. Дерево и лого HUNT — из обложки афтепати (hunt-after.jpg, 1280x720).
python3 .work/crops_v9.py"""
import subprocess, pathlib

R = pathlib.Path(__file__).resolve().parent.parent
A = R / "assets"
Z = R / ".work" / "zoom"


def crop(src, out, x, y, w, h, fmt="jpeg"):
    subprocess.run(["sips", "-s", "format", fmt, "-s", "formatOptions", "88", "-c", str(h), str(w), "--cropOffset", str(y), str(x),
                    str(A / src), "--out", str(out)], check=True, capture_output=True)
    print(out.name, w, "x", h)


crop("hunt-after.jpg", A / "hunt-logo.jpg", 492, 6, 285, 180)
crop("hunt-after.jpg", Z / "wood-r.jpg", 1236, 0, 40, 720)
crop("hunt-after.jpg", Z / "wood-l.jpg", 4, 140, 40, 580)
crop("hunt-dm.jpg", Z / "wood-dm.jpg", 0, 0, 1280, 720)
