"""Иконки соцсетей (Simple Icons, CC0) → .work/icons.json {имя: path d}. python3 .work/icons.py"""
import json, pathlib, re, urllib.request

OUT = pathlib.Path(__file__).resolve().parent / "icons.json"
res = {}
for name in ("telegram", "vk", "youtube", "boosty"):
    svg = urllib.request.urlopen(f"https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/{name}.svg", timeout=20).read().decode()
    res[name] = re.search(r' d="([^"]+)"', svg).group(1)
    print(name, len(res[name]))
OUT.write_text(json.dumps(res))
