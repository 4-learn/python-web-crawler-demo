"""16｜同一份 JSONL，給不同下游：Pandas 用 CSV、LLM 用 Markdown。

執行：python export.py ../05-pagination/N0060001.jsonl
"""
import csv
import json
import sys
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else "../05-pagination/N0060001.jsonl")
rows = [json.loads(line) for line in src.open(encoding="utf-8")]

# 給 Pandas：固定欄位、用 csv 模組（條文裡有逗號與換行）；utf-8-sig 讓 Excel 正確顯示中文
with open(src.stem + ".csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["pcode", "slug", "article_no", "chapter", "content", "source_url"],
                       extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)

# 給 LLM：每段自己看得懂——帶法規名稱、條號、出處
with open(src.stem + ".md", "w", encoding="utf-8") as f:
    for r in rows:
        f.write(f"## {r['law_name']} {r['article_no']}\n\n{r['content']}\n\n來源：{r['source_url']}\n\n")

with open(src.stem + ".csv", encoding="utf-8-sig") as f:
    print("CSV 讀回", len(list(csv.DictReader(f))), "筆；已輸出", src.stem + ".csv、" + src.stem + ".md")
