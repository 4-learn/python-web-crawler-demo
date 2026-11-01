"""08｜用使用者看得到的東西找元素，以及把「切換法規」包成函式。

執行：python 08-locator/more_locators.py
"""
import os

from playwright.sync_api import expect, sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")


def show_law(page, name):
    """在關卡 3 選一部法規，等它載完，回傳標題文字。"""
    page.get_by_label("選擇法規").select_option(label=name)
    title = page.locator("h2.law-title")
    expect(title).to_contain_text(name)
    return title.inner_text()


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(BASE + "v1/dynamic/")
    expect(page.locator("h2.law-title")).to_contain_text("勞動基準法")

    print("--- get_by_role ---")
    print(page.get_by_role("combobox", name="選擇法規").input_value())
    print(page.get_by_role("heading", level=2).inner_text())

    print("--- 切換後立刻數 vs 用 expect 等 ---")
    page.get_by_label("選擇法規").select_option(label="職業安全衛生法")
    print("立刻 count()：", page.locator("article.article").count())
    expect(page.locator("h2.law-title")).to_contain_text("職業安全衛生法")
    print("expect 之後：", page.locator("article.article").count())

    print("--- 包成函式 ---")
    print(show_law(page, "勞資爭議處理法"))
    browser.close()
