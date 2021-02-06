# arkham

> Stock runtime system, which can find a time to kick Your Ass

![Snap](/zip/screenshot.png)

## 1 Material Collection

### 1.1 python

I use poetry to build the python environment.
File `activate` on /rootpath/ is the link file to poetry/python.
So, you should make "source acrivate" enter python env.

e.g.

    $ sources activate
    (.venv) -> $

you can use any way to enable python.

Packages are in pyproject.toml

### 1.2 nodejs

global packages: pm2 gulp

install these packages in global.

### 1.3 jqdatasdk account

register an account on jqdatasdk on website.

fill username & password to `profile.json`

support: https://www.joinquant.com/default/index/sdk#jq-sdk-apply

### 1.4 Redis

make sure redis-server is running.

(in the future, redis will be DB, current it is a check item)

## 2 install packages

run these command to install packages.

    poetry install
    npm install

(it will be ok if you enable packages working.)

## 3 create etcfiles

copy etc/example/\* to etc/

edit the these as the template.

    launch is file `daemon.condig.yml`

    middleware is the files ending with `.sh`

    config files ending with `.json`

## 4 start

    gulp start

server can run if no error

    pm2 status

open http://127.0.0.1:6600 to login with wechat.( Archived , which can send msg to wechat)

open http://127.0.0.1:6602 to show APP web page.
(try to send msg on website. http://127.0.0.1:6602/msg/testing )
