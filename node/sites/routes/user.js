
var express = require('express');
var app = express.Router();
var userController = require('../controllers/UserController')

app.get('/users', function(req, res) {
    userController.doGetUser
});
app.get('/users/regist', function(req, res) {
    userController.doRegistUser
});


module.exports = app;

