"""05｜跟著「下一頁」爬完一部法規，輸出 JSONL。

執行：python crawl_law.py N0060001
"""
import json
import os
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
session = requests.Session()
session.headers["User-Agent"] = "course-crawler/1.0 (demo)"


def get_soup(url: str) -> BeautifulSoup:
    r = session.get(url, timeout=10)
    r.raise_for_status()
    r.encoding = "utf-8"
    return BeautifulSoup(r.text, "html.parser")


def parse_article(el, page_url: str, pcode: str, law_name: str) -> dict:
    link = el.select_one(".article-no a")
    return {
        "pcode": pcode,
        "law_name": law_name,
        "slug": el["data-slug"],
        "article_no": link.get_text(strip=True),
        "chapter": el.select_one(".chapter").get_text(strip=True),
        "content": "\n".join(p.get_text() for p in el.select(".article-content p")),
        "source_url": urljoin(page_url, link["href"]),
    }


def crawl(pcode: str) -> list[dict]:
    url = BASE + f"v1/laws/{pcode}/"
    rows = []
    while url:
        soup = get_soup(url)
        law_name = soup.select_one("h1.law-title").get_text(strip=True)
        rows += [parse_article(el, url, pcode, law_name) for el in soup.select("article.article")]
        print(soup.select_one(".pagination .current").get_text(), "累計", len(rows))
        nxt = soup.select_one("a.next")
        url = urljoin(url, nxt["href"]) if nxt else None  # 沒有「下一頁」就停
        time.sleep(1)  # robots.txt 的 Crawl-delay: 1
    expected = int(soup.select_one("dd.count").get_text())
    assert len(rows) == expected, f"只抓到 {len(rows)} 條，頁面寫 {expected} 條"
    return rows


if __name__ == "__main__":
    pcode = sys.argv[1] if len(sys.argv) > 1 else "N0060001"
    rows = crawl(pcode)
    out = f"{pcode}.jsonl"
    with open(out, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"寫入 {out}，共 {len(rows)} 條")
