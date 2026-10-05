"""03 補充｜真實世界的「先找 API」：全國法規資料庫開放資料。

law.moj.gov.tw 的 robots.txt 是 Disallow: /，不能爬網頁；但官方提供整包 JSON。
這支程式約下載 6 MB，請不要在課堂上全班同時執行，老師示範一次即可。

執行：python moj_open_data.py
"""
import io
import json
import zipfile

import requests

API = "https://law.moj.gov.tw/api/Ch/Law/JSON"  # 文件：https://law.moj.gov.tw/api/swagger/docs/v1

r = requests.get(API, headers={"User-Agent": "course-crawler/1.0 (demo)"}, timeout=120)
r.raise_for_status()
with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
    print("ZIP 內容：", zf.namelist())
    data = json.loads(zf.read("ChLaw.json").decode("utf-8-sig"))

print("資料更新日期：", data["UpdateDate"], "，共", len(data["Laws"]), "部法律")
law = next(l for l in data["Laws"] if l["LawURL"].endswith("pcode=N0030001"))
print(law["LawName"], law["LawModifiedDate"], len(law["LawArticles"]), "筆（含章節標題）")
