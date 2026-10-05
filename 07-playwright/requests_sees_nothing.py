"""07｜requests 只拿得到「原始碼」，看不到 JavaScript 產生的內容。

執行：python requests_sees_nothing.py
"""
import os

import requests
from bs4 import BeautifulSoup

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
r = requests.get(BASE + "v1/dynamic/", headers={"User-Agent": "course-crawler/1.0 (demo)"}, timeout=10)
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "html.parser")
print("#app 的內容：", soup.select_one("#app").get_text(strip=True))
print("article 數量：", len(soup.select("article.article")))
print("頁面引用的 JS：", [s["src"] for s in soup.select("script[src]")])
