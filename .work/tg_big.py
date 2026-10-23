"""Пробует взять фото поста TG в максимальном размере через embed. python3 .work/tg_big.py <пост:имя> ..."""
import re, sys, pathlib, urllib.request, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / ".work" / "big"
OUT.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"}

for arg in sys.argv[1:]:
    post, name = arg.split(":")
    for variant in (f"https://t.me/kbkmc/{post}?embed=1&mode=tme", f"https://t.me/kbkmc/{post}?single&embed=1"):
        h = urllib.request.urlopen(urllib.request.Request(variant, headers=UA), timeout=30).read().decode("utf-8", "ignore")
        urls = re.findall(r"background-image:url\('([^']+)'\)", h) + re.findall(r'<img[^>]+src="(https://cdn[^"]+)"', h)
        urls = [u for u in urls if "cdn" in u and "emoji" not in u]
        for i, u in enumerate(urls[:4]):
            f = OUT / f"{name}-{i}.jpg"
            f.write_bytes(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read())
            dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(f)], capture_output=True, text=True).stdout.split()
            print(post, variant[-12:], f.name, dims[-3], dims[-1])
        if urls:
            break
