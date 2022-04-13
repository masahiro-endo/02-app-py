
const ejs = require('ejs');
const express = require('express')
const bodyParser = require('body-parser')
const request = require('request')

var app = express.Router();

//const myAPIkey = '&key=AIzaSyCCwY4crDyUa4d571hBzcb1AH7Rqi09PXU'
const myAPIkey = ''




app.use( bodyParser.urlencoded({
    extended: true
}) );
app.use( bodyParser.json() );

// middleware that is specific to this router
app.use(function timeLog (req, res, next) {
    console.log('Time: ', Date.now());
    next();
});

const myLogger = function (req, res, next) {
    console.log('LOGGED');
    next();
};
app.use(myLogger);

const requestTime = function (req, res, next) {
    req.requestTime = Date.now();
    next();
  };
app.use(requestTime);




app.get('/', (req, res) => {
    const book = '';
    res.render('pages/book', {book: book} );
});

app.post('/', (req, res, next) => {

    const USER_NAME = `dbadmin`;
    const USER_PASSWD = `admin`;
    const HOST_NAME = `cluster0.dxxx6.mongodb.net`;
    //const HOST_NAME = `cluster0-shard-00-01.dxxx6.mongodb.net`;
    const DB_NAME = `myFirstDatabase`;
    const CONNECT_STRING = `mongodb+srv://${USER_NAME}:${USER_PASSWD}@${HOST_NAME}/${DB_NAME}?retryWrites=true&w=majority`;
    /*
    options = {
        method: 'GET',
        host: `${USER_NAME}:${USER_PASSWD}@${HOST_NAME}`,
        port: 27017,
        path: `/${DB_NAME}?retryWrites=true&w=majority`,
        json: true,
        url: `${CONNECT_STRING}`,
        proxy: 'http://test003:password@10.249.1.253:48080',
    };
    */
    console.log('url: ' + options.url);    
    
    request(options, function (error, response, data) {
        if (!error && response.statusCode == 200) {
            data = JSON.stringify(data);
            console.log(data);
            res.render('pages/book', {book: data} );
        }
    });
    
    /*
    https.get(options, (resp) => { 
        let data = ''; 
    
        // A chunk of data has been received. 
        resp.on('data', (chunk) => { 
            data += chunk; 
        }); 
    
        // The whole response has been received. Print out the result. 
        resp.on('end', () => { 
            //console.log(JSON.parse(data).explanation);
            //console.log(data.toString());
            data = JSON.stringify(data);
            console.log(data);
            res.render('pages/book', {book: data} );
        }); 
    
    }).on("error", (err) => { 
        console.log("Error: " + err.message); 
    });
    */

    //unable main process temporary
    // next();

}, (req, res) => {
    console.log("req.requestTime: " + req.requestTime); 
    res.render('pages/about');
});



module.exports = app;

