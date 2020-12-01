const fs = require("fs");
const child_process = require("child_process");

var flag_watch = true;
var file_watch = "cache/runtime/stamp.pickle";
var algo_list = [
    // "Algo_0xA001.py",
    "Algo_0xA902.py",
    "Algo_0xA801.py",
]

fs.watch(file_watch, (eventType, filename) => {
  if (filename && flag_watch == true) {
    flag_watch = false;
    //console.log(filename);
    algo_list.forEach(triger_cmd)
    // skip triger many times.
    setTimeout(function() {
      flag_watch = true;
    }, 5000);
  }
});

function triger_cmd(algo){
    py_cmd = "python pascal/" + algo
    var workerProcess = child_process.exec(
      py_cmd,
      { windowsHide: true },
      function(error, stdout, stderr) {
        if (error) {
          console.log(error.stack);
          console.log("Error code: " + error.code);
          console.log("Signal received: " + error.signal);
        }
        console.log(stdout);
        console.log(stderr);
      }
    );
}