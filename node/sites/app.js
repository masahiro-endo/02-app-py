
var path = require('path');
var fs = require('fs');

//Express フレームワークを読み込む
var express = require('express');
var session = require("express-session");
var bodyParser = require("body-parser");
var cookie = require("cookie-parser");
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
const flash = require('connect-flash');

var app = express();
const port = 8080



// ビューエンジンをejsにセットする
app.set('views', path.join(__dirname, 'views/'));
app.set('view engine', 'ejs');
app.engine('ejs', require('ejs').renderFile);
app.use('/public', express.static(__dirname + '/public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cookie());
//express-sessionモジュールを設定する
app.use(session( {
    secret: 'secret key',
    resave: false,
    saveUninitialized: false,
    cookie: {
      maxAge: 1 * 24 * 60 * 1000,
      secure: false
    }
}));


//Expressを使用している場合はInitializeが必要
app.use(passport.initialize());
app.use(passport.session());
app.use(flash());



// passport が ユーザー情報をシリアライズすると呼び出されます
passport.serializeUser(function (id, done) {
  done(null, id);
});
// passport が ユーザー情報をデシリアライズすると呼び出されます
passport.deserializeUser(function (id, done) {
  User.findById(id, (err, user) => {
      if (err) {
          return done(err);
      }
      done(null, user);
  });
});

// passport における具体的な認証処理を設定します。
passport.use(
  "auth",
  new LocalStrategy({
      usernameField: "username",
      passwordField: "password",
      passReqToCallback: true
  }, function (request, username, password, done) {
      process.nextTick(() => {
          User.findOne({ "email": username }, function (error, user) {
              if (error) {
                  return done(error);
              }
              if (!user || user.password != password) {
                  return done(null, false, request.flash("message", "Invalid username or password."));
              }
              // 保存するデータは必要最低限にする
              return done(null, user._id);
          });
      });
  })
);





// ルーティング設定
// var indexRouter = require('./routes/index');
// app.use('/', indexRouter);
var files = fs.readdirSync(__dirname + '/routes');
for (var file of files) {
    let buf = file.replace('.js', '').replace('index', '');
    app.use('/' + buf, require('./routes/' + buf));
}



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

  // 出力するデータ
  var data = {
    method: req.method,
    protocol: req.protocol,
    version: req.httpVersion,
    url: req.url,
    name: err.name,
    message: err.message,
    stack: err.stack
  };

  // render the error page
  res.status(err.status || 500);
  if (req.xhr) {
    res.json(data);
  } else {
    res.render('pages/error', { err: err, data: data });
  }
});






app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})



