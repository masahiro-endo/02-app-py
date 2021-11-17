/**
 * /app.js
 */
 const express = require('express');
 const app = express();
 const path = require('path');
 // /api/index.js で定義されたミドルウェア
 const api = require('./api/');
 
 app.listen(8080, () => {
   console.log('Running at Port 8080...');
 });
 
 // APIルーティング用ミドルウェアを/apiに設定
 app.use('/api', api);
 
 app.use(express.static(path.join(__dirname, 'public')));
 
 app.use((req, res) => {
   res.sendStatus(404);
 });

 

 