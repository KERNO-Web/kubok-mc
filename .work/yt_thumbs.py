"""Качает обложки YouTube в максимальном разрешении в assets/yt/. Запуск: python3 .work/yt_thumbs.py"""
import pathlib, urllib.request

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "yt"
OUT.mkdir(exist_ok=True)
IDS = ["yFk37WqensU", "TgrQ0N43CiU", "aAMWJh7chgE", "XiNIxZdJs6w", "yZyyW1XLNuM", "HwuMpB11GMY", "NEY-wCkF81w", "5uMRfEdG6ug", "ifDfwytzN74", "nPfCwm6pGFU", "CG8uANZNedE", "LsVvuYnQ_A4", "-rM3bXoUlU0", "ZGzIiM49Y2c", "90NMrF3nYBo", "Ojk4Iush2xM", "OYQAsMDFPNU", "__B0BwL1Lqk", "tbUFMZTpwoI", "uxEk6SBJacg", "tyX_kj2xTpw", "1qiIXkYuqOM", "Qn75X8Mj1r8", "sg3dTXCI8GQ", "kEjqtsZIfQs", "OgdpmpIjeKs", "MaFPQ9g302k",
       "tDnHPgZLMQE", "Ua9QH7VbzP8", "R0GMUgBNY_A", "nKBMggjdfWs", "SbS_QgVq3HM", "HTyyo-za-Y4"]
for vid in IDS:
    for name in ("maxresdefault", "hqdefault"):
        try:
            data = urllib.request.urlopen(f"https://i.ytimg.com/vi/{vid}/{name}.jpg", timeout=20).read()
        except Exception:
            continue
        if len(data) > 5000:
            (OUT / f"{vid}.jpg").write_bytes(data)
            print(vid, name, len(data))
            break
