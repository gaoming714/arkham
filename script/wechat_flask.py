"""
🍒 buy
🍏 sell

🔵 open
🔷 close
🍋
🍌 amount
🍍
"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import json
import pendulum
# import numpy as np
# import pandas as pd

## wechat profile
WECHAT_LIST = os.path.join(BASE_DIR,"etc","wechat.json")
wechat_list = None
with open(WECHAT_LIST, 'r', encoding='utf-8') as f:
    wechat_list = json.load(f)

user_list = wechat_list["user_list"]
chatroom_list = wechat_list["chatroom_list"]

## flask
from flask import Flask, request, jsonify
from markupsafe import escape

import itchat

app = Flask(__name__)

def login_wechat_auto():
    # itchat.auto_login(enableCmdQR=2)
    # itchat.auto_login(hotReload=True)
    itchat.auto_login()
    payload = ""
    str_list = ["🍒 => 买  Buy ", "\n",
                "🍏 => 卖  Sell", "\n",
                "🍌 => 量  amount", "\n",
                "🔵 => 开  open", "\n",
                "🔷 => 平  close", "\n",
                "🍍 => 阈  area", "\n",
                (pendulum.now("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")
                ]
    payload = payload.join(str_list)
    itchat.send(payload, toUserName='filehelper')
    for user in user_list:
        name = itchat.search_friends(name=user)
        if name == []:
            continue
        itchat.send(payload, toUserName=name[0]["UserName"])
    for user in chatroom_list:
        name = itchat.search_chatrooms(name=user)
        if name == []:
            continue
        itchat.send(payload, toUserName=name[0]["UserName"])

@app.route('/login',methods=['GET','POST'])
def login_wechat():
    itchat.auto_login()
    payload = ""
    str_list = ["🍒 => 买  Buy ", "\n",
                "🍏 => 卖  Sell", "\n",
                "🍌 => 量  amount", "\n",
                "🔵 => 开  open", "\n",
                "🔷 => 平  close", "\n",
                "🍍 => 阈  area", "\n",
                (pendulum.now("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")
                ]
    payload = payload.join(str_list)
    itchat.send(payload, toUserName='filehelper')

@app.route('/msg/<msg>',methods=['GET','POST'])
def send_message(msg):
    # print('请求方式为------->', request.method)
    # args = request.args.get("msg") or "args没有参数"
    # print('args参数是------->', args)
    # form = request.form.get('name') or 'form 没有参数'
    # print('form参数是------->', form)

    itchat.send(msg, toUserName='filehelper')
    for user in user_list:
        name = itchat.search_friends(name=user)
        itchat.send(msg, toUserName=name[0]["UserName"])
    for user in chatroom_list:
        name = itchat.search_chatrooms(name=user)
        itchat.send(msg, toUserName=name[0]["UserName"])
    # return jsonify(args=args, form=form)
    return jsonify(msg=msg)

if __name__ == '__main__':
    # login_wechat()
    app.run(port=9000)