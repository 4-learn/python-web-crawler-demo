"""15｜變動偵測：比較 v1 與 v2 的「勞動基準法」，找出新增、刪除、修改。

做法：每條算一個 content_hash，比較兩邊的 {slug: hash}。
v2 的 API 欄位名稱跟 v1 不同，先各自「正規化」成同一種格式再比。
執行：python detect_changes.py [pcode]
"""
import hashlib
import json
import os
import sys
import time
from urllib.parse import urljoin

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
session = requests.Session()
session.headers["User-Agent"] = "course-crawler/1.0 (demo)"


def get(url):
    time.sleep(0.2)  # 示範用；正式爬取請依 Crawl-delay
    r = session.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_v1(pcode: str) -> dict:
    out, url = {}, BASE + f"v1/api/laws/{pcode}/page-1.json"
    while url:
        data = get(url)
        for a in data["articles"]:
            out[a["slug"]] = content_hash(a["content"])
        url = urljoin(url, data["next"]) if data["next"] else None
    return out


def load_v2(pcode: str) -> dict:
    out, page = {}, 1
    while True:
        data = get(BASE + f"v2/api/laws/{pcode}/{page}.json")
        for a in data["items"]:                # 欄位改名：id / text
            out[a["id"]] = content_hash(a["text"])
        if page >= data["pages"]:              # 沒有 next，改用 pages
            break
        page += 1
    return out


pcode = sys.argv[1] if len(sys.argv) > 1 else "N0030001"
old, new = load_v1(pcode), load_v2(pcode)
added = sorted(new.keys() - old.keys())
deleted = sorted(old.keys() - new.keys())
modified = sorted(k for k in old.keys() & new.keys() if old[k] != new[k])
print(f"{pcode}：v1 {len(old)} 條，v2 {len(new)} 條")
print("新增：", added)
print("刪除：", deleted)
print("修改：", modified)
