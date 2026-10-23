"""Ужимает обложки шортсов до 540px ширины (2x для карточки ~270px) и собирает контакт-лист. python3 .work/shorts_resize.py"""
import pathlib, subprocess

R = pathlib.Path(__file__).resolve().parent.parent
for f in sorted((R / "assets" / "sh").glob("*.jpg")):
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", "--resampleWidth", "540", str(f), "--out", str(f)],
                   check=True, capture_output=True)
    print(f.name, f.stat().st_size // 1024, "KB")
