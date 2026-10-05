"""05｜詳細頁裡的 JSON-LD：網站自己提供的結構化資料。

執行：python json_ld.py
"""
import json
import os

import requests
from bs4 import BeautifulSoup

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
url = BASE + "v1/laws/N0030001/articles/30-1.html"
r = requests.get(url, headers={"User-Agent": "course-crawler/1.0 (demo)"}, timeout=10)
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "html.parser")
ld = json.loads(soup.select_one('script[type="application/ld+json"]').string)
print(json.dumps(ld, ensure_ascii=False, indent=2)[:400])
