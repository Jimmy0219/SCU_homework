//匯入必要模組
const express = require('express');
const router = express.Router();
//匯入sqlite.js檔匯出的資料庫連線物件
const db = require('../db/sqlite');

//基本查詢（取得表CBIF中所有的資料）
router.get('/users', (req, res) => {
  db.all('SELECT * FROM CBIF', (err, rows) => {
    if (err) return res.status(500).json({ error: '資料讀取錯誤' });
    res.json({ users: rows });
  });
});

//進階查詢（支援模糊比對的條件查詢）
router.get('/advanced-search', (req, res) => {
  const { titleKeyword, summaryKeyword, caseType } = req.query;

  const query = `
  SELECT * FROM CBIF
  WHERE
    ("Case-Type" LIKE ? OR ? = '') AND
    ("J-Title" LIKE ? OR ? = '') AND
    ("J-Summary" LIKE ? OR ? = '')
`;
//在查詢參數前後加上 %，達成模糊查詢效果
  const values = [
    `%${caseType}%`, caseType,
    `%${titleKeyword}%`, titleKeyword,
    `%${summaryKeyword}%`, summaryKeyword
  ];

  db.all(query, values, (err, rows) => {
    if (err) return res.status(500).json({ error: '搜尋失敗' });
    res.json({ users: rows });
  });
});

//匯出路由模組，供主伺服器掛載使用
module.exports = router;
