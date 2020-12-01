"""
algo for test
input None

output  detail   open_time, open_price, direction, expect_price, dump_price, dump_time
        None

"""
import json
import pickle
import datetime
import time
import os

import numpy as np
import pandas as pd

import board_push
from util.util import haunter

LOG = haunter()


cache_jqd = "./cache_jqd/"
cache_ticker = "./cache_ticker/"
cache_matrix = "./cache_matrix/"
cache_runtime = "./cache_runtime/"

EARLY = 4
SETUP = 7
INTER = 2


def end_nine(sub_df, ealier = 4, setup = 9, inter = 2):
    """
        0 1 2 3
        4 - 12
        return 1  => put down
        return -1 => wake up
    """
    arr = np.array(sub_df["close"])
    if len(arr) != ealier+setup: # 4+9
        return None
    direction = None
    for index, item in enumerate(arr):
        if index < ealier:
            continue
        elif index == ealier:
            direction = np.sign(item-arr[index-ealier])
        elif direction == np.sign(item-arr[index-ealier]):
            continue
        else:
            return None
    if direction == None:
        raise
    return direction

def algo_DeMark_lite(sub_df, ealier = 4, setup = 7, inter = 2):
    """
        DeMark Indicators are designed to anticipate turning points in the market.

        Tom DeMark created a strategy called a sequential that finds an overextended price move, 
        one that is likely to change direction and takes a countertrend position.

        To get a buy signal, the following three steps are applied to daily data:

        1) Setup.  There must be a  decline of at least nine or more consequtive closes that are 
        lower than the corresponding closes four days ealier.  If today’s close is equal to or 
        greater than the close four days before, the setup must begin again.

        2) Intersection.  To assure prices are declinging in an orderly fashion rather than 
        plunging, the high of any day on or after the eighth day of the set up must be greater 
        than the low of any day three or more days earlier.

        3) Countdown. Once setup and intersection have been satifiedm we count the number of days 
        in which we close lower than the close two days ago (doesn’t need to be continuous). 
        When the countdown reaches 13, we get a buy signal unless one of the following occurs:

        a. There is a close that exceeds the highest intraday high that occured during the setup stage.

        b.  A sell setup occurs (nine consequtive closes above the corresponding closes four days earlier).

        c.  Another buy setup occurs before the buy countdown is completed.

        Traders should expect that the development of the entire formation take no less than 21 days, 
        but more typically 24-39 days.

        Luckily there are many systems avaliable which do the counts for us.  Bloomberg is one such example.
    """
    # lite version is only 1 & 2, not apply step 3
    arr = np.array(sub_df["close"])
    if len(arr) != ealier+setup+inter: # 4+9
        return None
    direction = None
    for index, item in enumerate(arr):
        if index < ealier:
            continue
        elif index == ealier:
            direction = np.sign(item-arr[index-ealier])
        elif direction == 0:
            return None
        elif direction == np.sign(item-arr[index-ealier]):
            continue
        else:
            return None
    ## check 8 & 9
    if direction == -1: # up
        decling = sub_df["low"][sub_df["high"][-2]>sub_df["low"]].count()
        if decling < 3:
            decling = sub_df["low"][sub_df["high"][-1]>sub_df["low"]].count()
            if decling < 3:
                return None
    elif direction == 1: # down
        decling = sub_df["high"][sub_df["low"][-2]>sub_df["high"]].count()
        if decling < 3:
            decling = sub_df["high"][sub_df["low"][-1]>sub_df["high"]].count()
            if decling < 3:
                return None
    else:
        raise
    return direction


def launch():
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
    ticker_list = ["000001.XSHG"]
    ticker = ticker_list[0]

    # baseline
    baseline = "000001.XSHG"
    with open(cache_runtime + baseline, 'rb') as f:
        baseline_df = pickle.load(f)
    baseline_now = baseline_df.index[-1]

    # load data
    with open(cache_runtime + ticker, 'rb') as f:
        df = pickle.load(f)
    # open
    # LOG.debug(int(df["close"][2]*100) % 10)
    # LOG.info(int(df["close"][2]*100) % 10)
    # LOG.warning(int(df["close"][2]*100) % 10)

    # Algo
    sub_df = df[-(EARLY+SETUP+INTER):]
    # action = end_nine(sub_df)
    action = algo_DeMark_lite(sub_df)
    if action == None:
        return None
    elif action == -1: # up
        detail_dict = {}
        detail_dict["ticker"] = ticker
        detail_dict["open_price"] = sub_df["close"][-3:].mean() #tmp
        detail_dict["open_time"] = baseline_now
        detail_dict["direction"] = True
        detail_dict["expect_price"] = sub_df["close"][-7:-1].mean() #tmp
        detail_dict["dump_price"] = sub_df["close"][-1]-(sub_df["close"][-2]-sub_df["close"][-1])
        detail_dict["dump_time"] = baseline_now + datetime.timedelta(minutes=5)
    elif action == 1:
        detail_dict = {}
        detail_dict["ticker"] = ticker
        detail_dict["open_price"] = sub_df["close"][-3:].mean() #tmp
        detail_dict["open_time"] = baseline_now
        detail_dict["direction"] = False
        detail_dict["expect_price"] = sub_df["close"][-7:-1].mean() #tmp
        detail_dict["dump_price"] = sub_df["close"][-1]-(sub_df["close"][-2]-sub_df["close"][-1])
        detail_dict["dump_time"] = baseline_now + datetime.timedelta(minutes=5)
    else:
        raise
        return None
    # miss more series, so here is the only one
    detail_ss = pd.Series(detail_dict,name=detail_dict["ticker"])
    detail_df = detail_df.append(detail_ss, ignore_index=True)
    detail_json =  detail_df.T.to_json()
    print(detail_json)



detail = launch()
# if detail is not None:
#     print("aaa")
if detail is not None:
    board_push.launch(detail)




