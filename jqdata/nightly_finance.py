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
from datetime import datetime, timedelta
import time
import pytz
import pandas as pd
import jqdata.jqauth as jqauth
from util.util import haunter

LOG = haunter("nightly_finance")

BASELINE = "000001.XSHG" # SZZS - 000001
CACHE_NIGHTLY = os.path.join(BASE_DIR,"cache","nightly")


def pull_finance():
    """
    """
    ### get ticker_list
    ticker_df = jq.get_all_securities(types=['stock'], date=None)
    ticker_list = ticker_df.index.to_list()
    ## download finance
    df_indicator = jq.get_fundamentals(jq.query(
            jq.indicator.roe,
            jq.indicator.inc_total_revenue_year_on_year,
            jq.indicator.code,
            jq.indicator.pubDate,
            jq.indicator.statDate
            ).filter(
                jq.valuation.code.in_(ticker_list)
            ), statDate='2019')
    df_valuation = jq.get_fundamentals(jq.query(
            jq.valuation.code,
            jq.valuation.day,
            jq.valuation.pe_ratio,
            jq.valuation.pe_ratio_lyr
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

if __name__ == '__main__':
    jqauth.login()
    pull_finance()

