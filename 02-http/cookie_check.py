"""02｜Cookie：伺服器怎麼記得你。

這支要對「教室版」執行（GitHub Pages 版沒有 401）：
    export PLAYGROUND=http://老師IP:8000/
    python 02-http/cookie_check.py
"""
import os

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

url = BASE + "v1/api/members/notices.json"
r = requests.get(url, timeout=10)
print("沒帶 cookie：", r.status_code, r.text.strip())
r = requests.get(url, cookies={"pg_session": "demo-session-token"}, timeout=10)
print("帶 cookie：", r.status_code, r.headers["Content-Type"])
print("請求 header Cookie：", r.request.headers["Cookie"])
