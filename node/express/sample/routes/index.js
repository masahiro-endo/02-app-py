
const fs = require('fs')
const express = require('express')

var app = express.Router();


// indexのテンプレートを呼び出す
app.get('/', function (req, res) {

  var tagline = "tagline.";

  //const personJSON = JSON.stringify(mascots)
  //fs.writeFileSync('info.json', personJSON)

  //const bufferData = fs.readFileSync('info.json') //02-app-py 直下
  //const dataJSON = bufferData.toString()
  //const mascots = JSON.parse(dataJSON)

  const { parse } = require('csv-parse/sync');
  const inputData = fs.readFileSync('input.csv', { encoding : 'utf8' });
  const mascots = parse(inputData, { columns : true });


  console.log(__dirname + 'public')


  res.render('pages/index', {
      mascots: mascots,
      tagline: tagline
    });
});


module.exports = app;

