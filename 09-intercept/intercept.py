"""09｜攔截網路回應：讓瀏覽器去載入，我們直接拿它背後的 JSON。

執行：python intercept.py
"""
import os

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # 方法一：監聽所有回應，看看頁面呼叫了哪些 API
    seen = []
    page.on("response", lambda resp: seen.append(resp.url) if "/api/" in resp.url else None)

    # 方法二：等待「特定」回應，直接拿 JSON
    with page.expect_response(lambda r: "/api/laws/N0030001/page-1.json" in r.url) as info:
        page.goto(BASE + "v1/dynamic/")
    data = info.value.json()
    print("攔到：", info.value.url)
    print(data["name"], "第", data["page"], "頁，共", data["total_pages"], "頁")

    page.locator("article.article").first.wait_for()
    print("頁面呼叫過的 API：")
    for url in seen:
        print("  ", url.replace(BASE, ""))
    browser.close()
