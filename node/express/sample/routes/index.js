
const express = require('express')

var app = express.Router();


// indexのテンプレートを呼び出す
app.get('/', function (req, res) {
    res.render('pages/index', {
      mascots: mascots,
      tagline: tagline
    });
});


module.exports = app;

