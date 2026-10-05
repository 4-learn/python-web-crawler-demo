"""15｜選擇器失效：抓到 0 條就停下來報錯，不要用空檔案覆蓋舊資料。

執行：python zero_guard.py   （v1 正常；v2 改版後選擇器失效 → RuntimeError）
"""
import os

import requests
from bs4 import BeautifulSoup

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
HEADERS = {"User-Agent": "course-crawler/1.0 (demo)"}


def parse_page(url: str) -> list:
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    r.encoding = "utf-8"
    items = BeautifulSoup(r.text, "html.parser").select("article.article")  # v1 的選擇器
    if not items:
        raise RuntimeError(f"{url} 抓到 0 條：選擇器可能失效，停止，不要覆蓋舊資料")
    return items


print(len(parse_page(BASE + "v1/laws/N0030001/")), "條")
print(len(parse_page(BASE + "v2/laws/N0030001/p/1.html")), "條")
