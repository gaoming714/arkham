"""

"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from celery import Celery

import pickle
import time
import pendulum
import requests
import util.util as util
from util.util import haunter

LOG = haunter("trade")
cache_jqd = os.path.join(BASE_DIR, "cache", "jqd")
cache_ticker = os.path.join(BASE_DIR, "cache", "ticker")
cache_runtime = os.path.join(BASE_DIR, "cache", "runtime")

app = Celery('trade',
            backend='redis://127.0.0.1',
            broker='redis://127.0.0.1',)
# warning: localhost works slow

"""
detail = {
                "ticker":None,
                "direction":None,
                "amount":None,
                "open_price":None,
                "open_time":None,
                "expect_price":None,
                "dump_price":None,
                "dump_time":None,
                }

}
"""


@app.task
def kick(ticker, detail=None):
    """ only kick, 
    """
    detail = detail or {}
    # check not conflict, opened_list does not contain ticker
    opened_list = show_STARTED()
    if opened_list.count(ticker) > 1:
        LOG.info(["stock conflict => ", ticker])
        return "stock conflict"

    # pre kick
    LOG.info(["pre kick => ", ticker])

    # wechat
    payload = ""
    if detail == {}:
        str_list = ["🍌 ", str(util.pretty_name(ticker)), "\n",
                    ]
    elif detail["direction"] == True:
        str_list = ["🍒买 ", str(util.pretty_name(detail["ticker"])), "\n",
                    "🍒买 ", format(detail["open_price"], '.3f'), " 🍌 ",
                    format(detail["amount"], '%<3d'), "\n",
                    "🔵 ", str(detail["open_time"]), "\n",
                    "🍍 ", format(detail["dump_price"], '.3f'), " ~ ",
                    format(detail["expect_price"], '.3f')]
    elif detail["direction"] == False:
        str_list = ["🍏卖 ", str(util.pretty_name(detail["ticker"])), "\n",
                    "🍏卖 ", format(detail["open_price"], '.3f'), " 🍌 ",
                    format(detail["amount"], '%<3d'), "\n",
                    "🔵 ", str(detail["open_time"]), "\n",
                    "🍍 ", format(detail["expect_price"], '.3f'), " ~ ",
                    format(detail["dump_price"], '.3f')]
    payload = payload.join(str_list)
    r = requests.get('http://127.0.0.1:9000/msg/' + payload)
    time.sleep(300)
    return 0

@app.task
def story(ticker, detail=None):
    """ only kick, 
    """
    detail = detail or {}
    # check not conflict, opened_list does not contain ticker
    opened_list = show_STARTED()
    if opened_list.count(ticker) > 1:
        LOG.info(["stock conflict => ", ticker])
        return "stock conflict"
    # pre kick
    LOG.info(["pre kick => ", ticker])
    # wechat
    payload = ""
    if detail == {}:
        str_list = ["🍌 ", str(util.pretty_name(ticker)), "\n",
                    ]
    elif detail["direction"] == True:
        str_list = ["🍒买 ", str(util.pretty_name(detail["ticker"])), "\n",
                    "🍒买 ", format(detail["open_price"], '.3f'), " 🍌 ",
                    format(detail["amount"], '%<3d'), "\n",
                    "🔵 ", str(detail["open_time"]), "\n",
                    "🍑🍑🍑🍑🍑🍑🍑🍑"]
    elif detail["direction"] == False:
        str_list = ["🍏卖 ", str(util.pretty_name(detail["ticker"])), "\n",
                    "🍏卖 ", format(detail["open_price"], '.3f'), " 🍌 ",
                    format(detail["amount"], '%<3d'), "\n",
                    "🔵 ", str(detail["open_time"]), "\n",
                    "🍑🍑🍑🍑🍑🍑🍑🍑"]
    payload = payload.join(str_list)
    r = requests.get('http://127.0.0.1:9000/msg/' + payload)
    time.sleep(6 * 60 * 60)
    return 0

@app.task
def test_trade(ticker, detail={}):
    print("test is on")
    time.sleep(200)
    print("test is off")

@app.task
def hold(ticker, detail={}):
    return

@app.task
def drop(ticker, detail={}):
    return


def show_STARTED():
    opened_ticker = list()
    if app.control.inspect().active() is None:
        return []
    active_list = app.control.inspect().active()['trade@TeX']
    for record in active_list:
        opened_ticker.append(record["args"][0])
    LOG.warning(opened_ticker)
    return opened_ticker

def check_price(ticker, detail):
    # load data
    # not second, need udpate
    with open(cache_runtime + ticker, 'rb') as f:
        df = pickle.load(f)
    comming = df["close"][-1]
    current_time = df.index[-1]
    if current_time >= detail["dump_time"]:
        return False
    if detail["direction"] == True:
        if comming > detail["dump_price"] and comming < detail["expect_price"]:
            return True
        else:
            return False
    elif detail["direction"] == False:
        if comming > detail["expect_price"] and comming < detail["dump_price"]:
            return True
        else:
            return False
    else:
        LOG.error("direction is not True or False")
        return



"""
from celery import Celery
app = Celery('trade',
            backend='redis://127.0.0.1',
            broker='redis://127.0.0.1',
            include=['script.trade'])

app.control.inspect().stats()
app.control.inspect().active_queues()
app.control.inspect().active()


from trade import kick

kick.delay("000001")
kick.delay("000031")
kick.delay("000031")

import pandas as pd

now = pd.Timestamp.now().ctime()

detail = {
                "ticker":"000001.XSHE",
                "direction":True,
                "amount":1230,
                "open_price":31.543,
                "open_time":now,
                "expect_price":35,
                "dump_price":29.109,
                "dump_time":now,
                }
ab = kick.delay("000001.XSHG",detail=detail)

{'trade@TeX': [{'id': '31abb256-c8f9-47fc-b343-3e1306281c88',
   'name': 'script.trade.kick',
   'args': ['000001.XSHE'],
   'kwargs': {},
   'type': 'script.trade.kick',
   'hostname': 'trade@TeX',
   'time_start': 1603189753.557798,
   'acknowledged': True,
   'delivery_info': {'exchange': '',
    'routing_key': 'celery',
    'priority': 0,
    'redelivered': None},
   'worker_pid': 1279245496560}]}



"""
