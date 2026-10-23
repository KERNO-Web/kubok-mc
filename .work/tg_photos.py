"""Фото из публичной ленты t.me/s/kbkmc: печатает ссылку на фото и начало текста поста. Запуск: python3 .work/tg_photos.py .work/tg1.html"""
import re, sys, html

h = open(sys.argv[1], encoding="utf-8").read()
for post in h.split('class="tgme_widget_message_wrap')[1:]:
    photos = re.findall(r"tgme_widget_message_photo_wrap[^>]*background-image:url\('([^']+)'\)", post)
    text = re.search(r'tgme_widget_message_text[^>]*>(.*?)</div>', post, re.S)
    t = html.unescape(re.sub("<[^>]+>", " ", text.group(1))).strip()[:90] if text else ""
    link = re.search(r'data-post="([^"]+)"', post)
    for p in photos:
        print(link.group(1) if link else "?", "|", t.replace("\n", " "), "|", p)
