"""
algo for test
input None

output  detail   open_time, open_price, direction, expect_price, dump_price, dump_time
        None

"""
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


import json
import pickle
import time
import pendulum

import numpy as np
import pandas as pd

import requests
from util.util import haunter

import script.trade as trade

LOG = haunter("Algo_0xA800")


CACHE_RUNTIME = os.path.join(BASE_DIR,"cache","runtime")
CACHE_NIGHTLY = os.path.join(BASE_DIR,"cache","nightly")

EDGE_UP = 5 * 0.001
EDGE_DONW = -5 * 0.001

def algo_banker(price = None, net_value = None, baseline = None, pre_baseline = None):
    """
        calculate the base_net_value + HS300 <> current_price
    """
    LOG.info([price , net_value , baseline , pre_baseline])
    if price == None or net_value == None or baseline == None or pre_baseline == None:
        # log.error("algo_banker not work on args")
        return
    market_pct = (baseline - pre_baseline)/pre_baseline
    ticker_pct = (price - net_value)/net_value
    space = ticker_pct - market_pct
    if space > EDGE_UP:
        return -1
    elif space < EDGE_DONW:
        return 1
    else:
        return

def atom(ticker):
    action = None
    # detail_dict
    # detail = {  "ticker":None,
    #             "open_price":None,
    #             "open_time":None,
    #             "direction":None,
    #             "expect_price":None,
    #             "dump_price":None,
    #             "dump_time":None,
    #             }

    # detail DataFrame
    detail_df = pd.DataFrame(columns=[
        "ticker",
        "open_time", "open_price",
        "direction", "expect_price",
        "dump_price", "dump_time"])

    # init
    # ticker_list = ["000001.XSHG"]
    # ticker = ticker_list[0]

    # baseline
    baseline = "000001.XSHG"
    with open(os.path.join(CACHE_RUNTIME ,baseline), 'rb') as f:
        baseline_df = pickle.load(f)
    baseline_now = baseline_df.index[-1]

    # load pre data
    with open(os.path.join(CACHE_NIGHTLY, "fund_net_value.pickle"), 'rb') as f:
        net_df = pickle.load(f)

    # load data
    with open(os.path.join(CACHE_RUNTIME, ticker), 'rb') as f:
        df = pickle.load(f)
    with open(os.path.join(CACHE_RUNTIME, "510300.XSHG"), 'rb') as f:
        IF300_df = pickle.load(f)
    LOG.info(net_df)
    LOG.info(df)
    LOG.info(IF300_df)
    # Algo
    # action = end_nine(sub_df)
    price = df["close"][-1]
    net_value = net_df["netvalue"][ticker]
    baseline = IF300_df["close"][-1]
    pre_baseline = net_df["preclose"][-1]
    action = algo_banker(price = price, net_value = net_value, baseline = baseline, pre_baseline = pre_baseline)
    if action == None:
        return None
    elif action == 1: # up
        detail_dict = {}
        detail_dict["ticker"] = ticker
        detail_dict["direction"] = True
        detail_dict["amount"] = 0
        detail_dict["open_price"] = df["close"][-3:].mean() #tmp
        detail_dict["open_time"] = baseline_now
        detail_dict["expect_price"] = df["close"][-7:-3].mean() #tmp
        detail_dict["dump_price"] = df["close"][-1]-(df["close"][-2]-df["close"][-1])
        # detail_dict["dump_time"] = baseline_now + datetime.timedelta(minutes=5)
        detail_dict["dump_time"] = pendulum.parse(str(baseline_now),tz='Asia/Shanghai')
    elif action == -1:
        detail_dict = {}
        detail_dict["ticker"] = ticker
        detail_dict["direction"] = False
        detail_dict["amount"] = 0
        detail_dict["open_price"] = df["close"][-3:].mean() #tmp
        detail_dict["open_time"] = baseline_now
        detail_dict["expect_price"] = df["close"][-7:-3].mean() #tmp
        detail_dict["dump_price"] = df["close"][-1]-(df["close"][-2]-df["close"][-1])
        # detail_dict["dump_time"] = baseline_now + datetime.timedelta(minutes=5)
        detail_dict["dump_time"] = pendulum.parse(str(baseline_now),tz='Asia/Shanghai')
    else:
        return None
    # miss more series, so here is the only one
    detail_ss = pd.Series(detail_dict,name=detail_dict["ticker"])
    detail_df = detail_df.append(detail_ss, ignore_index=True)
    detail_json =  detail_df.T.to_json()
    LOG.info(detail_json)
    # return detail_dict
    # trade wechat
    trade.kick.delay(ticker, detail_dict)
    # auto flask wechat
    # if action == -1:
    #     payload = ""
    #     str_list = ["🍒 ", str(   detail_dict["ticker"]),    "\n",
    #                 "🍒 ", format(detail_dict["open_price"],'.3f')," 🍌0\n",
    #                 "🔵 ", str(   detail_dict["open_time"]), "\n",
    #                 "🌽 ", format(detail_dict["expect_price"],'.3f')]
    #     payload = payload.join(str_list)
    #     r = requests.get('http://127.0.0.1:9000/msg/' + payload)
    # elif action == 1:
    #     payload = ""
    #     str_list = ["🍏 ", str(   detail_dict["ticker"]),    "\n",
    #                 "🍏 ", format(detail_dict["open_price"],'.3f')," 🍌0\n",
    #                 "🔵 ", str(   detail_dict["open_time"]), "\n",
    #                 "🌽 ", format(detail_dict["expect_price"],'.3f')]
    #     payload = payload.join(str_list)
    #     r = requests.get('http://127.0.0.1:9000/msg/' + payload)

def launch():
    # now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    # mk_alpha = datetime.datetime(now.year,now.month,now.day,9,40,0)
    # mk_beta = datetime.datetime(now.year,now.month,now.day,14,50,0)
    now = pendulum.now("Asia/Shanghai")
    dawn = pendulum.today("Asia/Shanghai")
    mk_alpha = dawn.add(hours=9,minutes=35)
    mk_beta = dawn.add(hours=14,minutes=50)
    if now < mk_alpha:
        return
    elif now > mk_beta:
        return
    # init ticker_list
    ticker_list = ["161706.XSHE"]
    for ticker in ticker_list:
        atom(ticker)
        # if detail != None and detail != {}:
        #    trade.kick.delay(ticker, detail)
    # load JSON
    # with open('../etc/Algo_0xA902.json', 'r') as f:
    #     data = json.load(f)
    # ticker_list = data

if __name__ == '__main__':
    launch()



