
var path = require('path');

//Express フレームワークを読み込む
var express = require('express');
var app = express();
const port = 8080


// ビューエンジンをejsにセットする
app.set('views', path.join(__dirname, 'views/'));
app.set('view engine', 'ejs');
app.engine('ejs', require('ejs').renderFile);




var indexRouter = require('./routes/index');
var likeRouter = require('./routes/like');
var userRouter = require('./routes/user');
var bookRouter = require('./routes/book');
var aboutRouter = require('./routes/about');
app.use('/', indexRouter);
app.use('/like', likeRouter);
app.use('/user', userRouter);
app.use('/book', bookRouter);
app.use('/about', aboutRouter);



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



app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})



