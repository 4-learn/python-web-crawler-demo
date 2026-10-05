"""02｜看懂一次 HTTP 請求：status code、header、內容。

執行：python inspect_request.py
"""
import os

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
HEADERS = {"User-Agent": "course-crawler/1.0 (demo)"}

r = requests.get(BASE + "v1/laws/", headers=HEADERS, timeout=10)
print("請求：", r.request.method, r.request.url)
print("請求 header User-Agent：", r.request.headers["User-Agent"])
print("狀態碼：", r.status_code, r.reason)
print("Content-Type：", r.headers.get("Content-Type"))
print("ETag：", r.headers.get("ETag"))
print("內容前 200 字：")
print(r.text[:200])

print("\n--- 幾個常見的狀態碼 ---")
for path in ["v1/laws", "v1/no-such-page.html"]:
    r = requests.get(BASE + path, headers=HEADERS, timeout=10, allow_redirects=False)
    print(r.status_code, BASE + path, "→", r.headers.get("Location", ""))

# 304：帶上次拿到的 ETag，問伺服器「內容有變嗎？」
first = requests.get(BASE + "v1/laws/", headers=HEADERS, timeout=10)
etag = first.headers.get("ETag")
second = requests.get(BASE + "v1/laws/", headers={**HEADERS, "If-None-Match": etag}, timeout=10)
print(second.status_code, "If-None-Match", etag, "→ 內容長度", len(second.content))
