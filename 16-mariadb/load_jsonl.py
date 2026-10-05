"""16｜把爬到的 JSONL 寫進 MariaDB：參數化查詢 + upsert。

連線設定讀環境變數（不要把密碼寫進程式）：
    export DB_HOST=127.0.0.1 DB_USER=crawler DB_PASS=... DB_NAME=crawler_course
執行：python load_jsonl.py ../05-pagination/N0060001.jsonl
連續執行兩次：第二次應顯示「新增 0、更新 0、未變 N」。
"""
import datetime as dt
import hashlib
import json
import os
import sys

import mariadb  # pip install mariadb==1.1.14（需先 sudo apt install libmariadb-dev）

UPSERT = """
INSERT INTO law_articles
  (pcode, law_name, slug, article_no, chapter, content, source_url, content_hash, fetched_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE
  law_name = VALUES(law_name), article_no = VALUES(article_no), chapter = VALUES(chapter),
  content = VALUES(content), source_url = VALUES(source_url),
  content_hash = VALUES(content_hash), fetched_at = VALUES(fetched_at)
"""


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    now = dt.datetime.now().replace(microsecond=0)

    conn = mariadb.connect(host=os.environ.get("DB_HOST", "127.0.0.1"), port=int(os.environ.get("DB_PORT", 3306)),
                           user=os.environ["DB_USER"], password=os.environ["DB_PASS"],
                           database=os.environ.get("DB_NAME", "crawler_course"))
    try:
        cur = conn.cursor()
        with open(os.path.join(os.path.dirname(__file__), "schema.sql"), encoding="utf-8") as f:
            cur.execute(f.read())

        cur.execute("SELECT pcode, slug, content_hash FROM law_articles")
        existing = {(p, s): h for p, s, h in cur.fetchall()}
        stats = {"新增": 0, "更新": 0, "未變": 0}
        for r in rows:
            h = r.get("content_hash") or hashlib.sha256(r["content"].encode("utf-8")).hexdigest()
            key = (r["pcode"], r["slug"])
            if key not in existing:
                stats["新增"] += 1
            elif existing[key] != h:
                stats["更新"] += 1
            else:
                stats["未變"] += 1
                continue  # 沒變就不寫，fetched_at 也不動
            cur.execute(UPSERT, (r["pcode"], r["law_name"], r["slug"], r["article_no"], r.get("chapter", ""),
                                 r["content"], r["source_url"], h, r.get("fetched_at", now)))
        conn.commit()
        print(stats)
        cur.execute("SELECT COUNT(*) FROM law_articles WHERE pcode = ?", (rows[0]["pcode"],))
        print("資料表中", rows[0]["pcode"], "共", cur.fetchone()[0], "條")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main(sys.argv[1])
