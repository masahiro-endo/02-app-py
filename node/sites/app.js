
var path = require('path');

//Express フレームワークを読み込む
var express = require('express');
var app = express();
const port = 8080


// ビューエンジンをejsにセットする
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.engine('ejs', require('ejs').renderFile);


// indexのテンプレートを呼び出す
app.get('/', function(req, res) {
  var mascots = [
    { name: 'Sammy', organization: "DigitalOcean", birth_year: 2012},
    { name: 'Tux', organization: "Linux", birth_year: 1996},
    { name: 'Moby Dock', organization: "Docker", birth_year: 2013}
  ];
  var tagline = "No programming concept is complete without a cute animal mascot.";

  res.render('pages/index', {
    mascots: mascots,
    tagline: tagline
  });
});

// aboutページのテンプレートを呼び出す
app.get('/about', function(req, res) {
  res.render('pages/about');
});


app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})



