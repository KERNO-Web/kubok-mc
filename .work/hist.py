"""Вытаскивает из старого транскрипта куски CSS v2 со стилем BTB. python3 .work/hist.py <jsonl> <слово> [n]"""
import sys, re

path, word = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
seen = set()
for line in open(path, encoding="utf-8", errors="ignore"):
    for m in re.finditer(re.escape(word), line):
        chunk = line[max(0, m.start() - 600): m.end() + 900].encode().decode("unicode_escape", "ignore") if "\\n" in line else line[max(0, m.start() - 600): m.end() + 900]
        key = chunk[:120]
        if key in seen:
            continue
        seen.add(key)
        print("=" * 40)
        print(chunk)
        n -= 1
        if n <= 0:
            sys.exit()
