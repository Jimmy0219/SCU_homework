import os
import json
import sqlite3

conn = sqlite3.connect("law_search_database.sqlite")
cursor = conn.cursor()
json_folder = "aaa456"

# 讀取資料夾中所有 json 檔案
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        filepath = os.path.join(json_folder, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                item = json.load(f)
        except Exception as e:
            print(f"❌ 讀取 {filename} 時出錯：{e}")
            continue
        JID = item.get("JID")
        JFULL = item.get("JFULL")

        try:
            cursor.execute('''
            INSERT INTO JFT ("J-ID", "Full-Text")
            VALUES (?, ?)
    ''', (JID, JFULL))
            print(f"✅ 已匯入：{filename}")
        except Exception as e:
            print(f"❌ 匯入 {filename} 時出錯：{e}")




conn.commit()
conn.close()
print("🎉 所有 JSON 檔案處理完成。")