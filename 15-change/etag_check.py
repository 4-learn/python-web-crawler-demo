"""15｜條件式請求：沒變就不要重新下載。

第一次取得 ETag 存起來，下次帶 If-None-Match；伺服器回 304 代表沒變。
執行：python etag_check.py   （執行兩次看看）
"""
import json
import os
from pathlib import Path

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
CACHE = Path("etag_cache.json")
cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}

for path in ["v1/api/laws.json", "v1/api/laws/N0030001/page-1.json"]:
    url = BASE + path
    headers = {"User-Agent": "course-crawler/1.0 (demo)"}
    if url in cache:
        headers["If-None-Match"] = cache[url]
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code == 304:
        print("304 沒變，跳過", path)
    else:
        print(r.status_code, "下載", path, len(r.content), "bytes")
        if r.headers.get("ETag"):
            cache[url] = r.headers["ETag"]
CACHE.write_text(json.dumps(cache, indent=1))
