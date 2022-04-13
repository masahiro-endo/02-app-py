
//var sqlite3 = require('sqlite3').verbose();
let path_db = `../db/db.sqlite3`;


let sql_drop = `drop table if exists m_user`;
let sql_create = `create table if not exists m_user( \
                        id integer primary key autoincrement, \
                        name nverchar(32), \
                        email nverchar(32), \
                        password nverchar(32) \
                        role nverchar(32) `
let sql_insert = `insert into members(name,email,password,role) values(?,?,?,?)`;

const connect = function () {
    const db = new sqlite3.Database(path_db, (err) => {
        if (err) {
            console.error("database error: " + err.message);
        } else {
            return db;
        }
    });
};

var init = function () {
    const db = this.connect();
    db.serialize(() => {
        db.run(sql_drop);
        db.run(sql_create, (err) => {
            if (err) {
                console.error("table error: " + err.message);
            } else {
                //初期データinsert
                var data = [
                    { name: 'hoge', email: '1@1.com', password: '11', role: 'admin' },
                    { name: 'fuga', email: '2@2.com', password: '22', role: 'sales' },
                    { name: 'bar', email: '3@3.com', password: '33', role: 'sales' }
                ];
                data.forEach( function ( row ) {
                    db.run(sql_insert, row.name, row.email, row.password, row.role);
                });
            }
        });
    });
    db.close((err) => {
        if (err) {
          return console.error(err.message);
        }
    });
};
    

var addUser = function (name, email, password, role) {
    const db = this.connect();
    const stmt = db.prepare(sql_insert);
    stmt.run(name, email, password, role, (err) => { //lambda式を使うとthis.lastIDでは取得できない
        if (err) {
            res.status(400).json({
                "status": "error",
                "message": err.message
            });
            return;
        } else {
            res.status(201).json({
                "status": "OK",
                "lastID": stmt.lastID
            });
        }
    });
    db.close((err) => {
        if (err) {
          return console.error(err.message);
        }
    });
};

//get members
app.get("/members", (req, res) => {
    db.all("select * from members", [], (err, rows) => {
        if (err) {
            res.status(400).json({
                "status": "error",
                "message": err.message
            });
            return;
        } else {
            res.status(200).json({
                "status": "OK",
                "members": rows
            });
        }
    });
});

//get member
app.get("/members/:id", (req, res) => {
    const id = req.params.id;
    db.get("select * from members where id = ?", id, (err, row) => {
        if (err) {
            res.status(400).json({
                "status": "error",
                "message": err.message
            });
            return;
        } else {
            res.status(200).json({
                "status": "OK",
                "members": row
            });
        }
    })
})

//update member
app.patch("/members", (req, res) => {
    const reqBody = req.body;
    const stmt = db.prepare("update members set name = ?, age = ? where id = ?");
    stmt.run(reqBody.name, reqBody.age, reqBody.id, (err, result) => {
        if (err) {
            res.status(400).json({
                "status": "error",
                "message": err.message
            });
            return;
        } else {
            res.status(200).json({
                "status": "OK",
                "updatedID": stmt.changes
            });
        }
    })
})

//delete member
app.delete("/members/:id", (req, res) => {
    const id = req.params.id;
    const stmt = db.prepare("delete from members where id = ?");
    stmt.run(id, (err, result) => {
        if (err) {
            res.status(400).json({
                "status": "error",
                "message": err.message
            });
            return;
        } else {
            res.status(200).json({
                "status": "OK",
                "deletedID": stmt.changes
            });
        }
    })
})





module.exports = db;
