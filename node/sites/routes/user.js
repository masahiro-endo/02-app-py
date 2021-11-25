
var express = require('express');
var userController = require('../controllers/UserController')
var app = express.Router();



app.get('/', function(req, res) {
    userController.doGetUser
});
app.get('/regist', function(req, res) {
    userController.doRegistUser
});


module.exports = app;

