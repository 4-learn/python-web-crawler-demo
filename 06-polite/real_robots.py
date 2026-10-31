"""06（進階）｜robotparser 讀真實網站也會出錯：空行與萬用字元 *。

執行：python 06-polite/real_robots.py   （只下載兩個網站的 robots.txt 各一次）
"""
import urllib.robotparser

import requests

UA = "course-crawler/1.0 (demo)"


def check(robots_url, paths, clean=False):
    text = requests.get(robots_url, headers={"User-Agent": UA}, timeout=10).text
    lines = text.splitlines()
    if clean:
        lines = [l for l in lines if l.strip()]          # 把空行拿掉
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(lines)
    site = robots_url.rsplit("/", 1)[0]
    for p in paths:
        print(f"  {'可以爬' if rp.can_fetch(UA, site + p) else '禁止  '}  {p}")


print("全國法規資料庫（原樣交給 parse）：")
check("https://law.moj.gov.tw/robots.txt", ["/", "/api/Ch/Law/JSON"])
print("全國法規資料庫（拿掉空行再 parse）：")
check("https://law.moj.gov.tw/robots.txt", ["/", "/api/Ch/Law/JSON", "/LawClass/LawAll.aspx"], clean=True)
print("勞動部（disallow: /App_Data/*）：")
check("https://www.mol.gov.tw/robots.txt", ["/", "/App_Data/x"])
