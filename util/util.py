import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import json
import pickle
from jsonschema import validate


cache_path = os.path.join(BASE_DIR, "cache")
etc_path = os.path.join(BASE_DIR, "etc")

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

def check_alive(tickers):
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

def pretty_name(tickers):
    if type(tickers) == type(""):
        ticker_list = [tickers]
    else:
        ticker_list = tickers
    # pickle
    with open(os.path.join(cache_path, "code_mapping.pickle"), 'rb') as f:
        dbs = pickle.load(f)
    if not (set(ticker_list) < set(dbs.index)):
        return tickers
    display_name_list = dbs["display_name"][ticker_list].to_list()
    code_list = dbs["code"][ticker_list].to_list()
    pretty_zip = zip(code_list,display_name_list)
    pretty_list = list(map(lambda x: " - ".join(x),pretty_zip))
    if type(tickers) == type(""):
        return pretty_list[0]
    else:
        return pretty_list

    # json
    # with open(os.path.join(cache_path, "code_mapping.json"), 'r',encoding='utf-8') as f:
    #     dbs = pickle.load(f)
    # for ticker in ticker_list:
    #     if ticker not in dbs:
    #         return False
    # return True

def renamesnow(ticker):
    material = ticker.split(".")
    if material[1] == "XSHA":
        output = "SH" + material[0]
    elif material[1] == "XSHE":
        output = "SZ" + material[0]
    else:
        output = ticker
    return output

#####################################################################
### logging by loguru
#######################################
from loguru import logger

LOG_DIR = os.path.join(BASE_DIR, "log")
DEFAULT_PATH = os.path.join(BASE_DIR, "log", "main.log")

def haunter(logname = None, debugpath=None):
    if debugpath != None:
        # for debug
        logger.add(debugpath)
        return logger
    logger.remove(handler_id=None)
    logger.add(sys.stderr, level="WARNING")
    logger.add(DEFAULT_PATH)
    if logname:
        if ".log" in logname:
            logpath = os.path.join(LOG_DIR, logname)
        else:
            logpath = os.path.join(LOG_DIR, logname+".log")
        logger.add(logpath)
    return logger
#####################################################################


if __name__ == '__main__':
    pass
