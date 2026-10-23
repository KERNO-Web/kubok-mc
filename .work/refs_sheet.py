"""Контакт-лист refs/orgs с номерами файлов: .work/refs-sheet.html (превью в .work/pv-refs). python3 .work/refs_sheet.py"""
import pathlib, subprocess

R = pathlib.Path(__file__).resolve().parent.parent
src = pathlib.Path("/private/tmp/claude-501/-Users-sergey-mac-Vibecode/43dbef9e-eddc-4750-8856-d31cf0408d57/images")
out = R / ".work" / "pv-refs"
out.mkdir(exist_ok=True)
files = sorted(src.iterdir(), key=lambda p: int(p.stem) if p.stem.isdigit() else 999)
cells = []
for f in files:
    if f.name.startswith("."):
        continue
    pv = out / (f.stem + ".jpg")
    subprocess.run(["sips", "-s", "format", "jpeg", "-Z", "320", str(f), "--out", str(pv)], capture_output=True)
    cells.append(f'<div><img src="pv-refs/{pv.name}"><b>{f.name}</b></div>')
(R / ".work" / "refs-sheet.html").write_text(
    '<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#111;display:grid;grid-template-columns:repeat(8,1fr);gap:3px;'
    'font:bold 14px monospace;color:#ff0}div{position:relative}img{width:100%;height:150px;object-fit:cover;display:block}'
    'b{position:absolute;left:2px;top:2px;background:#000;padding:0 3px}</style>' + "".join(cells))
print(len(cells))
