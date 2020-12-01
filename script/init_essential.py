"""
init essential

check cache dir
check cache stamp.pickle

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
import util.personal as personal
from util.util import haunter
from jsonschema import validate

LOG = haunter()

cache_path = os.path.join(BASE_DIR, "cache")
etc_path = os.path.join(BASE_DIR, "etc")
ajv_path = os.path.join(BASE_DIR, "test", "func", "jsonschema")



def check_algo_dispatcher():
    with open(os.path.join(etc_path, "Algo_active.json"), 'r') as f:
        data = json.load(f)
    schema = {  "description": "A product in the catalog",
                "type": "object",
                "properties": {
                    "data": {
                    "description": "The unique identifier for a product",
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    }
                },
                "required": [ "data" ]
    }
    validate(data, schema)

def check_ticker_dbs(tickers):
    if type(tickers) == type(""):
        ticker_list = [tickers]
    else:
        ticker_list = tickers
    # pickle
    with open(os.path.join(cache_path, "code_mapping.pickle"), 'rb') as f:
        dbs = pickle.load(f)
    for ticker in ticker_list:
        if ticker not in dbs.index:
            return False
    return True
    # json
    # with open(os.path.join(cache_path, "code_mapping.json"), 'r',encoding='utf-8') as f:
    #     dbs = pickle.load(f)
    # for ticker in ticker_list:
    #     if ticker not in dbs:
    #         return False
    # return True



check_algo_dispatcher()


if __name__ == '__main__':
    check_algo_dispatcher()
    print(check_ticker_dbs(["000001.XSHG","000003.XSHG"]))
    pass
