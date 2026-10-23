"""Переносит «Пропали без вести» в правую колонку HUNT, под Deathmatch. Запуск: python3 .work/move_gone.py"""
import pathlib

p = pathlib.Path(__file__).resolve().parent.parent / "index.html"
s = p.read_text(encoding="utf-8")
block = '\n        <h3 class="tag tag--ink">Пропали без&nbsp;вести</h3>\n        <div class="gone"></div>'
assert block in s, "block not found"
s = s.replace(block, "", 1)
anchor = 'Мишарик, Молодой Казах, МЦ Доналдас, Kumska.</p>\n        </article>'
assert anchor in s, "anchor not found"
s = s.replace(anchor, anchor + '\n        <div class="gone-wrap">' + block.replace("\n        ", "\n          ") + '\n        </div>', 1)
p.write_text(s, encoding="utf-8")
print("moved")
