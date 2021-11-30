
const ejs = require('ejs');
const express = require('express')
const bodyParser = require('body-parser')
const request = require('request')
var app = express.Router();

const tunnel = require('tunnel');
const https = require('https');
const myAPIkey = 'AIzaSyCCwY4crDyUa4d571hBzcb1AH7Rqi09PXU'




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
    res.render('pages/book');
});

app.post('/', (req, res, next) => {

    const tunnelAg = tunnel.httpsOverHttp({
        proxy: {
            host: '10.249.1.253',
            port: 48080
        }
    });
    
    options = {
        method: 'GET',
        host: 'www.googleapis.com',
        port: 443,
        path: `/books/v1/volumes?q=isbn:${req.body.isbn}&key=${myAPIkey}`,
        agent: tunnelAg,
        json: true,
        url: `https://www.googleapis.com/books/v1/volumes?q=isbn:${req.body.isbn}&key=${myAPIkey}`,
    };
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

