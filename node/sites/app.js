
var path = require('path');

//Express フレームワークを読み込む
var express = require('express');
var app = express();
const port = 8080


// ビューエンジンをejsにセットする
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.engine('ejs', require('ejs').renderFile);




// aboutページのテンプレートを呼び出す
app.get('/about', function(req, res) {
  res.render('pages/about');
});



var indexRouter = require('./routes/index');
var likeRouter = require('./routes/like');
var userRouter = require('./routes/user');
var aboutRouter = require('./routes/about');
app.use('/', indexRouter);
app.use('/like', likeRouter);
app.use('/user', userRouter);
app.use('/about', aboutRouter);



// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {

  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});



app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})



