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
from util.util import renamesnow

import script.trade as trade


from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
options = Options()
options.add_argument('--headless')

LOG = haunter("Algo_0xA801")


CACHE_RUNTIME = os.path.join(BASE_DIR,"cache","runtime")
CACHE_NIGHTLY = os.path.join(BASE_DIR,"cache","nightly")

EDGE_UP = 5 * 0.001
EDGE_DONW = - 15 * 0.001

def atom(ticker):
    action = None


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
    # with open(os.path.join(CACHE_NIGHTLY, "fund_net_value.pickle"), 'rb') as f:
    #     net_df = pickle.load(f)

    # load data
    with open(os.path.join(CACHE_RUNTIME, ticker), 'rb') as f:
        df = pickle.load(f)

    # Algo
    snowticker = renamesnow(ticker)
    try:
        # print(snowticker)
        phase_pct = get_phase("SH510300")
        premium_pct = get_premium(snowticker)
        LOG.info(["phase_pct", phase_pct])
        # print(phase_pct)
        LOG.info(["premium_pct", premium_pct])
        print(phase_pct)
        print(premium_pct)
    except:
        return
    if premium_pct - phase_pct < EDGE_DONW:
        action = 1
    elif premium_pct - phase_pct > EDGE_UP:
        action = -1
    else:
        return
    print(action)
    if action == None:
        return None
    elif action == 1: # up
        detail_dict = {}
        detail_dict["ticker"] = ticker
        detail_dict["direction"] = True
        detail_dict["amount"] = 3500
        detail_dict["open_price"] = df["close"][-1:].mean() #tmp
        detail_dict["open_time"] = baseline_now
        detail_dict["expect_price"] = 0 #tmp
        detail_dict["dump_price"] = 0
        # detail_dict["dump_time"] = baseline_now + datetime.timedelta(minutes=5)
        detail_dict["dump_time"] = pendulum.parse(str(baseline_now),tz='Asia/Shanghai')
    elif action == -1:
        detail_dict = {}
        detail_dict["ticker"] = ticker
        detail_dict["direction"] = False
        detail_dict["amount"] = 3500
        detail_dict["open_price"] = df["close"][-1:].mean() #tmp
        detail_dict["open_time"] = baseline_now
        detail_dict["expect_price"] = 0 #tmp
        detail_dict["dump_price"] = 0
        # detail_dict["dump_time"] = baseline_now + datetime.timedelta(minutes=5)
        detail_dict["dump_time"] = pendulum.parse(str(baseline_now),tz='Asia/Shanghai')
    else:
        return None
    # return detail_dict
    # trade wechat
    LOG.info(["detail_dict", detail_dict])
    trade.story.delay(ticker, detail_dict)

def get_phase(ticker=None):
    with Firefox(options=options) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://xueqiu.com/S/SH510300")
        ans = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[5]/div/div[1]/div[2]")
        if ans:
            return float(ans.text.strip().split()[1].split("%")[0])/100
        else:
            LOG.critical("webdriver fail. check web -> xueqiu")
            return

def get_premium(ticker=None):
    with Firefox(options=options) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://xueqiu.com/S/" + ticker)
        ans = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[5]/table/tbody/tr[4]/td[2]/span")
        if ans:
            return float(ans.text.strip().split("%")[0])/100
        else:
            LOG.critical("webdriver fail. check web -> xueqiu")
            return




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
    # atom("161706.XSHE")
    launch()



