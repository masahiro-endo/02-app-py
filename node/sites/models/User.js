
const mongoose = require("mongoose");
 
const UserSchema = mongoose.Schema({
    "id":       String,
    "email":    String,
    "name":     String,
    "password": String,
    "role":     String
});
 
module.exports = mongoose.models.User || mongoose.model("User", UserSchema);
