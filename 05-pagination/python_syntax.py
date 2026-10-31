"""05｜這節會用到的 Python 語法：用練習站的資料示範。

執行：python 05-pagination/python_syntax.py
"""
import os

import requests
from bs4 import BeautifulSoup

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
r = requests.get(BASE + "v1/laws/N0030001/", headers={"User-Agent": "course-crawler/1.0 (demo)"}, timeout=10)
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "html.parser")
articles = soup.select("article.article")

print("--- 1. dict：用 {鍵: 值} 把一筆資料包起來 ---")
first = articles[0]
row = {
    "slug": first["data-slug"],
    "article_no": first.select_one(".article-no a").get_text(strip=True),
}
print(row)
print(row["article_no"])

print("--- 2. list comprehension：[對每個做什麼 for 每個 in 一串] ---")
numbers = [el.select_one(".article-no a").get_text(strip=True) for el in articles]
print(len(numbers), numbers[:3])

print("--- 3. 用換行把多段接起來：\"\\n\".join(...) ---")
paragraphs = [p.get_text() for p in first.select(".article-content p")]
print(paragraphs)
print("\n".join(paragraphs))

print("--- 4. 三元運算：A if 條件 else B ---")
nxt = soup.select_one("a.next")
print(nxt["href"] if nxt else None)

print("--- 5. rows += [...]：把一串接到另一串後面 ---")
rows = []
rows += numbers[:2]
rows += numbers[2:4]
print(rows)
