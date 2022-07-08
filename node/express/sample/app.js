
 const express = require('express');
 const app = express();
 const path = require('path');
 const api = require('./api/');
 
 const port = 8080



app.listen(port, () => {
  console.log(`Sample App listening at http://localhost:${port}`)
});

 

 app.use('/api', api);
 
 app.use(express.static(path.join(__dirname, 'public')));
 
 app.use((req, res) => {
   res.sendStatus(404);
 });

 
