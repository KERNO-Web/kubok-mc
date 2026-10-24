# --noise/--speck в style.css: SVG feTurbulence -> готовые плитки assets/fx/*.webp (2x, поэтому через image-set)
import re
p = "/Users/sergey-mac/Vibecode/kubok-mc/style.css"
s = open(p, encoding="utf-8").read()
s, a = re.subn(r'--noise: url\("data:image/svg\+xml,[^"]+"\);', '--noise: -webkit-image-set(url("assets/fx/noise.webp") 2x);', s)
s, b = re.subn(r'--speck: url\("data:image/svg\+xml,[^"]+"\);', '--speck: -webkit-image-set(url("assets/fx/speck.webp") 2x);', s)
open(p, "w", encoding="utf-8").write(s)
print(a, b)
