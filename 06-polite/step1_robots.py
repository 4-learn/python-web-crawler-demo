"""06｜第一步：讀 robots.txt，每次請求前先問「能不能爬」。

執行：python 06-polite/step1_robots.py
"""
import os
import urllib.robotparser
from urllib.parse import urljoin

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
USER_AGENT = "course-crawler/1.0 (demo)"

# 自己下載 robots.txt，再交給 parse()（不用 rp.read()，原因見講義第 4 段）
r = requests.get(urljoin(BASE, "robots.txt"), headers={"User-Agent": USER_AGENT}, timeout=10)
r.encoding = "utf-8"
robots = urllib.robotparser.RobotFileParser()
robots.parse(r.text.splitlines())

interval = float(robots.crawl_delay(USER_AGENT) or 1)   # 沒寫 Crawl-delay 就 1 秒
print("間隔", interval, "秒")

for path in ["v1/laws/", "v1/api/laws.json", "v1/admin/"]:
    if robots.can_fetch(USER_AGENT, BASE + path):
        print("可以爬", path)
    else:
        print("略過  ", path)
