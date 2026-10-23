"""Переносит карточку афтепати из правой колонки HUNT под «Пропали без вести». Запуск: python3 .work/move_after.py"""
import pathlib, re

p = pathlib.Path(__file__).resolve().parent.parent / "index.html"
s = p.read_text(encoding="utf-8")
card = re.search(r'\s*<article class="card card--after">.*?</article>', s, re.S).group(0)
s = s.replace(card, "", 1)
s = s.replace('<div class="gone"></div>', '<div class="gone"></div>' + card.replace('class="card card--after"', 'class="card card--after card--left"'), 1)
p.write_text(s, encoding="utf-8")
print("moved")
