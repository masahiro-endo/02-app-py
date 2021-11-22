
const ejs = require('ejs');
const fs = require('fs');
const express = require('express')

var app = express.Router();
var like;

try { //いいねデータがあれば読み込み。なければいいねが0
  like = fs.readFileSync('./data.txt','UTF-8');
} catch(err){
  like = 0;
}

app.get('/', (req, res) => {
  res.render('pages/like.ejs',{like:like});
});

app.post('/', (req, res) => { //いいねボタンをクリックした時
  like++;

  fs.writeFileSync('./data.txt',String(like));
  res.render('pages/like.ejs',{like:like});
});

module.exports = app;

