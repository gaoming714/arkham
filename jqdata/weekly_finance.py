"""
download data from jqdatasdk
the launch should be in the morning
only for personal account.

update on Saturday 7:00

"""
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import jqdatasdk as jq
import pickle
from datetime import datetime, timedelta
import time
import pytz
import pandas as pd
import pendulum
import jqdata.jqauth as jqauth
from util.util import haunter

LOG = haunter("nightly_finance")

BASELINE = "000001.XSHG" # SZZS - 000001
CACHE_NIGHTLY = os.path.join(BASE_DIR,"cache","nightly")


def pull_finance():
    """
    """
    clock = pendulum.now("Asia/Shanghai")
    if clock.month < 5:
        finance_year = clock.year - 2
    else:
        finance_year = clock.year - 1

    ### get ticker_list
    ticker_df = jq.get_all_securities(types=['stock'], date=None)
    ticker_list = ticker_df.index.tolist()
    ## download finance
    df_indicator = jq.get_fundamentals(jq.query(
            jq.indicator.roe,
            jq.indicator.inc_total_revenue_year_on_year,
            jq.indicator.code,
            jq.indicator.pubDate,
            jq.indicator.statDate
            ).filter(
                jq.valuation.code.in_(ticker_list)
            ), statDate=finance_year)
    df_valuation = jq.get_fundamentals(jq.query(
            jq.valuation.code,
            jq.valuation.day,
            jq.valuation.pe_ratio,
            jq.valuation.pe_ratio_lyr,
            jq.valuation.market_cap,
            jq.valuation.circulating_cap,
            jq.valuation.circulating_market_cap
            ).filter(
                jq.valuation.code.in_(ticker_list)
            ), date=None)
    df = pd.merge(df_indicator,df_valuation,on='code')
    df = df.rename(columns={"inc_total_revenue_year_on_year":"inc"})
    df = df.dropna()
    df = df.set_index(['code'])
    df = df.sort_index()
    LOG.info("download finance data ===================")
    LOG.info(df)

    # save to data.pickle
    LOG.info("Download Data to finance.pickle")
    with open(os.path.join(CACHE_NIGHTLY, "finance.pickle"), 'wb') as f:
        pickle.dump(df, f)
def pull_ticker():
    index_list = [  "000300.XSHG",
                    "000688.XSHG",
                    "399300.XSHE",
    ]
    weight_dict = {}
    for index_item in index_list:
        # ticker_list = jq.get_index_stocks(index_item)
        # print(ticker_list)
        weight_df = jq.get_index_weights(index_item)
        # print(weight_df.index.tolist())
        # print(weight_df)
        #                    date  weight display_name
        # code
        # 000001.XSHE  2020-12-31   0.957         平安银行
        # 000002.XSHE  2020-12-31   0.996          万科A
        weight_dict[index_item] = weight_df
    # save to data.pickle
    LOG.info("Download Data to weights.pickle")
    with open(os.path.join(CACHE_NIGHTLY, "weights.pickle"), 'wb') as f:
        pickle.dump(weight_dict, f)



def hold_period():
    """
        update on 15:20
    """

    now = pendulum.now("Asia/Shanghai")
    dawn = pendulum.today("Asia/Shanghai")
    mk_epsilon = dawn.add(hours=7,minutes=0)
    mk_zeta = pendulum.tomorrow("Asia/Shanghai")
    flag = False
    # refresh remain per half-hour
    if now < mk_epsilon and now.day_of_week == 6:
        LOG.info(["remain (s) ",(mk_epsilon - now).total_seconds()])
        time.sleep((mk_epsilon - now).total_seconds())
        pull_finance()
    else:
        LOG.info(["remain to tomorrow (s) ",(mk_zeta - now).total_seconds()])
        time.sleep((mk_zeta - now).total_seconds())
if __name__ == '__main__':
    jqauth.login()
    pull_finance()
    pull_ticker()
    # while True:
    #     hold_period()


