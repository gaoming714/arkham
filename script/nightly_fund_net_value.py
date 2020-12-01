"""
download data from jqdatasdk
the launch should be in the morning
only for personal account.

"""
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import jqdatasdk as jq
import pickle
import pendulum
from datetime import datetime, timedelta
import time
import pytz
import pandas as pd
import util.personal as personal
from util.util import haunter

LOG = haunter("nightly_fund")

BASELINE = "000001.XSHG" # SZZS - 000001
CACHE_NIGHTLY = os.path.join(BASE_DIR,"cache","nightly")
# stamp_file = os.path.join(CACHE_PATH,"stamp.pickle")
# ticker_list = ["000905.XSHG","000333.XSHE","002032.XSHE","601990.XSHG","002415.XSHE"]
# ticker_list.append(BASELINE)

now = pendulum.now("Asia/Shanghai")
dawn = pendulum.today("Asia/Shanghai")

def pull_fund_net_value():
    """
    """
    ### get ticker_list
    # ticker_df = jq.get_all_securities(types=['fund'], date=None)
    # ticker_list = ticker_df.index.to_list()
    ticker_list = ["161706.XSHE","510300.XSHG"]
    baseline_df = jq.get_price(BASELINE, end_date = dawn, count = 2, frequency='daily')
    print(type(baseline_df.index[-1]))
    print(type(dawn.to_datetime_string()))
    print(str(baseline_df.index[-1]) == dawn.to_datetime_string())
    print(baseline_df)
    if str(baseline_df.index[-1]) == dawn.to_datetime_string():
        previous_date = baseline_df.index[0]
    else:
        previous_date = baseline_df.index[-1]
    netvalue_df = jq.get_extras('unit_net_value', ticker_list, end_date=previous_date, df=True, count=1)
    netvalue_se = netvalue_df.iloc[0]
    netvalue_se.name = "netvalue"
    # ticker_all_df = jq.get_all_securities(types=['stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof',], date=None)

    preclose_df = jq.get_price(ticker_list, end_date = previous_date, count = 1, frequency='daily')
    preclose_df = preclose_df.set_index(["code"])
    preclose_df = preclose_df.sort_index()
    preclose_se = preclose_df["close"]
    preclose_se.name = "preclose"
    df = pd.concat([netvalue_se, preclose_se], axis=1)
    print(df)
    # df = pd.merge(df_indicator,df_valuation,on='code')
    # df = df.rename(columns={"inc_total_revenue_year_on_year":"inc"})
    # df = df.dropna()
    # df = df.set_index(['code'])
    # df = df.sort_index()
    LOG.info("download finance data ===================")
    LOG.info(df)
    print(df)

    # save to data.pickle
    LOG.info("Download Data to fund_net_value.pickle")
    with open(os.path.join(CACHE_NIGHTLY, "fund_net_value.pickle"), 'wb') as f:
        pickle.dump(df, f)

if __name__ == '__main__':
    personal.login()
    pull_fund_net_value()

