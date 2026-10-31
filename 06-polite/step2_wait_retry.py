"""06｜第二步：固定間隔、遇到 429 依 Retry-After 等待再試。

執行：python 06-polite/step2_wait_retry.py
"""
import os
import time

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
interval = 1.0       # 兩次請求至少隔幾秒
last_time = 0.0      # 上一次送出請求的時間


def wait_and_get(url):
    global last_time
    for attempt in range(4):                                # 最多試 4 次
        wait = interval - (time.monotonic() - last_time)    # 距離上次請求還差幾秒
        if wait > 0:
            time.sleep(wait)
        last_time = time.monotonic()
        r = requests.get(url, headers={"User-Agent": "course-crawler/1.0 (demo)"}, timeout=10)
        if r.status_code == 429 or r.status_code >= 500:
            retry_after = float(r.headers.get("Retry-After", 2 ** attempt))
            print(f"  {r.status_code}，等 {retry_after:.0f} 秒再試")
            time.sleep(retry_after)
            continue                                        # 再試一次
        return r
    raise RuntimeError(f"試了 4 次仍失敗：{url}")


start = time.monotonic()
for n in [1, 2, 3]:
    r = wait_and_get(BASE + f"v1/api/laws/N0030001/page-{n}.json")
    print(f"{time.monotonic() - start:4.1f} 秒  {r.status_code}  page-{n}.json")
