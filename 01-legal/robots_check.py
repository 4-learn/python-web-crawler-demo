"""01｜讀 robots.txt：判斷某個網址能不能爬。

執行：python robots_check.py
"""
import os
import urllib.robotparser

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")
USER_AGENT = "course-crawler/1.0 (demo)"

rp = urllib.robotparser.RobotFileParser(BASE + "robots.txt")
rp.read()

print("Crawl-delay:", rp.crawl_delay(USER_AGENT))
for path in ["v1/laws/", "v1/api/laws.json", "v1/admin/", "v2/admin/"]:
    ok = rp.can_fetch(USER_AGENT, BASE + path)
    print(f"{'可以爬' if ok else '禁止  '}  {BASE + path}")

# 換一個在 robots.txt 被點名的 User-Agent
print("BadBot 可以爬首頁嗎？", rp.can_fetch("BadBot", BASE))
