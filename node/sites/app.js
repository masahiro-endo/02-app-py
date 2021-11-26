
var path = require('path');

//Express フレームワークを読み込む
var express = require('express');
var cookie = require("cookie-parser");
var session = require("express-session");
var bodyParser = require("body-parser");
var app = express();
const port = 8080


// ビューエンジンをejsにセットする
app.set('views', path.join(__dirname, 'views/'));
app.set('view engine', 'ejs');
app.engine('ejs', require('ejs').renderFile);
app.use('/static', express.static(__dirname + '/public'));
app.use(cookie());
app.use(session({ secret: "YOUR SECRET SALT", resave: true, saveUninitialized: true }));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());



var indexRouter = require('./routes/index');
var likeRouter = require('./routes/like');
var userRouter = require('./routes/user');
var bookRouter = require('./routes/book');
var shopRouter = require('./routes/shop');
var aboutRouter = require('./routes/about');
app.use('/', indexRouter);
app.use('/like', likeRouter);
app.use('/user', userRouter);
app.use('/book', bookRouter);
app.use('/shop', shopRouter);
app.use('/about', aboutRouter);


/*
//catch all endpoint will be Error Page
app.get('*', function (req, res) {
  if (req.accepts('html')) {
     res.send('404', '<script>location.href = "/the-404-page.html";</script>');
     return;
  }
});

// catch 404 and forward to error handler
app.use( function (req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use( function (err, req, res, next) {

  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('pages/error', { error: err });
});
*/


// カスタムエラーページ
app.use(function (request, response, next) {
  // 出力するデータ
  var data = {
      method: request.method,
      protocol: request.protocol,
      version: request.httpVersion,
      url: request.url
  };

  // エラーを返却
  response.status(404);
  if (request.xhr) {
      response.json(data);
  } else {
      response.render('pages/404', { data: data });
  }
});
app.use(function (error, request, response, next) {
  // 出力するデータ
  var data = {
      method: request.method,
      protocol: request.protocol,
      version: request.httpVersion,
      url: request.url,
      name: error.name,
      message: error.message,
      stack: error.stack
  };

  response.status(500);
  if (request.xhr) {
      response.json(data);
  } else {
      response.render('pages/500', { data: data });
  }
});



app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})



