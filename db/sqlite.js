//匯入必要模組
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
//組合出資料庫檔案的完整路徑
const dbPath = path.join(__dirname, '../law_search_database.sqlite');
//使用模組sqlite3建立連線
const db = new sqlite3.Database(dbPath);
//將連線物件匯出，供其他模組使用
module.exports = db;
