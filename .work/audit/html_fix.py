# index.html: размытый фон низа -> уменьшенные копии assets/lw/, версии style/app
import re
p = "/Users/sergey-mac/Vibecode/kubok-mc/index.html"
s = open(p, encoding="utf-8").read()
def lw(m):
    return re.sub(r'assets/krug/(\w+)/(\d+)\.jpg', r'assets/lw/\1-\2.jpg', m.group(0))
s, a = re.subn(r'<div class="lw lw--bw">.*?</div>', lw, s, count=1)
s, b = re.subn(r'style\.css\?v=\d+', 'style.css?v=95', s)
s, c = re.subn(r'app\.js\?v=\d+', 'app.js?v=66', s)
open(p, "w", encoding="utf-8").write(s)
print(a, b, c, s.count("assets/lw/"))
