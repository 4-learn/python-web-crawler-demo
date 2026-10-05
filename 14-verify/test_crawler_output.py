"""14｜驗證爬蟲輸出：不靠「能跑就好」。

--jsonl 參數定義在 conftest.py。執行：
    pytest -q test_crawler_output.py --jsonl ../05-pagination/N0060001.jsonl
"""
import json
import os
import random

import pytest
import requests

BASE = os.environ.get("PLAYGROUND", "https://4-learn.github.io/crawler-playground/")


@pytest.fixture(scope="module")
def rows(request):
    path = request.config.getoption("--jsonl")
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


@pytest.fixture(scope="module")
def api_articles(rows):
    """用另一個來源（API）當作標準答案。"""
    pcode = rows[0]["pcode"]
    url = BASE + f"v1/api/laws/{pcode}/page-1.json"
    out = []
    while url:
        data = requests.get(url, timeout=10).json()
        out += data["articles"]
        url = requests.compat.urljoin(url, data["next"]) if data["next"] else None
    return out


def test_count_matches_source(rows, api_articles):
    assert len(rows) == len(api_articles)


def test_no_duplicates(rows):
    numbers = [r["article_no"] for r in rows]
    dup = {n for n in numbers if numbers.count(n) > 1}
    assert not dup, f"重複的條號：{dup}"


def test_required_fields(rows):
    for r in rows:
        for key in ("pcode", "article_no", "content", "source_url"):
            assert r.get(key), f"{r.get('article_no')} 缺少 {key}"


def test_random_sample_matches_source(rows, api_articles):
    truth = {a["article_no"]: a["content"] for a in api_articles}
    for r in random.Random(0).sample(rows, k=min(5, len(rows))):
        assert r["content"] == truth[r["article_no"]], f"{r['article_no']} 內容不同"


def test_order_kept(rows, api_articles):
    assert [r["article_no"] for r in rows] == [a["article_no"] for a in api_articles]
