
const ejs = require('ejs');
const express = require('express')

var app = express.Router();



// aboutページのテンプレートを呼び出す
// '/about' ではない
app.get('/', function (req, res) {
    res.render('pages/about');
});

app.post('/', function (req, res) {
    res.render('pages/about');
});


module.exports = app;
