"""09｜方法二：expect_response 等一支特定的 API，直接拿 JSON。

執行：python 09-intercept/intercept_expect.py
"""
import os

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    print("--- 打開頁面時，等勞動基準法第 1 頁 ---")
    with page.expect_response(lambda r: "/api/laws/N0030001/page-1.json" in r.url) as info:
        page.goto(BASE + "v1/dynamic/")
    data = info.value.json()
    print("攔到：", info.value.url)
    print(data["name"], "第", data["page"], "頁，共", data["total_pages"], "頁")

    print("--- 切換法規時，等大量解僱勞工保護法第 1 頁 ---")
    with page.expect_response(lambda r: "/api/laws/N0020012/page-1.json" in r.url) as info:
        page.get_by_label("選擇法規").select_option(label="大量解僱勞工保護法")
    data = info.value.json()
    print(list(data.keys()))
    print(data["articles"][0])
    browser.close()
