"""06｜被限速時，polite_get 會依 Retry-After 等待再試。

只對教室版執行：
    export PLAYGROUND=http://老師IP:8000/
    python 06-polite/retry_demo.py
"""
import os
import sys

import requests

from polite_get import load_robots, polite_get

BASE = os.environ.get("PLAYGROUND", "http://127.0.0.1:8000/")
if "github.io" in BASE:
    sys.exit("請對教室版 server.py 執行這個示範")

load_robots(BASE)
codes = [requests.get(BASE + "v1/api/laws.json", timeout=5).status_code for _ in range(25)]
print("別的程式先把額度用光：", {c: codes.count(c) for c in sorted(set(codes))})
r = polite_get(BASE + "v1/api/laws/N0020012/page-1.json")
print(r.status_code, "v1/api/laws/N0020012/page-1.json")
