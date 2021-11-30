
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
//app.use(session({ secret: "YOUR SECRET SALT", resave: true, saveUninitialized: true }));
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


// ハッシュ値を求めるために必要なもの
var crypto = require("crypto");
var secretKey = "some_random_secret";
var getHash = function(target){
        var sha = crypto.createHmac("sha256", secretKey);
            sha.update(target);
                return sha.digest("hex");
};

//Expressを使用している場合はInitializeが必要
app.use(passport.initialize());
app.use(passport.session());
app.use(flash());

// passportでのセッション設定
passport.serializeUser(function(user, done){
  done(null, {email: user.email, _id: user._id});
});
passport.deserializeUser(function(serializedUser, done){
  User.findById(serializedUser._id, function(err, user){
      done(err, user);
  });
});

passport.use( new LocalStrategy( 
  {
    userNameField:'username',
    passwordField:'password',
    passReqToCallback: true
  }, 
  function (req, username, password, done) {
    process.nextTick( function() {
      //処理書く
    　//ユーザ名、パスワード不正時の処理を記述する
      var hashedPassword = getHash(password);

      if (!username) {
          return done(null, false, { message: 'Username is incorrect' })
      //↓にはPasswordチェック処理を実装してください。
      } else if (hashedPassword !== password) {
          return done(null, false, { message: 'Password is incorrect' })
      } else {
          console.log("username" + username);
          return done(null, username);
      }
  })
}));





// ルーティング設定
//app.use('/routes', express.static(__dirname + '/routes'));
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



