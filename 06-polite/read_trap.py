"""06（進階）｜rp.read() 的陷阱：robots.txt 被 429 時，會當成「全部允許」。

只對教室版執行：
    export PLAYGROUND=http://老師IP:8000/
    python 06-polite/read_trap.py
"""
import os
import sys
import urllib.robotparser

import requests

BASE = os.environ.get("PLAYGROUND", "http://127.0.0.1:8000/")
if "github.io" in BASE:
    sys.exit("請對教室版 server.py 執行這個示範")

codes = [requests.get(BASE + "v1/api/laws.json", timeout=5).status_code for _ in range(25)]
print("先把額度用完：", {c: codes.count(c) for c in sorted(set(codes))})
rp = urllib.robotparser.RobotFileParser(BASE + "robots.txt")
rp.read()
print("allow_all =", rp.allow_all)
print("can_fetch v1/admin/ ->", rp.can_fetch("course-crawler/1.0", BASE + "v1/admin/"))
