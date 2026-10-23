"""Контакт-листы фото ивентов с номерами: .work/contact-<FOLDER>.html + .txt с соответствием номер → файл.
python3 .work/contact.py"""
import pathlib

W = pathlib.Path(__file__).resolve().parent
files = sorted(p.name for p in (W / "pv").glob("*.jpg"))
for folder in ("HUNT", "SVOBODA", "BTB"):
    lst = [f for f in files if f.startswith(folder + "__")]
    html = ('<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#111;display:grid;grid-template-columns:repeat(5,1fr);'
            'gap:4px;font:bold 22px monospace;color:#ff0}div{position:relative}img{width:100%;height:190px;object-fit:cover;display:block}'
            'b{position:absolute;left:4px;top:2px;background:#000;padding:0 4px}</style>'
            + "".join(f'<div><img src="pv/{f}"><b>{i + 1}</b></div>' for i, f in enumerate(lst)))
    (W / f"contact-{folder}.html").write_text(html)
    (W / f"contact-{folder}.txt").write_text("\n".join(f"{i + 1} {f}" for i, f in enumerate(lst)))
    print(folder, len(lst))
