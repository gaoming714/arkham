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
import time
import pytz
import pysnooper
import util.personal as personal
from util.util import haunter

LOG = haunter()

CACHE_PATH = os.path.join(BASE_DIR, "cache")

# @pysnooper.snoop(os.path.join(BASE_DIR, "log","snoop.log"))
def launch():
    """

    """
    ticker_df = jq.get_all_securities(types=['stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof',], date=None)
    ticker_df['ticker'] = ticker_df.index
    ticker_df['code'] = ticker_df['ticker'].apply(lambda x:x[:6])

    order =  ['display_name', 'name', 'type', 'ticker', 'code']
    ticker_df = ticker_df[order]
    ticker_dict = ticker_df.T.to_dict()

    # save to code_mapping.pickle
    LOG.info("ticker_map dumps to file, code_mapping.pickle")
    with open(os.path.join(CACHE_PATH,'code_mapping.pickle'), 'wb') as f:
        pickle.dump(ticker_df, f)

    # save to code_mapping.json
    LOG.info("ticker_map dumps to file, code_mapping.json")
    with open(os.path.join(CACHE_PATH,'code_mapping.json'), 'w', encoding='utf-8') as f:
        json.dump(ticker_dict, f, ensure_ascii=False)



if __name__ == '__main__':
    personal.login()
    launch()
