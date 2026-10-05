"""11｜同一件事：Selenium 4 與 Playwright 對照。

Selenium 4.6 起內建 Selenium Manager，會自動下載對應的 driver，
不再需要 webdriver_manager。
執行：python selenium_vs_playwright.py
"""
import os
import time

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
URL = BASE + "v1/dynamic/"


def with_selenium() -> int:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.article")))
        return len(driver.find_elements(By.CSS_SELECTOR, "article.article"))
    finally:
        driver.quit()


def with_playwright() -> int:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL)
        page.locator("article.article").first.wait_for()
        n = page.locator("article.article").count()
        browser.close()
        return n


for name, fn in [("Playwright", with_playwright), ("Selenium", with_selenium)]:
    t = time.time()
    try:
        print(f"{name}: {fn()} 條，{time.time() - t:.1f} 秒")
    except Exception as e:
        print(f"{name}: 失敗 {type(e).__name__}: {str(e).splitlines()[0][:120]}")
