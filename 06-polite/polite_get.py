"""06｜有禮貌的 GET：先查 robots.txt、固定間隔、遇到 429 依 Retry-After 重試。

其他程式可以 from polite_get import PoliteSession 重複使用。
執行示範：python polite_get.py
"""
import os
import time
import urllib.robotparser
from urllib.parse import urljoin

import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")


class Blocked(Exception):
    """robots.txt 不允許，或重試後仍被拒絕。"""


class PoliteSession:
    def __init__(self, base: str, user_agent: str, min_interval: float | None = None, max_retries: int = 3):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = user_agent
        self.user_agent = user_agent
        self.robots = self._load_robots(urljoin(base, "robots.txt"))
        delay = self.robots.crawl_delay(user_agent)
        self.min_interval = min_interval if min_interval is not None else float(delay or 1)
        self.max_retries = max_retries
        self._last = 0.0

    def _load_robots(self, url: str) -> urllib.robotparser.RobotFileParser:
        """自己下載 robots.txt。
        注意：rp.read() 遇到 429、404 等狀態碼會當成「全部允許」，被限速時反而失去保護。"""
        rp = urllib.robotparser.RobotFileParser(url)
        for attempt in range(4):
            r = self.session.get(url, timeout=10)
            if r.status_code == 429:
                time.sleep(float(r.headers.get("Retry-After", 2 ** attempt)))
                continue
            if r.status_code == 404:
                rp.allow_all = True  # 沒有 robots.txt：沒有限制，但仍要有禮貌
            elif r.status_code in (401, 403) or r.status_code >= 500:
                rp.disallow_all = True  # 看不到規則：保守起見全部不爬
            else:
                r.encoding = "utf-8"
                rp.parse(r.text.splitlines())
            return rp
        raise Blocked(f"拿不到 robots.txt：{url}")

    def get(self, url: str) -> requests.Response:
        if not self.robots.can_fetch(self.user_agent, url):
            raise Blocked(f"robots.txt 不允許：{url}")
        for attempt in range(self.max_retries + 1):
            wait = self.min_interval - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
            r = self.session.get(url, timeout=10)
            if r.status_code == 429 or r.status_code >= 500:
                retry_after = float(r.headers.get("Retry-After", 2 ** attempt))
                print(f"  {r.status_code}，等 {retry_after:.0f} 秒再試（第 {attempt + 1} 次）")
                time.sleep(retry_after)
                continue
            r.raise_for_status()
            r.encoding = "utf-8"
            return r
        raise Blocked(f"重試 {self.max_retries} 次仍失敗：{url}")


if __name__ == "__main__":
    s = PoliteSession(BASE, "course-crawler/1.0 (demo)")
    print("間隔", s.min_interval, "秒")
    for path in ["v1/laws/", "v1/api/laws.json", "v1/admin/"]:
        try:
            r = s.get(BASE + path)
            print(r.status_code, path)
        except Blocked as e:
            print("略過：", e)
