"""Список роликов со страницы канала: id и название. Запуск: python3 .work/yt_list.py .work/yt.html"""
import re, sys

h = open(sys.argv[1], encoding="utf-8").read()
seen = set()
for m in re.finditer(r'"title":\{"content":"(.*?)"', h):
    ids = re.findall(r'"videoId":"([\w-]{11})"', h[max(0, m.start() - 4000):m.start()])
    if ids and ids[-1] not in seen:
        seen.add(ids[-1])
        print(ids[-1], m.group(1)[:110])
