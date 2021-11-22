
const express = require('express');
const User = require('../models/User');
const Views = '../views/'


var doGetUser = function (req, res, next) {
  Users.getUser(id).then((result) => {
    res.render(Views + 'user.ejs',{users: result});
  });
}

var Create = function (req, res) {
  var nombre = req.body.nombre;
  var apellido = req.body.apellido;
  var nick = req.body.username;
  console.log("Datos" + nombre + apellido + nick);

  User.create( 
    {
      nombre:nombre,
      apellido:apellido,
      username:nick
    },
    function (err, usr) {
      if (err) {
        console.log("Error");
      } else {
        console.log("");
      }
  });

  User.find({}, function (err, user) {
    if (err) {
      console.log("Error");
    } else {
      console.log("" + user)
      res.json(user);
    }
  });

};

var Read = function (req, res) {
  User.find({}, function (err, user) {
    if (err) {
      return console.log("error=" + err);
    } else {
       res.json(user);
    }        
  });
};

var Update = function (req, res) {
  User.update( {_id : req.params.todo_id},
                {
                  $set:{
                    nombre: req.body.nombre,
                    apellido: req.body.apellido,
                    username: req.body.username
                  }
                }, 
                function (err, persona) {
                    if (err) {
                        res.send(err);
                    }
                    // Obtine y devuelve todas las personas tras crear una de     ellas
                    User.find( 
                      function (err, user) {
                        if (err) {
                          res.send("Ha habido un error" + err)
                        } else {
                          console.log("Se va a enviar " + persona)
                          res.json(user);
                        }
                      }
                    );
  });
};


var Delete = function (req, res) {
  User.remove(
    {
      _id: req.params.todo_id
    }, 
    function (err, todo) {
      if(err){
        res.send("Error"+err);
      } else {
        console.log("")
      }
    }
  );

  User.find({}, 
            function (err, todos) {
              if (err) {
                res.send(err);
              } else {
                res.json(todos);
              }
            });
};



module.exports = {
  doGetUser: doGetUser,
  Create: Create,
  Update: Update,
  Read: Read,
  Delete: Delete
}

