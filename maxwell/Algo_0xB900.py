"""
init code

"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import jqdatasdk as jq
import pickle
import json
from datetime import datetime, timedelta
import pytz
import time
import numpy as np
import pandas as pd
import pysnooper
import util.personal as personal
from util.util import haunter

LOG = haunter()

CACHE_PATH = os.path.join(BASE_DIR, "cache", "nightly")

# @pysnooper.snoop(os.path.join(BASE_DIR, "log","snoop.log"))
def launch():
    """

    """
    fund_df = jq.get_all_securities(types=['fund','open_fund'], date = datetime.now())
    # fund_df = jq.get_all_securities(types=['fund','open_fund'])
    portfolio_df = pd.DataFrame()
    for ticker in fund_df.index:
        print(ticker)
        code = ticker[:6]
        sub_df = jq.finance.run_query(jq.query(jq.finance.FUND_PORTFOLIO_STOCK).filter(jq.finance.FUND_PORTFOLIO_STOCK.code==code).limit(10))
        #   id    code   period_start  period_end    pub_date  report_type_id report_type  rank  symbol   name      shares    market_cap  proportion
        #   1   000001   2011-01-01    2011-06-30    2011-08-24  403005       半年度         1  600125   铁龙物流  36690953.0  3.867226e+08        3.6
    # proportion_df = portfolio_df[['period_end','rank','symbol','name','proportion']]
        portfolio_df = pd.concat([portfolio_df,sub_df],axis=0,sort=False)

    # save to fund_portfolio.pickle
    LOG.info("ticker_map dumps to file, fund_portfolio.pickle")
    with open(os.path.join(CACHE_PATH, 'fund_portfolio.pickle'), 'wb') as f:
        pickle.dump(portfolio_df, f)

    sub_portfolio = portfolio_df.reset_index()
    portfolio_dict = sub_portfolio.T.to_json(force_ascii=False)
    # save to code_mapping.json
    LOG.info("ticker_map dumps to file, fund_portfolio.json")
    with open(os.path.join(CACHE_PATH,'fund_portfolio.json'), 'w', encoding='utf-8') as f:
        json.dump(portfolio_dict, f, ensure_ascii=False)



if __name__ == '__main__':
    personal.login()
    launch()
