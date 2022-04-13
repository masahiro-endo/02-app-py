
const ejs = require('ejs');
const express = require('express')
var passport = require('passport');
var mongoose = require("mongoose");
const request = require('request')

var app = express.Router();
const User = require("../models/user.js");

/*
const USER_NAME = `dbadmin`;
const USER_PASSWD = `admin`;
const HOST_NAME = `cluster0.dxxx6.mongodb.net`;
//const HOST_NAME = `cluster0-shard-00-01.dxxx6.mongodb.net`;
const DB_NAME = `myFirstDatabase`;
const CONNECT_STRING = `mongodb+srv://${USER_NAME}:${USER_PASSWD}@${HOST_NAME}/${DB_NAME}?retryWrites=true&w=majority`;
const options = {
  useUnifiedTopology: true,
  useNewUrlParser: true,
};

mongoose.connect(
  CONNECT_STRING,
  options
);
*/

//const db = mongoose.connection;
//db.on('error', console.error.bind(console, 'DB connection error:'));
//db.once('open', () => console.log('DB connection successful'));





/*
var proxy = request.defaults({'proxy': 'http://10.249.1.253:48080/'})

console.log(CONNECT_STRING);
proxy.get(connectString, function (error, response, body) {
  console.log(response.statusCode);
  console.log(error);
  if (!error && response.statusCode == 200) {
    console.log(body);
  }
});
//var server = http.createServer(function (req, res) {
//  proxy.get('http://www.google.co.jp/').pipe(res)
//});
//server.listen(10000);

*/

// 認可処理。指定されたロールを持っているかどうか判定します。
var authorize = function (role) {
  return function (request, response, next) {
      if (request.isAuthenticated() &&
          request.user.role === role) {
          return next();
      }
      response.redirect("/auth");
  };
};




app.get('/', function (req, res) {
    res.render('pages/auth', { message: req.flash('error')});
});

app.post('/', authorize("group1"), 
  passport.authenticate('local', {
    successRedirect: '/pages/about',　//ログイン成功時に遷移したい画面
    failureRedirect: '/pages/auth', //ログイン失敗時に遷移したい画面
    session: true,
    failureFlash: true
  })
);

app.get('/create', async (req, res) => {
  const insert = await row({
    id:       "tanaka",
    email:    "tanaka@sample.com",
    name:     "tanaka",
    password: "password",
    role:     "group1"
  });

  await insert.save();
  res.status(200).json(insert);
});
/*
app.get('/create', (req, res) => {
  User.create(
    {
      id:       "tanaka",
      email:    "tanaka@sample.com",
      name:     "tanaka",
      password: "password",
      role:     "group1"
    },
    (err, data) => {
      if (err) {
        res.status(500).json(err);
      }
      res.status(200).json(data);
    }
  );

client.connect(err => {

  const collection = client.db('test').collection('devices');
  // perform actions on the collection object
  console.log('Connected successfully to server');

  const documents = [
    { a: 1 },
    { a: 2 },
    { a: 3 }
  ];

  collection.insertMany(documents, (err, result) => {
    console.log('Inserted 3 documents into the collection');
    console.log(result);
    client.close();
  })

});

*/

app.get('/list', async (req, res) => {
  const Users = await User.find({});
  res.status(200).json(Users);
});



module.exports = app;
