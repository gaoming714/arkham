var express = require('express');
var app = require("express")();
var http = require("http").createServer(app);
var io = require("socket.io")(http);

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.get("/msg/:msg", (req, res) => {
  const msg = req.params.msg;
  io.emit("chat message", msg);
  res.end();
});

app.use(express.static(__dirname + "/static"));
app.use(function (req, res, next) {
      res.status(404)
      res.sendFile(__dirname + "/static/404.html");
      //res.status(404).send("Sorry can't find that!")
})

io.on("connection", (socket) => {
  console.log("a user connected");
  socket.on("chat message", (msg) => {
    console.log("message: " + msg);
    io.emit("chat message", msg);
  });
  socket.on("disconnect", () => {
    console.log("user disconnected");
  });
});

http.listen(6602, () => {
  console.log("listening on *:6602");
});
