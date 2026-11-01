"""11｜前輩留下的 Selenium 爬蟲（給你讀的，不用執行）。

這是公司舊專案裡常見的寫法，裡面有好幾個過時或有問題的地方，
講義第 7 段會逐一指出來。Workshop 延伸題要把它改寫成 Playwright。

要執行它還得另外 pip install webdriver-manager，所以本課只讀不跑。
"""
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager      # ① 另外裝的套件，自己下載 driver

URL = "https://4-learn.github.io/crawler-playground/v1/laws/N0030001/"

options = webdriver.ChromeOptions()
options.add_argument("--headless")                             # ② 舊的 headless 參數
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(URL)
time.sleep(5)                                                  # ③ 猜 5 秒應該載好了

rows = []
for el in driver.find_elements(By.CLASS_NAME, "article"):      # ④ 只抓這一頁，沒有跟著「下一頁」
    rows.append({
        "chapter": el.find_element(By.CLASS_NAME, "chapter").text,
        "article_number": el.find_element(By.CSS_SELECTOR, ".article-no a").text,
        "content": el.find_element(By.CLASS_NAME, "article-content").text,
    })

driver.quit()                                                  # ⑤ 中間出錯就不會執行到，瀏覽器留在背景

with open("laws_data.json", "w", encoding="utf-8") as f:      # ⑥ 存在目前目錄、沒有來源網址
    json.dump(rows, f, ensure_ascii=False, indent=2)
print(f"共 {len(rows)} 條")
