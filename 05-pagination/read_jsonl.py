"""05｜JSONL 的關鍵在每筆後面的 "\n"：寫入、漏掉換行、讀回。

執行：python 05-pagination/read_jsonl.py
（第 3 段要先跑過 python 05-pagination/crawl_law.py N0060001）
"""
import json
import os

rows = [
    {"slug": "1", "article_no": "第 1 條", "content": "第一段\n第二段"},
    {"slug": "2", "article_no": "第 2 條", "content": "本法用詞"},
]
os.makedirs("output", exist_ok=True)

print("--- 1. 有 + \"\\n\"：一行一筆 ---")
with open("output/good.jsonl", "w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print(open("output/good.jsonl", encoding="utf-8").read())

print("--- 2. 漏了 + \"\\n\"：全部擠在同一行 ---")
with open("output/bad.jsonl", "w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False))
print(open("output/bad.jsonl", encoding="utf-8").read())
try:
    [json.loads(line) for line in open("output/bad.jsonl", encoding="utf-8")]
except json.JSONDecodeError as e:
    print("讀回失敗：", type(e).__name__, e)

print("\n--- 3. 讀回 crawl_law.py 產生的檔案 ---")
rows = [json.loads(line) for line in open("output/N0060001.jsonl", encoding="utf-8")]
print(len(rows), "條")
print(rows[-1]["article_no"], rows[-1]["source_url"])
