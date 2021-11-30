
const ejs = require('ejs');
const express = require('express')

var app = express.Router();


let isLogined = function (req, res, next) {
    if( req.isAuthenticated() ) {
        return next();
    }else{
        res.redirect("/login");
    }
};


// aboutページのテンプレートを呼び出す
// app.get('/about', ・・・ ではない
app.get('/', isLogined, function (req, res) {
    res.render('pages/about');
});

app.post('/', function (req, res) {
    res.render('pages/about');
});


module.exports = app;
