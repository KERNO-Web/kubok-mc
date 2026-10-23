"""Поиск на YouTube без API: печатает id и названия. Запуск: python3 .work/yt_search.py "запрос" """
import re, sys, urllib.parse, urllib.request

q = urllib.parse.quote(sys.argv[1])
req = urllib.request.Request(f"https://www.youtube.com/results?search_query={q}", headers={"Accept-Language": "ru", "User-Agent": "Mozilla/5.0"})
h = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
seen = set()
for m in re.finditer(r'"videoRenderer":\{"videoId":"([\w-]{11})".{0,3000}?"title":\{"runs":\[\{"text":"(.*?)"', h, re.S):
    if m.group(1) not in seen:
        seen.add(m.group(1))
        print(m.group(1), m.group(2)[:100])
    if len(seen) >= 8:
        break
