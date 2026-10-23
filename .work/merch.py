"""Мерч: копирует 6 мокапов в assets/merch (пары спереди/сзади) и печатает размеры. python3 .work/merch.py"""
import pathlib, subprocess

R = pathlib.Path(__file__).resolve().parent.parent
IMG = pathlib.Path("/private/tmp/claude-501/-Users-sergey-mac-Vibecode/2c74d36a-62c3-4bd5-8f2f-197ee7569606/images")
OUT = R / "assets" / "merch"
OUT.mkdir(parents=True, exist_ok=True)
PAIRS = {"white-front": "16.jpg", "white-back": "12.jpg", "black-front": "13.jpg", "black-back": "14.jpg",
         "model-front": "11.webp", "model-back": "15.jpg"}
for name, src in PAIRS.items():
    dst = OUT / f"{name}.jpg"
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86", str(IMG / src), "--out", str(dst)], check=True, capture_output=True)
    o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(dst)], capture_output=True, text=True).stdout.split()
    print(name, o[-3], o[-1])
