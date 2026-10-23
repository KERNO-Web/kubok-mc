"""Фото «из круга» по ивентам: порядок = лучшие первыми (номера из контакт-листов .work/contact-<F>.txt),
копии в assets/krug/<key>/NN.jpg (q80) и массив KRUG для app.js в .work/krug.json. python3 .work/krug.py"""
import json, pathlib, subprocess

R = pathlib.Path(__file__).resolve().parent.parent
W = R / ".work"
ORDER = {
    ("HUNT", "hunt"): [15, 8, 12, 7, 16, 9, 1, 2, 17, 4, 14, 6, 19, 3, 18, 13, 5, 11, 20, 10],
    ("SVOBODA", "svoboda"): [20, 14, 12, 3, 2, 4, 10, 11, 17, 19, 1, 8, 9, 13, 7, 15, 18, 5, 6, 16],
    ("BTB", "btb"): [8, 1, 9, 13, 3, 19, 4, 7, 11, 2, 14, 15, 17, 10, 6, 12, 16, 5, 18],
}
data = {}
for (folder, key), order in ORDER.items():
    names = dict(line.split(" ", 1) for line in (W / f"contact-{folder}.txt").read_text().splitlines())
    out = R / "assets" / "krug" / key
    out.mkdir(parents=True, exist_ok=True)
    data[key] = []
    for i, n in enumerate(order, 1):
        stem = names[str(n)].split("__", 1)[1].rsplit(".", 1)[0]
        src = R / folder / f"{stem}.jpg"
        dst = out / f"{i:02d}.jpg"
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80", str(src), "--out", str(dst)], check=True, capture_output=True)
        o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(dst)], capture_output=True, text=True).stdout.split()
        data[key].append([f"{i:02d}", int(o[-3]), int(o[-1])])
    print(key, len(data[key]))
(W / "krug.json").write_text(json.dumps(data, separators=(",", ":")))
