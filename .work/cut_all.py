"""Пакетное вырезание людей через скомпилированный .work/cutout. Запуск из kubok-mc: python3 .work/cut_all.py"""
import subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BIN = ROOT / ".work" / "cutout"
B = ".work/brief/kubok_mc_visual_brief/"
JOBS = {
    "assets/ph-1.jpg": "ph-1", "assets/ph-2.jpg": "ph-2", "assets/ph-3.jpg": "ph-3",
    "assets/ph-4.jpg": "ph-4", "assets/ph-5.jpg": "ph-5", "assets/ph-6.jpg": "ph-6",
    "assets/ph-after.jpg": "ph-after", "assets/frame-crowd.jpg": "crowd",
    "assets/q-gokilla.jpg": "gokilla", "assets/q-zeiman.jpg": "zeiman",
    B + "SVOBODA/SVOBODA_06_IZTOLPY_vs_PALMDROPOV_preview.png": "sv-iztolpy",
    B + "SVOBODA/SVOBODA_03_NOKTU_vs_JOLLO_preview.png": "sv-nokty",
    B + "EARLIER/EARLIER_01_HHOS_vs_SHALA_preview.png": "btb-xxoc",
    B + "EARLIER/EARLIER_03_BIGA_ONE_vs_VISHNYA_preview.png": "btb-biga",
}
for src, name in JOBS.items():
    r = subprocess.run([str(BIN), str(ROOT / src), str(ROOT / "assets/cut" / f"{name}.png")], capture_output=True, text=True)
    print(name, (r.stdout or r.stderr).strip())
