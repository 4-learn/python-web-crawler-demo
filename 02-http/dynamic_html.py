"""02｜關卡 3 的 HTML 裡有條文嗎？用 requests 抓抓看。

執行：python 02-http/dynamic_html.py
"""
import os

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
HEADERS = {"User-Agent": "course-crawler/1.0 (demo)"}

r = requests.get(BASE + "v1/dynamic/", headers=HEADERS, timeout=10)
r.encoding = "utf-8"
for line in r.text.splitlines():
    if "law-select" in line or 'id="app"' in line:   # 只挑出關鍵的兩行
        print(line.strip())
print("HTML 裡有『第 1 條』嗎？", "第 1 條" in r.text)
