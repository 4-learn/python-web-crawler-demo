"""06｜教室示範：沒禮貌 vs 有禮貌。請對「教室版」server.py 執行，不要對 GitHub Pages 狂打。

老師：python server.py --host 0.0.0.0
學員：PLAYGROUND=http://老師IP:8000/ python rude_vs_polite.py
"""
import os
import sys

import requests

from polite_get import PoliteSession

BASE = os.environ.get("PLAYGROUND", "http://127.0.0.1:8000/")
if "github.io" in BASE:
    sys.exit("請對教室版 server.py 執行這個示範")

print("--- 沒禮貌：連續 30 次，不等待 ---")
codes = [requests.get(BASE + "v1/api/laws.json", timeout=5).status_code for _ in range(30)]
print({c: codes.count(c) for c in set(codes)})

print("--- 有禮貌：每秒 1 次 ---")
s = PoliteSession(BASE, "course-crawler/1.0 (demo)")
for i in range(1, 6):
    print(s.get(BASE + f"v1/api/laws/N0020012/page-{1 if i < 3 else 2}.json").status_code)
