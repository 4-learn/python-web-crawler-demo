"""10｜無限捲動：一直往下捲，直到出現「已經到底了」。

執行：python infinite_scroll.py
"""
import os

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(BASE + "v1/scroll/")
    items = page.locator("article.feed-item")
    items.first.wait_for()

    rounds = 0
    while page.locator("#feed-end").count() == 0:
        before = items.count()
        page.mouse.wheel(0, 3000)
        try:
            # 等到條數變多（或到底）；不寫死 sleep
            page.wait_for_function(
                "([n]) => document.querySelectorAll('article.feed-item').length > n || document.querySelector('#feed-end')",
                arg=[before], timeout=10_000)
        except Exception:
            print("10 秒內沒有新內容，停止")
            break
        rounds += 1
        print(f"第 {rounds} 次捲動：{items.count()} 條")

    print("總共", items.count(), "條；最後一條：", items.last.locator(".article-no").inner_text())
    browser.close()
