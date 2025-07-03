import sqlite3
import json

# 連線到 SQLite 資料庫
conn = sqlite3.connect("law_search_database.sqlite")
cursor = conn.cursor()

# 正確的 JOIN 查詢
query = """
SELECT 
  JFT.`Full-Text`,
  CBIF.`J-Summary`,
  CBIF.`Case-Type`
FROM JFT
JOIN CBIF ON JFT.`J-ID` = CBIF.`J-ID`
WHERE 
  JFT.`Full-Text` IS NOT NULL AND
  CBIF.`Case-Type` IS NOT NULL
LIMIT 50
"""

# 執行查詢
results = cursor.execute(query).fetchall()

# 寫入 JSONL 檔案
with open("data.jsonl", "w", encoding="utf-8") as f:
    for row in results:
        # 取出資料並去除換行符號
        full_text = str(row[0]).replace("\n", " ").strip()
        summary = str(row[1]).replace("\n", " ").strip()
        case_type = str(row[2]).replace("\n", " ").strip()

        # 建構 instruction 與 response
        instruction = "閱讀以下判決書內容，並標記其結構化資訊（主文內容、案件類型）"
        input = f"<判決書開始>{full_text}<判決書結束>"
        response = f"摘要:{summary},檔案類型:{case_type}"

        sample = {
            "instruction": instruction,
            "input": input,
            "response": response
        }

        f.write(json.dumps(sample, ensure_ascii=False) + "\n")

print("✅ 共寫入", len(results), "筆乾淨資料到 data.jsonl")
