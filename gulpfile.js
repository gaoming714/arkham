const { watch, series, parallel } = require('gulp');
const shell = require('shelljs');

function start(cb) {
    shell.exec('bash etc/start.sh',{silent:true});
    cb();
}

function clean(cb) {
    shell.exec('pm2 delete all',{silent:true});
    cb();
}

exports.start = start;
exports.clean = clean;
