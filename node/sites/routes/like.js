
const ejs = require('ejs');
const fs = require('fs');
const express = require('express')

var app = express.Router();
var like = 0;


//いいねデータがあれば読み込み。なければいいねが0
try {
  like = fs.readFileSync('./data.txt','UTF-8');
} catch (err) {
  like = 0;
}


app.get('/', (req, res) => {
  res.render('pages/like', {like: like});
});

//いいねボタンをクリックした時
app.post('/', (req, res) => {
  like++;
  fs.writeFileSync('./data.txt',String(like));

  res.render('pages/like', {like: like});
});



module.exports = app;

