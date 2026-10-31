"""03｜requests 的 Response：送出請求後拿到什麼。

執行：python 03-api/response_basics.py
"""
import os

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

r = requests.get(BASE + "v1/api/laws.json", headers={"User-Agent": "course-crawler/1.0 (demo)"}, timeout=10)
print(r)
print(r.status_code, r.ok)
print(r.url)
print(r.headers["Content-Type"])
print(r.encoding)
print(type(r.content), len(r.content), r.content[:30])
print(type(r.text), len(r.text), repr(r.text[:30]))   # repr：把換行顯示成 \n
data = r.json()
print(type(data), data["count"])

print("\n--- 故意用錯的編碼 ---")
r.encoding = "big5"
text = r.text
print(text[text.find('"name"'):][:22])   # 找到第一個 "name" 印出來
