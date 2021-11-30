
const express = require('express')
var app = express.Router();
//var co = require("co");
//var MongoClient = require("mongodb").MongoClient;
var csrf = require("csurf");
var csrfProtection = csrf({ cookie: true })


/**
 * リクエストボディーからForm入力データを抽出
 */
var extract = function (req) {
  return {
    name:       req.body.name,
    location:   req.body.location,
    tel:        req.body.tel,
    _csrf:      req.body._csrf
  };
};
 
/**
 *  リクエストデータを検証
 */
var validate = function (data) {
  var errors = data.errors = [];
 
  if (!data.name) {
    errors[errors.length] = "会社名を指定してください。";
  }
  if (!data.location) {
    errors[errors.length] = "所在地を指定してください。";
  }
  if (!data.tel) {
    errors[errors.length] = "電話番号を指定してください。";
  }
 
  return errors.length === 0;
};
 
/**
 * リクエストデータを登録
 */
/*
var commit = function (data, callback) {
  const URL = "mongodb://localhost:27017/test";
 
  return co(function* () {
    var db = yield MongoClient.connect(URL);
    var collection = db.collection("shops");
    var result = yield collection.updateOne(
      { name: { $eq: data.name } },
      { $set: data },
      { upsert: true },
      (error, result) => {
        db.close();
        callback && callback();
      });
  }).catch((reason) => {
    console.error(JSON.stringify(reason));
  });
};
*/

app.get("/", csrfProtection, function (req, res) {
    res.redirect('/shop/input');
 });

 
app.get("/input", csrfProtection, function (req, res) {
   // csrfToken付きでページを返す
   res.render('pages/shop/input.ejs', { csrfToken: req.csrfToken() });
});
 

app.post("/input", csrfProtection, function (req, res) {
  // 入力データを取得
  var data = extract(req);
 
  // 入力画面の再表示
  res.render('pages/shop/input.ejs', { data: data });
});


app.post("/confirm", function (req, res) {
  // 入力データを取得
  var data = extract(req);
 
  // 入力データの検証
  if (!validate(data)) {
    return res.render("pages/shop/input.ejs", { data: data });
  }
  res.render("pages/shop/confirm.ejs", data);
});
 

app.post("/complete", function (req, res) {

  if ('btn-back' in req.body) {
    return res.redirect("/shop/input");
  }



  // 入力データを取得
  var data = extract(req);
 
  // 入力データの検証
  if (!validate(data)) {
    return res.render("pages/shop/input.ejs", data);
  }
 
  // 登録処理
  /*
  commit(data).then(() => {
    // 使用済み 秘密文字 と トークン の無効化
    delete req.session._csrf;
    res.clearCookie("_csrf");
 
    // 完了画面へリダイレクト
    res.redirect("pages/shop/complete");
  });
  */

  // 完了画面へリダイレクト
  //res.redirect("pages/shop/complete");
  res.render("pages/shop/complete.ejs", data);
});
 



module.exports = app;





