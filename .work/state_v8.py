"""Обновляет docs/STATE.md под v8. python3 .work/state_v8.py"""
import pathlib

p = pathlib.Path(__file__).resolve().parent.parent / "docs" / "STATE.md"
s = p.read_text()
s = s.replace("## Что сделано (v7)", "## Что сделано (v8)\n\n**Идентичность ивентов (v8, по просьбе Сергея):** HUNT = тёмный андерграунд (доска расследования: #110e0c, грязь `--dirt`, зерно `--speck` с CSS-дрожанием, виньетка, тёмный фильтр на фото, затёртый штамп HUNT фильтром `#hunt-grime`). Св*бода = граффити-стена (кирпич SVG, неоновые баллоны radial-gradient, теги со слов их афиши шрифтами Sedgwick Ave Display / Permanent Marker / Rubik Spray Paint, на мобиле только 4 тега, цветные подписи плиток). BTB = ретро-флаер как в v2 (чёрный #070608, белый, фуксия #ea0be0, фотокопия, полоса логотипов на фуксии). Скрипт `.work/skins_v8.py`.\n")
s = s.replace("надпись = настоящая краска с афиши `assets/svoboda-paint.png` (RGBA, x4, резкость; `.work/paint.swift paint`)",
              "надпись = чистая версия от Сергея 2000x667, вырезана в прозрачный `assets/svoboda-paint.png` (`.work/paint.swift paint … 0 0 2000 667 1`)")
s = s.replace("Взят Archivo 900 ширина 62, вытянут scaleY 1.16, буквы внахлёст с серой обводкой (как на афише)",
              "Взят Archivo 900 ширина 62, вытянут scaleY 1.16, буквы внахлёст с обводкой (v8: фуксия с белой обводкой)")
p.write_text(s)
print("ok")
