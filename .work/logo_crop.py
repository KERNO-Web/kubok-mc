"""Обрезает viewBox logo.svg по реальным границам букв. Запуск: python3 .work/logo_crop.py"""
import pathlib, re

p = pathlib.Path(__file__).resolve().parent.parent / "assets" / "logo.svg"
s = p.read_text()
nums = [float(n) for n in re.findall(r"[ML]([\d.]+) ([\d.]+)", s) for n in n]
xs, ys = nums[0::2], nums[1::2]
x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
s = re.sub(r'viewBox="[^"]+"', f'viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}"', s)
p.write_text(s)
print("viewBox", round(x0), round(y0), round(x1 - x0), round(y1 - y0))
