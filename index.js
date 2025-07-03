//匯入必要模組
const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

//匯入cbif.js檔匯出的API路由模組
const cbifRoutes = require('./routes/cbif');

//解析 JSON 格式的請求內容
app.use(express.json());

//指定前端網頁的資料夾
app.use(express.static(path.join(__dirname, 'views')));

//當使用者訪問/user時，回傳user.html頁面
app.get('/user', (req, res) => {
  res.sendFile(path.join(__dirname, 'views/user.html'));
});

//掛載API路由模組
app.use('/api', cbifRoutes);
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
