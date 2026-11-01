"""07｜page.content() 拿到的是「此刻」的 DOM；以及兩種截圖。

執行：python 07-playwright/content_and_screenshot.py
"""
import os

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(user_agent="course-crawler/1.0 (demo)")
    page.goto(BASE + "v1/dynamic/")

    print("--- content()：等待前後 ---")
    print("網頁標題：", page.title())
    print("剛 goto 完：", "<article" in page.content())
    page.locator("article.article").first.wait_for()
    print("等待之後：", page.content().count('<article class="article"'), "個 article")

    print("--- 截圖 ---")
    os.makedirs("output", exist_ok=True)
    page.screenshot(path="output/dynamic.png")                  # 只截視窗範圍
    page.screenshot(path="output/full.png", full_page=True)     # 截整頁
    print("已存 output/dynamic.png、output/full.png")
    browser.close()
