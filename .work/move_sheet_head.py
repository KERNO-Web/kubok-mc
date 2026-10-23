"""Выносит заголовок «Из круга» из ленты над ней. Запуск: python3 .work/move_sheet_head.py"""
import pathlib, re

p = pathlib.Path(__file__).resolve().parent.parent / "index.html"
s = p.read_text(encoding="utf-8")
head = re.search(r'\s*<div class="sheet__head">.*?</div>', s, re.S).group(0)
s = s.replace(head, "", 1)
s = s.replace('<div class="sheet__pin">', '<div class="sheet__pin">' + head.replace("\n          ", "\n        "), 1)
p.write_text(s, encoding="utf-8")
print("moved")
