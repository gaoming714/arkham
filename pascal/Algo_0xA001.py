"""
algo for test
input None

output  detail   open_time, open_price, direction, expect_price, dump_price, dump_time
        None

"""

import pickle
import datetime
import time
import os
import board_push
from util.util import haunter

LOG = haunter()


cache_jqd = "./cache_jqd/"
cache_ticker = "./cache_ticker/"
cache_matrix = "./cache_matrix/"
cache_runtime = "./cache_runtime/"
def launch():
    flag = None
    detail = {"open_price":None,
                "open_time":None,
                "direction":None,
                "expect_price":None,
                "dump_price":None,
                "dump_time":None,}
    # init
    ticker_list = ['510050.XSHG', '510500.XSHG', '510300.XSHG', '601318.XSHG']
    ticker = ticker_list[0]

    # load data
    with open(cache_runtime + ticker, 'rb') as f:
        df = pickle.load(f)
    # open
    LOG.debug(int(df["close"][2]*100) % 10)
    LOG.info(int(df["close"][2]*100) % 10)
    LOG.warning(int(df["close"][2]*100) % 10)
    if int(df["close"][2]*100) % 10 == 4:
        flag = True
        detail["ticker"] = ticker
        detail["open_price"] = df["close"][0]
        detail["open_time"] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        detail["direction"] = True
        detail["expect_price"] = df["close"][0]*1.01
        detail["dump_price"] = df["close"][0]*0.09
        detail["dump_time"] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)+datetime.timedelta(minutes=5)

    # output TEMP
    if flag == True:
        print("==========================")
        print("SMG ticker\t\t", detail["ticker"])
        print("SMG open_price\t\t", detail["open_price"])
        print("SMG open_time\t\t", detail["open_time"])
        print("SMG direction\t", detail["direction"])
        print("SMG expect_price\t",detail["expect_price"])
        print("SMG dump_price\t\t", detail["dump_price"])
        print("SMG dump_time\t\t", detail["dump_time"])
        print("==========================\n")
        return detail


detail = launch()
# if detail is not None:
#     print("aaa")
if detail is not None:
    board_push.launch(detail)




