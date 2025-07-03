import sqlite3
import re
from tqdm import tqdm

# 主文擷取函式
def extract_summary(text):
    match = re.search(
        r"主\s*文\s*(.+?)(?:\n\s*(?:犯罪事實及理由|事\s*實|理\s*由|\n)|$)",
        text,
        re.DOTALL
    )
    if match:
        summary = match.group(1).strip()
        return re.sub(r'\n+', ' ', summary)  # 移除換行，換成空格
    return None

# 資料庫處理主程序
def process_database(db_path):
    print("🔧 開始處理資料庫...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT `J-ID`, `Full-Text` FROM JFT WHERE `Full-Text` IS NOT NULL")
    rows = cursor.fetchall()

    error_jids = []

    for jid, full_text in tqdm(rows, desc="⏳ 擷取主文進行中"):
        try:
            summary = extract_summary(full_text)
            if summary:
                cursor.execute("UPDATE CBIF SET `J-Summary` = ? WHERE `J-ID` = ?", (summary, jid))
            else:
                error_jids.append(jid)
        except Exception as e:
            print(f"⚠️ 解析錯誤 J-ID: {jid}, 原因: {e}")
            error_jids.append(jid)

    conn.commit()
    conn.close()

    print("✅ 處理完成！")
    if error_jids:
        print("⚠️ 以下 J-ID 未能成功擷取主文，建議人工檢查：")
        print(error_jids)

# 執行入口
if __name__ == "__main__":
    db_path = "law_search_database.sqlite"  # ← 改成你自己的 SQLite 檔名
    process_database(db_path)
