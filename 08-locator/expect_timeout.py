"""08｜expect 等不到會怎樣：2 秒後直接報錯（這是預期結果）。

執行：python 08-locator/expect_timeout.py
"""
import os

from playwright.sync_api import expect, sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(BASE + "v1/dynamic/")
    print("等標題出現「不存在的法」，最多 2 秒…")
    expect(page.locator("h2.law-title")).to_contain_text("不存在的法", timeout=2000)
    print("這一行不會被執行到")
