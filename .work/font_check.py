"""Проверка кириллицы у шрифтов Google Fonts. Запуск: python3 .work/font_check.py"""
import urllib.request, urllib.parse

FAMILIES = ["Sofia Sans Extra Condensed", "Sofia Sans Condensed", "Sofia Sans", "Alumni Sans", "Anton", "Bebas Neue",
            "Oswald", "Fira Sans Extra Condensed", "Roboto Condensed", "Tektur", "Unbounded", "Dela Gothic One",
            "Rubik Mono One", "Geologica", "Rubik Dirt", "Rubik Wet Paint", "Big Shoulders Display", "Archivo Black",
            "Archivo", "Anybody", "Climate Crisis", "Bona Nova SC", "Kanit"]
for f in FAMILIES:
    url = "https://fonts.googleapis.com/css2?family=" + urllib.parse.quote(f)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
    try:
        css = urllib.request.urlopen(req, timeout=15).read().decode()
        print(f"{f:32} cyrillic={'/* cyrillic */' in css}")
    except Exception as e:
        print(f"{f:32} error {e}")
