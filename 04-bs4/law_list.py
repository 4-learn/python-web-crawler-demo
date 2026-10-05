"""04｜BeautifulSoup：用 CSS selector 取出法規列表。

執行：python law_list.py
"""
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
URL = BASE + "v1/laws/"

r = requests.get(URL, headers={"User-Agent": "course-crawler/1.0 (demo)"}, timeout=10)
r.raise_for_status()
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "html.parser")

# 1. 標籤、class、id
print("頁面標題：", soup.select_one("h1").get_text(strip=True))
print("法規數量（頁面上寫的）：", soup.select_one("#law-count").get_text())

# 2. 每一列：tr.law；屬性用 ["data-pcode"]
for row in soup.select("table.law-list tr.law"):
    link = row.select_one("td.law-name a")
    print(
        row["data-pcode"],
        link.get_text(strip=True),
        row.select_one("td.count").get_text(),
        urljoin(URL, link["href"]),  # 相對網址 → 絕對網址
    )

# 3. find / find_all 是同一件事的另一種寫法
first = soup.find("tr", class_="law")
print("find 找到的第一列：", first.find("a").get_text())
