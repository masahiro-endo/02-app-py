const express = require('express');
const app = express();
// requestを読み込み
const request = require('request');

app.listen(8080, () => {
  console.log('Running at Port 8080...');
});

app.get('/nyaaaaaaaan/:width/:height', (req, res) => {
  // 送受信の設定
  const options = {
    url: 'http://placekitten.com/' + `${req.params.width}/${req.params.height}`,
    method: 'GET',
    encoding: null
  };

  request(options, (err, response, body) => {
    res.set('Content-Type', response.headers['content-type']);
    res.send(body);
  });
});




/**
 * 取得したいサーバのドメイン：https://sample
 * 画像のパス：/thumbnail?id=00000
 */
 const TEST_DOMAIN = 'https://sample';


app.get('/thumbnail', (req, res) => {

    request(TEST_DOMAIN + req.originalUrl)
      // 成功時
      .on('response', (response) => {
        console.log(response.statusCode);
        console.log(response.headers['content-type']);
      })
      // 失敗時
      .on('error', function (err) {
        console.log(err);
        res.sendStatus(404);
      })
      .pipe(res);
});


