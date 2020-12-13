const { watch } = require('gulp');
const shell = require('shelljs');
const fs = require('fs');

var file_stamp = "cache/runtime/stamp.pickle";

var raw = fs.readFileSync('etc/profile.json');
var profile = JSON.parse(raw);
var algo_list = profile["algo"];

function broadcast(cb) {
    algo_list.forEach(triger_cmd);
    cb();
}

function triger_cmd(algo) {
    py_cmd = 'python pascal/' + algo;
    console.log(py_cmd);
    shell.exec(py_cmd);
}

watch(file_stamp, broadcast)


