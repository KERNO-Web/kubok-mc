"""Компилирует bake.swift и запекает ч/б версии в assets/bw/. Запуск: python3 .work/bake_all.py"""
import subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = ROOT / ".work"
A = ROOT / "assets"
(A / "bw").mkdir(exist_ok=True)
binary = W / "bake"
if not binary.exists():
    subprocess.run(["swiftc", "-O", str(W / "bake.swift"), "-o", str(binary)], check=True)

JOBS = [("ph-1.jpg", "ph-1.jpg"), ("ph-2.jpg", "ph-2.jpg"), ("ph-3.jpg", "ph-3.jpg"), ("ph-4.jpg", "ph-4.jpg"),
        ("ph-5.jpg", "ph-5.jpg"), ("ph-6.jpg", "ph-6.jpg"), ("ph-after.jpg", "ph-after.jpg"),
        ("cut/ph-4.png", "ph-4-cut.png"), ("org-halloween.jpg", "org-halloween.jpg"),
        ("org-pohoronil.jpg", "org-pohoronil.jpg"), ("face-bach.jpg", "face-bach.jpg")]
for src, dst in JOBS:
    r = subprocess.run([str(binary), str(A / src), str(A / "bw" / dst)], capture_output=True, text=True)
    print((r.stdout or r.stderr).strip())
