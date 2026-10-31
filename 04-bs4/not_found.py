"""04｜找不到元素時：select_one 回 None，接著呼叫 get_text() 就會出錯。

執行：python 04-bs4/not_found.py   （最後丟出 AttributeError 是預期結果）
"""
import os

import requests
from bs4 import BeautifulSoup

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

r = requests.get(BASE + "v1/laws/", headers={"User-Agent": "course-crawler/1.0 (demo)"}, timeout=10)
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "html.parser")

table = soup.select_one("table.no-such-class")   # 故意寫錯 class
print("select_one 找不到：", table)
print(table.get_text())
