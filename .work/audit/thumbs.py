# Уменьшенные копии картинок, которые показываются мелко:
#  - превью роликов в списках плееров: assets/yt/<id>.jpg 1280x720 -> assets/yt/s/<id>.jpg 400x225 (в списке они ~90px)
#  - размытый фон под организаторами: assets/krug/<ивент>/NN.jpg 1280 -> assets/lw/<ивент>-NN.jpg 640 (там blur 7px)
# Запуск: python3 .work/audit/thumbs.py
import os, re, subprocess

ROOT = "/Users/sergey-mac/Vibecode/kubok-mc"
A = os.path.join(ROOT, "assets")


def shrink(src, dst, size, q=82):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    subprocess.run(["sips", "-Z", str(size), "-s", "format", "jpeg", "-s", "formatOptions", str(q), src, "--out", dst],
                   check=True, stdout=subprocess.DEVNULL)


n = 0
for f in sorted(os.listdir(os.path.join(A, "yt"))):
    if f.endswith(".jpg"):
        shrink(os.path.join(A, "yt", f), os.path.join(A, "yt", "s", f), 400)
        n += 1

html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
lw = re.search(r'<div class="lw lw--bw">(.*?)</div>', html).group(1)
m = 0
for ev, nn in re.findall(r'assets/krug/(\w+)/(\d+)\.jpg', lw):
    shrink(os.path.join(A, "krug", ev, nn + ".jpg"), os.path.join(A, "lw", f"{ev}-{nn}.jpg"), 640, 80)
    m += 1
print("yt thumbs:", n, "lower bg:", m)
