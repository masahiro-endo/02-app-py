
const ejs = require('ejs');
const express = require('express')
var passport = require('passport');

var app = express.Router();



app.get('/', function (req, res) {
    res.render('pages/auth', { message: req.flash('error')});
});

app.post('/', 
  passport.authenticate('local', {
    successRedirect: '/pages/about',　//ログイン成功時に遷移したい画面
    failureRedirect: '/pages/auth', //ログイン失敗時に遷移したい画面
    session: true,
    failureFlash: true
  })
);



module.exports = app;
