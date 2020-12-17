# arkham

> Stock runtime system, which can find a time to kick Your Ass

![Snap](/zip/screenshot.png)

## 1 Material Collection

### 1.1 python

I use poetry to build the python environment.
activate is the link file to poetry/python.
so , you should make "source acrivate" can enter python env.

e.g.

    $ sources activate
    (.venv) ->

you can use any to run python if you install the packages

then the edit the start.sh

### 1.2 nodejs

global packages: pm2 gulp

install there packages in global.

### 1.3 jqdatasdk account

register an account on jqdatasdk on website.

support: joinquant.com

### 1.4 Redis

make sure redis-server is running.

## 2 install packages

run these command to install packages.

    poetry install
    npm install

## 3 create etcfiles

copy etc/example/\* to etc/

edit the these as the template.

especially the profile.json

## 4 start

    gulp start

server can run if no error

    pm2 status can check

open http://127.0.0.1:6600 to login with wechat.

open http://127.0.0.1:6602 to show APP web page.
