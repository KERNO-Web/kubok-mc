"""Шортсы: вертикальные обложки (oardefault 9:16, иначе hq720 с обрезкой) + названия через oEmbed.
python3 .work/shorts.py  →  assets/sh/<id>.jpg и .work/shorts.json"""
import json, pathlib, subprocess, urllib.request, urllib.parse

R = pathlib.Path(__file__).resolve().parent.parent
OUT = R / "assets" / "sh"
OUT.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/130 Safari/537.36"}
SETS = {
    "hunt": ["Hsbtt14y0Eo"],
    "svoboda": ["MyZux-W9hoc"],
    "btb": ["jcwS65q3dXY"],
}  # первая партия (по 4) уже скачана; здесь только добавленные


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read()


def dims(f):
    o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(f)], capture_output=True, text=True).stdout.split()
    return int(o[-3]), int(o[-1])


meta = {}
for season, ids in SETS.items():
    meta[season] = []
    for vid in ids:
        title = ""
        try:
            q = urllib.parse.quote(f"https://www.youtube.com/shorts/{vid}")
            title = json.loads(get(f"https://www.youtube.com/oembed?url={q}&format=json"))["title"]
        except Exception as e:
            title = f"? {e}"
        f = OUT / f"{vid}.jpg"
        src = None
        for name in ("oardefault", "oar2", "hq720", "maxresdefault", "hqdefault"):
            try:
                data = get(f"https://i.ytimg.com/vi/{vid}/{name}.jpg")
            except Exception:
                continue
            if len(data) > 4000:
                f.write_bytes(data)
                src = name
                break
        w, h = dims(f)
        if w > h:  # горизонтальная обложка: вырезаем центр 9:16
            cw = int(h * 9 / 16)
            subprocess.run(["sips", "-c", str(h), str(cw), str(f), "--out", str(f)], capture_output=True)
            w, h = dims(f)
        meta[season].append({"id": vid, "title": title, "src": src, "size": f"{w}x{h}"})
        print(season, vid, src, f"{w}x{h}", title)
(R / ".work" / "shorts.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
