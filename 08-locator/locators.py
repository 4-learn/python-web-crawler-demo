"""08｜Locator 與自動等待：不用 time.sleep。

執行：python locators.py
"""
import os

from playwright.sync_api import expect, sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(BASE + "v1/dynamic/")

    title = page.locator("h2.law-title")
    expect(title).to_contain_text("勞動基準法")  # 會自動重試直到成立或逾時（預設 5 秒）
    print(title.inner_text())

    # 用「使用者看得到的東西」找元素：label、role、文字
    page.get_by_label("選擇法規").select_option(label="職業安全衛生法")
    expect(title).to_contain_text("職業安全衛生法")
    print(title.inner_text())

    articles = page.locator("article.article")
    print("條數：", articles.count())
    first = articles.first
    print(first.locator(".article-no").inner_text(), first.locator(".article-content").inner_text()[:30], "…")

    # 取全部：all_inner_texts() 一次拿回 list
    numbers = page.locator("article.article .article-no").all_inner_texts()
    print("前 5 個條號：", numbers[:5])
    browser.close()
