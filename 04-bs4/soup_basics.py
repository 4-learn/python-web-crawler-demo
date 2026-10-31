"""04｜BeautifulSoup 的基本概念：soup 是什麼、Tag 物件有哪些東西。

執行：python 04-bs4/soup_basics.py
"""
import os

import requests
from bs4 import BeautifulSoup

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

r = requests.get(BASE + "v1/laws/", headers={"User-Agent": "course-crawler/1.0 (demo)"}, timeout=10)
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "html.parser")

print("--- soup：整份 HTML 解析成的樹 ---")
print(type(soup))
print(soup.title)
print(soup.title.get_text())

print("--- Tag：樹上的一個元素 ---")
row = soup.select_one("tr.law")
print(type(row))
print(row.name)                       # 標籤名
print(row.attrs)                      # 全部屬性（dict）
print(row["data-pcode"], row.get("class"), row.get("no-such"))
link = row.select_one("a")            # Tag 也能再往裡面找
print(link)
print(link.get_text(), link["href"])

print("--- select 回傳很多個 Tag ---")
rows = soup.select("tr.law")
print(type(rows), len(rows), type(rows[0]))

print("--- 找不到時 ---")
print(soup.select_one("table.no-such-class"), soup.select("table.no-such-class"))

print("--- get_text 與 strip ---")
td = BeautifulSoup("<td>\n    勞動基準法\n</td>", "html.parser").td
print(repr(td.get_text()))
print(repr(td.get_text(strip=True)))
