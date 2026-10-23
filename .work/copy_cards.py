"""Копирует карточки внетурнирных баттлов HUNT в assets. Запуск: python3 .work/copy_cards.py"""
import subprocess, pathlib

SRC = pathlib.Path("/private/tmp/claude-501/-Users-sergey-mac-Vibecode/43dbef9e-eddc-4750-8856-d31cf0408d57/images")
A = pathlib.Path(__file__).resolve().parent.parent / "assets"
for src, dst in [("11.webp", "hunt-main-miksi.jpg"), ("12.webp", "hunt-main-yami.jpg")]:
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "90", str(SRC / src), "--out", str(A / dst)], check=True, capture_output=True)
    print(dst)
