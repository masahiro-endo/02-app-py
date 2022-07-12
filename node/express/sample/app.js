
 var path = require('path');
 var fs = require('fs');

 const express = require('express');
 var session = require("express-session");
 var bodyParser = require("body-parser");
 var cookie = require("cookie-parser");
 
 const app = express();
 
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



 // ルーティング設定
 var files = fs.readdirSync(__dirname + '/routes');
 for (var file of files) {
    let buf = file.replace('.js', '').replace('index', '');
    app.use('/' + buf, require('./routes/' + buf));
 }




app.listen(port, () => {
  console.log(`Sample App listening at http://localhost:${port}`)
});

 

 
 app.use((req, res) => {
   res.sendStatus(404);
 });

 
