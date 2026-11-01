"""09｜方法一：page.on("response", ...) 監聽所有回應，看看頁面背後呼叫了哪些 API。

執行：python 09-intercept/intercept_on.py
"""
import os

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")


def log(resp):
    """每收到一個回應，Playwright 就呼叫一次這個函式。"""
    if "/api/" in resp.url:                          # 只看 API，其他（HTML、CSS、JS）略過
        print(resp.status, resp.request.resource_type, resp.headers.get("content-type"), resp.url.replace(BASE, ""))


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("response", log)                         # 把 log 交給 Playwright（不加括號）
    page.goto(BASE + "v1/dynamic/")
    page.locator("article.article").first.wait_for()
    browser.close()
