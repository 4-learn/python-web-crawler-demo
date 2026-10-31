"""06｜有禮貌的 GET：先查 robots.txt、固定間隔、遇到 429 依 Retry-After 重試。

不用 class，只用三個函式：
    load_robots(base)   讀 robots.txt（自己下載，不用 rp.read()）
    polite_get(url)     檢查 robots → 等到滿間隔 → 送出；429／5xx 就等 Retry-After 重試
執行示範：python 06-polite/polite_get.py
"""
import os
import time
import urllib.robotparser
from urllib.parse import urljoin

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
USER_AGENT = "course-crawler/1.0 (demo)"
MAX_RETRIES = 3

session = requests.Session()
session.headers["User-Agent"] = USER_AGENT
robots = None        # 讀好的 robots.txt 規則（load_robots 會設定）
interval = 1.0       # 兩次請求至少隔幾秒（load_robots 會依 Crawl-delay 設定）
last_time = 0.0      # 上一次送出請求的時間


def load_robots(base):
    """自己下載 robots.txt，再交給 rp.parse()。
    注意：rp.read() 遇到 429 會當成「全部允許」，被限速時反而失去保護。"""
    global robots, interval
    url = urljoin(base, "robots.txt")
    rp = urllib.robotparser.RobotFileParser()
    for attempt in range(4):
        r = session.get(url, timeout=10)
        if r.status_code == 429:                      # 連 robots.txt 都被限速：等一下再試
            time.sleep(float(r.headers.get("Retry-After", 2 ** attempt)))
            continue
        if r.status_code == 404:
            rp.allow_all = True                       # 沒有 robots.txt：沒有限制，但仍要有禮貌
        elif r.status_code in (401, 403) or r.status_code >= 500:
            rp.disallow_all = True                    # 看不到規則：保守起見全部不爬
        else:
            r.encoding = "utf-8"
            rp.parse(r.text.splitlines())
        robots = rp
        interval = float(rp.crawl_delay(USER_AGENT) or 1)   # 沒寫 Crawl-delay 就 1 秒
        return
    raise RuntimeError(f"拿不到 robots.txt：{url}")


def polite_get(url):
    """有禮貌的 GET。robots.txt 不允許就回傳 None；重試後仍失敗就丟出錯誤。"""
    global last_time
    if not robots.can_fetch(USER_AGENT, url):
        print("略過（robots.txt 不允許）：", url)
        return None
    for attempt in range(MAX_RETRIES + 1):
        wait = interval - (time.monotonic() - last_time)   # 距離上次請求還差幾秒
        if wait > 0:
            time.sleep(wait)
        last_time = time.monotonic()
        r = session.get(url, timeout=10)
        if r.status_code == 429 or r.status_code >= 500:
            retry_after = float(r.headers.get("Retry-After", 2 ** attempt))
            print(f"  {r.status_code}，等 {retry_after:.0f} 秒再試（第 {attempt + 1} 次）")
            time.sleep(retry_after)
            continue
        r.raise_for_status()
        r.encoding = "utf-8"
        return r
    raise RuntimeError(f"重試 {MAX_RETRIES} 次仍失敗：{url}")


if __name__ == "__main__":
    load_robots(BASE)
    print("間隔", interval, "秒")
    for path in ["v1/laws/", "v1/api/laws.json", "v1/admin/"]:
        r = polite_get(BASE + path)
        if r is not None:
            print(r.status_code, path)
