"""07｜第一支 Playwright 程式：開瀏覽器、等內容出現、截圖。

安裝：pip install playwright && playwright install --with-deps chromium
執行：python first_playwright.py           （預設 headless，看不到視窗）
      HEADED=1 python first_playwright.py  （有桌面環境時可看到瀏覽器）
"""
import os

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=not os.environ.get("HEADED"))
    page = browser.new_page(user_agent="course-crawler/1.0 (demo)")
    page.goto(BASE + "v1/dynamic/")
    print("一開始：", page.locator("#app").inner_text())

    page.locator("article.article").first.wait_for()  # 等第一條條文出現
    print("等待後：", page.locator("h2.law-title").inner_text())
    print("article 數量：", page.locator("article.article").count())

    page.screenshot(path="dynamic.png", full_page=False)
    print("已存 dynamic.png")
    browser.close()
