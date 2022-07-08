
 var path = require('path');
 var fs = require('fs');

 const express = require('express');
 const app = express();
 
 const port = 8080


 

 app.use(express.static(path.join(__dirname, 'public')));

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

 
