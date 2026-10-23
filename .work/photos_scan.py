"""Список фото в HUNT/SVOBODA/BTB с размерами + превью 400px для контакт-листа. python3 .work/photos_scan.py"""
import pathlib, subprocess

R = pathlib.Path(__file__).resolve().parent.parent
OUT = R / ".work" / "pv"
OUT.mkdir(exist_ok=True)
for folder in ("HUNT", "SVOBODA", "BTB"):
    for f in sorted((R / folder).iterdir()):
        if f.name.startswith(".") or f.is_dir():
            continue
        o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(f)], capture_output=True, text=True).stdout.split()
        try:
            w, h = int(o[-3]), int(o[-1])
        except (ValueError, IndexError):
            print(folder, f.name, "?")
            continue
        pv = OUT / f"{folder}__{f.stem}.jpg"
        subprocess.run(["sips", "-s", "format", "jpeg", "-Z", "400", str(f), "--out", str(pv)], capture_output=True)
        print(folder, f.name, w, "x", h, f.stat().st_size // 1024, "KB")
