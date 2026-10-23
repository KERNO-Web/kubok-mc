"""Скачивает фото постов t.me/kbkmc по номерам из сохранённых страниц. Запуск: python3 .work/tg_get.py <html> <пост:имя> ..."""
import re, sys, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
h = open(sys.argv[1], encoding="utf-8").read()
want = dict(a.split(":") for a in sys.argv[2:])
for post in h.split('class="tgme_widget_message_wrap')[1:]:
    m = re.search(r'data-post="kbkmc/(\d+)"', post)
    if not m or m.group(1) not in want:
        continue
    photos = re.findall(r"tgme_widget_message_photo_wrap[^>]*background-image:url\('([^']+)'\)", post)
    for i, p in enumerate(photos):
        name = want[m.group(1)] + (f"-{i + 1}" if len(photos) > 1 else "") + ".jpg"
        data = urllib.request.urlopen(p, timeout=30).read()
        (ROOT / "assets" / name).write_bytes(data)
        print(name, len(data))
