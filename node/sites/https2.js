/*
 * https2.js
 * Copyright (C) 2014 kaoru <kaoru@bsd>
 */
//var https = require('https');
var http = require('http');
var fs = require('fs');
//var ssl_server_key = 'server_key.pem';
//var ssl_server_crt = 'server_crt.pem';
 
var http_port = 8080;
//var https_port = 8443;

//var options = {
//        key: fs.readFileSync(ssl_server_key),
//        cert: fs.readFileSync(ssl_server_crt)
//};
 
//https.createServer(options, function (req,res) {
//        res.writeHead(200, {
//                'Content-Type': 'text/plain'
//        });
//        res.end("Hello, world on https\n");
//}).listen(https_port);
 
http.createServer(function (req,res) {
        res.writeHead(200, {
                'Content-Type': 'text/plain'
        });
        res.end("Hello, world on http\n");
}).listen(http_port);

