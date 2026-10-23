"""Вытаскивает надпись Св*бода с афиши в SVG и фото Бача с афиши TOP 16. Запуск: python3 .work/svoboda_title.py"""
import subprocess, pathlib, re

W = pathlib.Path(__file__).resolve().parent
A = W.parent / "assets"
IMG = pathlib.Path("/private/tmp/claude-501/-Users-sergey-mac-Vibecode/43dbef9e-eddc-4750-8856-d31cf0408d57/images")

# Бач с афиши TOP 16
subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "90", "-c", "176", "170", "--cropOffset", "210", "508",
                str(IMG / "36.webp"), "--out", str(A / "face-bach.jpg")], check=True, capture_output=True)
subprocess.run(["sips", "-s", "format", "jpeg", str(IMG / "36.webp"), "--out", str(A / "hunt-top16.jpg")], check=True, capture_output=True)

# Красная надпись: маска и вектор
mask = W / "sv-mask.png"
print(subprocess.run(["swift", str(W / "redmask.swift"), str(IMG / "37.webp"), str(mask), "118", "118", "755", "262"], capture_output=True, text=True).stdout.strip())
print(subprocess.run(["swift", str(W / "vectorize.swift"), str(mask), str(A / "svoboda-title.svg")], capture_output=True, text=True).stdout.strip())
svg = A / "svoboda-title.svg"
s = svg.read_text().replace('fill="#fff"', 'fill="#e01b22"')
nums = [float(n) for pair in re.findall(r"[ML]([\d.]+) ([\d.]+)", s) for n in pair]
xs, ys = nums[0::2], nums[1::2]
s = re.sub(r'viewBox="[^"]+"', f'viewBox="{min(xs):.1f} {min(ys):.1f} {max(xs) - min(xs):.1f} {max(ys) - min(ys):.1f}"', s)
svg.write_text(s)
print("svg", round(max(xs) - min(xs)), "x", round(max(ys) - min(ys)))
