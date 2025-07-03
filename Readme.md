# 法律判決書查詢系統 

本專案是一個以 Node.js + Express 架設的後端查詢系統，搭配 SQLite 資料庫，並整合 Python 工具進行法律判決書的資料前處理與匯入，支援網頁端查詢與關鍵字檢索。

## 目錄說明

將原先的模板檔案拆分成不同檔案，在使用導入或匯出的應用，以便未來進行維護與修改：

### 主要檔案架構

- **db/sqlite.js：** 資料庫連線模組（原先於index.js）。
- **node_modules：** 存放伺服器相依套件。
- **routes/cbif.js：** 路由模組（原先於index.js）。
- **views：** HTML前端頁面及其CSS檔。
- **index.js：** 伺服器主程式。載入靜態 HTML 頁面 /user，並將 /api/* 路由導向 cbif.js。
- **package-lock.json：** 記錄安裝套件的確切版本。
- **package.json：** 套件與指令設定檔。
- **law_search_database.sqlite：** 資料庫，儲存判決書結構化資料。

### 協助整理資料之Python工具

- **import_json_to_CBIF.py ：** 匯入 JSON 到 CBIF 表格。
- **import_json_to_JFT.py ：** 匯入 JSON 到 JFT 表格。
- **extract_j_summary.py ：** 擷取主文摘要段落工具。

## 個檔案功能介紹

主要拆分為前端、API路由，以及協助大筆資料處理的Python工具

### 前端頁面功能

使用者可在頁面上操作三項主要功能：

一、進階查詢表單：以「案件標題」、「主文關鍵字」、「案件類別」為條件進行模糊查詢

二、PDF 檔案欄位：直接從表格中下載對應案件 PDF 檔案

三、查看全部資料：重置查詢結果並顯示出全部資料

查詢邏輯會透過 JavaScript 觸發 fetch 或 XMLHttpRequest 對 /api/users 或 /api/advanced-search 發出 GET 請求，並將回傳結果動態插入 <table> 中。

### API 路由說明

由 routes/cbif.js 提供以下 API：

users：撈取 CBIF 資料表所有紀錄
advanced-search：根據三個欄位進行模糊查詢（案件標籤、主文關鍵字、案件類別）

### Python 工具說明

import_json_to_CBIF.py：將 JSON 格式的案件結構化資料匯入 CBIF 表格
import_json_to_JFT.py：將 JSON 判決全文匯入 JFT 表格
extract_j_summary.py：自動擷取每份判決中的主文段落，未來可用於摘要訓練或搜尋強化

## 資料庫結構說明

將判決書檔案（Json檔）中不同Key值內的內容做出區分及正規化處理，讓資料進行有效的分類：

### 表格 CBIF

以下是個欄位的名稱及其說明：
J-ID：判決編號（主鍵）
J-Title：判決標題
J-Date：判決日期
J-Summary：主文摘要
Case-Type：案件類型（刑事、民事等）
J-PDF：PDF的檔案連結

### 表格 JFT

以下是個欄位的名稱及其說明：
J-ID：判決編號（對應 CBIF）
Full-Text：判決全文內容

## 特別標注與未來延伸應用
由於諸多原因，導致有些判決書中並沒有明顯的主文段落。
例如：
一、裁定或簡式程序判決，可能不採用明顯的「主文」標題。
二、主文被嵌在開頭或事實段落中。
三、判決未完成上傳格式標準化。

以上問題都會導致無法用簡易的Python指令處理資料龐大的判決書文本，故某些J-Summary欄位中會顯示“此判決書無主文段落”。
一來是增加閱讀體驗。
二來是若未來會將以上資料庫內容延伸至模型訓練的資料集，進而訓練模型理解其中語意並生成判決書簡介（並非截取）。資料內容中若出現“此判決書無主文段落”或是“NULL”怕會影響模型學習而造成語意污染（誤以為這樣的句子也是主文的一種）。