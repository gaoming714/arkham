"""
download data from jqdatasdk
download from 9:00-11.30  13:00-15:00
download only happends @ 0 second
not unlimited for personal account.

"""
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import jqdatasdk as jq
import pickle
import time
import json
import pendulum
import jqdata.jqauth as jqauth
from util.util import haunter

LOG = haunter("download")

BASELINE = "000001.XSHG" # SZZS - 000001
CACHE_RUNTIME = os.path.join(BASE_DIR,"cache","runtime")
STAMP_PATH = os.path.join(CACHE_RUNTIME,"stamp.pickle")
PROFILE = os.path.join(BASE_DIR,"etc","profile.json")
data = None
with open(PROFILE, 'r', encoding='utf-8') as f:
    data = json.load(f)
ticker_list = data["download"]
ticker_list.append(BASELINE)

now = pendulum.now("Asia/Shanghai")
dawn = pendulum.today("Asia/Shanghai")
mk_mu = dawn.add(hours=9,minutes=20)
mk_nu = dawn.add(hours=9,minutes=25)
mk_alpha = dawn.add(hours=9,minutes=30)
mk_beta = dawn.add(hours=11,minutes=30)
mk_gamma = dawn.add(hours=13,minutes=0)
mk_delta = dawn.add(hours=15,minutes=0)
mk_zeta = pendulum.tomorrow("Asia/Shanghai")


def hold_period():
    """
        mu nu  9:30  alpha beta  12  gamma  delta  15 zeta
    """
    while True:
        now = pendulum.now("Asia/Shanghai")
        # refresh remain per half-hour
        if now.minute % 30 == 0:
            LOG.info(("JQData Remains => ",jqauth.jq_remains()))
        if now < mk_alpha:
            LOG.info(["remain (s) ",(mk_alpha - now).total_seconds()])
            time.sleep((mk_alpha - now).total_seconds())
        elif now <= mk_beta:
            return
        elif now < mk_gamma:
            LOG.info(["remain (s) ",(mk_gamma - now).total_seconds()])
            time.sleep((mk_gamma - now).total_seconds())
        elif now <= mk_delta:
            return
        else:
            LOG.info("Market Closed")
            LOG.warning(["remain to end (s) ",(mk_zeta - now).total_seconds()])
            time.sleep((mk_zeta - now).total_seconds())
            # for holiday, tmp, dawn does work for it.
            while pendulum.now("Asia/Shanghai").date() not in jq.get_all_trade_days():
                time.sleep(86400)
            # update dawn, need exit.
            LOG.info("update to tomorrow")
            exit(0)

def fetch_baseline():
    # download baseline
    now = pendulum.now("Asia/Shanghai")
    stamp_df = jq.get_price(BASELINE, end_date = now, count = 1, frequency='minute')
    stamp_cloud = stamp_df.index[-1]

    # check baseline stamp, cteate if no file.
    try:
        with open(STAMP_PATH, 'rb') as f:
            stamp_local = pickle.load(f)
    except:
        LOG.warning("stamp_local is None, return stamp_cloud")
        return stamp_cloud
    LOG.info(["stamp < local cloud > ", stamp_local, stamp_cloud])
    LOG.info(['stamp same', stamp_local == stamp_cloud])
    while stamp_cloud == stamp_local: # new data for baseline
        # download baseline
        time.sleep(0.27) # for test
        reload_now = pendulum.now("Asia/Shanghai")
        LOG.info(["Reload baseline ", reload_now])
        stamp_df = jq.get_price(BASELINE, end_date = reload_now, count = 1, frequency='minute')
        stamp_cloud = stamp_df.index[-1]
        if reload_now > now.add(seconds=90):
            LOG.warning("reload more than 90s")
        if reload_now > now.add(seconds=180):
            LOG.error("fail to reload too many times")
            return
    return stamp_cloud

def pull_all(stamp=None):
    if stamp == None:
        return
    now = pendulum.now("Asia/Shanghai")
    for ticker in ticker_list:
        data= jq.get_price(ticker,
                # start_date=datetime(2019,5, 7,  9, 0, 0),
                count = 120,
                end_date=now,
                fields = ['open', 'close', 'high', 'low', 'volume',
                        'money', 'avg', 'high_limit', 'low_limit',
                        'pre_close', 'paused', 'factor', 'price',
                        'open_interest'],
                frequency='minute')
        with open(os.path.join(CACHE_RUNTIME, ticker), 'wb') as f:
            pickle.dump(data, f)
    # save stamp.pickle
    LOG.debug("save stamp.pickle, pull_all finish")
    with open(STAMP_PATH, 'wb') as f:
        pickle.dump(stamp, f)

if __name__ == '__main__':
    jqauth.login()
    while True:
        hold_period()
        stamp = fetch_baseline()
        pull_all(stamp)

        # LOG.info(("JQData Remains => ",personal.jq_remains()))

        now = pendulum.now("Asia/Shanghai")
        LOG.info(("Next fetch (s)=> ", 59-now.second))
        LOG.debug(("local time => ", now))
        LOG.debug(("stamp time => ", stamp))
        time.sleep(59-now.second)
