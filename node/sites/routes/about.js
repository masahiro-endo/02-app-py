
const ejs = require('ejs');
const express = require('express')

var app = express.Router();



// aboutページのテンプレートを呼び出す
app.get('/about', function(req, res) {
    res.render('pages/about');
});

app.post('/about', function(req, res) {
    res.render('pages/about');
});


module.exports = app;
