"""Вторая нарезка: main event 1/4 и Deathmatch Clash из анонсов. Запуск: python3 .work/crop2.py <папка_рефов>"""
import subprocess, sys, pathlib

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"


def crop(src, out, x, y, w, h):
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "84",
                    "-c", str(h), str(w), "--cropOffset", str(y), str(x),
                    str(SRC / src), "--out", str(OUT / out)], check=True, capture_output=True)


crop("23.webp", "q-gokilla.jpg", 62, 72, 415, 465)
crop("23.webp", "q-zeiman.jpg", 778, 72, 412, 462)
crop("24.webp", "dm-hidji.jpg", 80, 54, 240, 192)
crop("24.webp", "dm-kumska.jpg", 966, 52, 240, 190)
crop("24.webp", "dm-kazakh.jpg", 74, 398, 250, 170)
crop("24.webp", "dm-donalds.jpg", 497, 437, 232, 168)
crop("24.webp", "dm-misharik.jpg", 906, 432, 238, 164)
print("ok")
