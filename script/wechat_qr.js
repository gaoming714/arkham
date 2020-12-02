var request = require('request');
var http = require('http');
var fs = require('fs');
http.createServer(function (req,res) {
    request('http://127.0.0.1:9000/login', function (error, response, body) {
        if (!error && response.statusCode == 200) {
                console.log(body) // 请求成功的处理逻辑
                }
    });
    res.writeHead(200, {'Content-Type': 'image/png'});

    setTimeout(function(){
        fs.createReadStream('./QR.png').pipe(res);
        }, 5000);

}).listen(6600);
console.log("Start server at 3000");
