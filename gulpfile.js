const { watch, series, parallel } = require('gulp');
const shell = require('shelljs');
const signale = require('signale');
const chalk = require('chalk');

function check(cb) {
    var daemon_list = [
        'etc/start.sh',
        'etc/daemon.config.yml',
        'etc/daemon.download.sh',
        'etc/daemon.trade.sh',
        'etc/daemon.wechatflask.sh',
        'etc/start.sh'
    ]
    var status = shell.find(daemon_list);
    if (status.code !== 0) {
        throw new Error('Missing', status.stderr);
    }
    cb();
}

function main(cb) {
    shell.exec('pm2 start etc/daemon.config.yml',{silent:true});
    cb();
}

function prettymsg(cb) {
    signale.star('Enjoy Yourself!');
    signale.note('pm2 status => Show Status');
    cb();
}

function clean(cb) {
    shell.exec('pm2 delete all',{silent:true});
    cb();
}

exports.start = series(check, main, prettymsg)
exports.clean = series(clean)
