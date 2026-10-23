"""Нарезка рефов Кубка МЦ в assets/ через sips (macOS). Запуск: python3 .work/crop.py <папка_рефов>"""
import subprocess, sys, shutil, pathlib

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)


def crop(src, out, x, y, w, h):
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "84",
                    "-c", str(h), str(w), "--cropOffset", str(y), str(x),
                    str(SRC / src), "--out", str(OUT / out)], check=True, capture_output=True)


def conv(src, out, maxw=None):
    args = ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82"]
    if maxw:
        args += ["--resampleWidth", str(maxw)]
    subprocess.run(args + [str(SRC / src), "--out", str(OUT / out)], check=True, capture_output=True)


# 1/8 финала — обложки из скрина канала (1.webp, 2000px)
cols, rows = [160, 731, 1302], [69, 528, 987]
pairs = ["body-killhomie", "bach-shala", "smoke-eeugene",
         "miksi-kukish", "envimi-kapustu", "nokty-kulakoff",
         "iren-elmad", "verch-zeiman"]
for i, name in enumerate(pairs):
    crop("1.webp", f"r8-{name}.jpg", cols[i % 3], rows[i // 3], 537, 292)

# Лица 16 участников с афиши (7.webp)
faces = ["verch", "miksi", "kapustu", "iren", "timmi", "kukish", "smoke", "kulakoff",
         "shala", "nokty", "envimi", "zeiman", "body", "killhomie", "elmad", "eeugene"]
fx, fy = [966, 1145, 1324, 1503], [203, 380, 556, 733]
for i, name in enumerate(faces):
    crop("7.webp", f"face-{name}.jpg", fx[i % 4], fy[i // 4], 138, 137)

# 1/4 финала — фото с досок
crop("11.webp", "q-miksi.jpg", 62, 72, 415, 465)
crop("11.webp", "q-otrix.jpg", 778, 72, 412, 462)
crop("12.webp", "q-yami.jpg", 62, 72, 415, 465)
crop("12.webp", "q-kenya.jpg", 778, 72, 412, 462)

# Архив сезонов
crop("2.webp", "arch-svoboda.jpg", 705, 1023, 550, 300)
crop("3.webp", "arch-btb.jpg", 1269, 568, 548, 300)
crop("2.webp", "arch-bpm.jpg", 1289, 85, 550, 300)

# Фото и кадры как есть
for src, out in [("15.jpg", "ph-1.jpg"), ("16.jpg", "ph-2.jpg"), ("17.jpg", "ph-3.jpg"),
                 ("18.jpg", "ph-4.jpg"), ("19.jpg", "ph-5.jpg"), ("20.jpg", "ph-6.jpg"),
                 ("14.jpg", "ph-after.jpg"), ("13.webp", "poster-after.jpg"),
                 ("5.webp", "frame-wanted.jpg"), ("6.webp", "frame-crowd.jpg"),
                 ("9.webp", "frame-svoboda.jpg")]:
    conv(src, out, 1600)
shutil.copy(SRC / "10.png", OUT / "logo.png")
print("ok", len(list(OUT.iterdir())))
