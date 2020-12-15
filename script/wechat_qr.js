var request = require('request');
var http = require('http');
var fs = require('fs');
var shell = require('shelljs');

shell.config.silent = true;

http.createServer(function (req,res) {
    request('http://127.0.0.1:9000/login', function (error, response, body) {
        if (!error && response.statusCode == 200) {
                console.log(body) // 请求成功的处理逻辑
                }
    });

//    res.writeHead(200, {'Content-Type': 'image/png'});
//    setTimeout(function(){
//        fs.createReadStream('./QR.png').pipe(res);
//        }, 5000);

    var waitingnum = 0;
    var timer = setInterval(function() {
        var result = shell.find('./QR.png');
        if (result.code === 0 ) {
            clearTimeout(timer);
            res.writeHead(200, {'Content-Type': 'image/png'});
            fs.createReadStream('./QR.png').pipe(res);
            return
        }
        else if (waitingnum >6){
            clearTimeout(timer);
            res.writeHead(200, {'Content-Type': 'image/png'});
            fs.createReadStream('./zip/Bizarremyview.png').pipe(res);
            return
        }
        else {
            waitingnum = waitingnum +1;
        }
    }, 500);

}).listen(6600);
console.log("Start server at 6600");
