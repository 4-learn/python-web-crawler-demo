"""10｜登入一次，保存登入狀態；下次直接用，不必再登入。

帳密從環境變數讀取，不要寫死在程式裡：
    export PG_USER=student PG_PASS=crawler-demo
執行：python login_and_save.py
"""
import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
STATE = Path("state.json")  # 內含 cookie，等同登入憑證：不要 commit、不要分享

with sync_playwright() as p:
    browser = p.chromium.launch()

    if not STATE.exists():
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE + "v1/members/login.html")
        page.get_by_label("帳號").fill(os.environ["PG_USER"])
        page.get_by_label("密碼").fill(os.environ["PG_PASS"])
        page.get_by_role("button", name="登入").click()
        expect(page.locator("#welcome")).to_be_visible()
        context.storage_state(path=STATE)
        print("登入成功，已保存", STATE)
        context.close()

    context = browser.new_context(storage_state=STATE)
    page = context.new_page()
    page.goto(BASE + "v1/members/")
    notices = page.locator("li.notice-item")
    notices.first.wait_for()
    print("會員通知：")
    for text in notices.all_inner_texts():
        print("  -", text)
    browser.close()
