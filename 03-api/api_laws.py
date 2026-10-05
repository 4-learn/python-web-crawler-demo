"""03｜先找 API：用 requests 取得 JSON，跟著 next 欄位走完分頁。

執行：python api_laws.py
"""
import os
from urllib.parse import urljoin

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
session = requests.Session()
session.headers["User-Agent"] = "course-crawler/1.0 (demo)"


def get_json(url: str) -> dict:
    r = session.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


laws = get_json(BASE + "v1/api/laws.json")
print(f"共 {laws['count']} 部法規")
for law in laws["laws"]:
    print(f"  {law['pcode']}  {law['name']}（{law['article_count']} 條）")

pcode = "N0030001"  # 勞動基準法
url = BASE + f"v1/api/laws/{pcode}/page-1.json"
articles = []
while url:
    data = get_json(url)
    articles.extend(data["articles"])
    print(f"第 {data['page']} / {data['total_pages']} 頁，累計 {len(articles)} 條")
    url = urljoin(url, data["next"]) if data["next"] else None

print(articles[0]["article_no"], articles[0]["content"][:40], "…")
assert len(articles) == data["total"]
