"""11｜Trace Viewer：把每一步的截圖、DOM、網路請求都錄下來。

執行：python trace_demo.py
查看：playwright show-trace trace.zip   （或上傳到 https://trace.playwright.dev ，檔案只在本機瀏覽器處理）
"""
import os

from playwright.sync_api import sync_playwright

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    try:
        page.goto(BASE + "v1/dynamic/")
        # 故意寫錯 selector：v2 的寫法，在 v1 頁面上找不到
        page.locator("tr.row").first.wait_for(timeout=3000)
    except Exception as e:
        print("失敗了：", type(e).__name__)
        print("打開 trace.zip 看失敗當下的畫面與 DOM")
    finally:
        context.tracing.stop(path="trace.zip")
        browser.close()
