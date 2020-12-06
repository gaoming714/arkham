"""
download data from jqdatasdk
need finance.pickle

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
from util.util import haunter

LOG = haunter("nightly_assess")

BASELINE = "000001.XSHG" # SZZS - 000001
PE_HS300 = None
CACHE_PATH = os.path.join(BASE_DIR,"cache")
CACHE_NIGHTLY = os.path.join(BASE_DIR,"cache","nightly")
# stamp_file = os.path.join(cache_runtime,"stamp.pickle")
ticker_list = [
    "601318.XSHG", # 中国平安
    # "601398.XSHG", # 工商银行
    # "601288.XSHG", # 农业银行
    "600036.XSHG", # 招商银行
    # "601988.XSHG", # 中国银行
    # "601166.XSHG", # 兴业银行
    # "600000.XSHG", # 浦发银行
    # "000001.XSHE", # 平安银行
    # "600016.XSHG", # 民生银行
    # "601328.XSHG", # 交通银行
    "002142.XSHE", # 宁波银行
    # "601998.XSHG", # 中信银行
    # "601818.XSHG", # 光大银行
    # "000333.XSHE", # 美的集团
    # "000651.XSHE", # 格力电器
    # "002032.XSHE", # 苏泊尔
    # "002508.XSHE", # 老板电器
    # "002242.XSHE", # 九阳股份
    # "603868.XSHG", # 飞科电器

    "603288.XSHG", # 海天味业
    "600298.XSHG", # 安琪酵母
    "600887.XSHG", # 伊利股份
    # "002714.XSHE", # 牧原股份
    "600519.XSHG", # 贵州茅台
    "000858.XSHE", # 五粮液
    "600809.XSHG", # 山西汾酒

    # "603160.XSHG", # 汇顶科技
    # "603501.XSHG", # 韦尔股份
    # "603986.XSHG", # 兆易创新
    "002916.XSHE", # 深南电路
    "002463.XSHE", # 沪电股份
    # "603228.XSHG", # 景旺电子
    # "002475.XSHE", # 立讯精密
    "300750.XSHE", # 宁德时代
    "300014.XSHE", # 亿纬锂能
    "002415.XSHE", # 海康威视
    # "002236.XSHE", # 大华股份
    # "601138.XSHG", # 工业富联

    "002352.XSHE", # 顺丰控股
    "002120.XSHE", # 韵达股份

    # "002174.XSHE", # 游族网络 x
    # "603444.XSHG", # 吉比特
    # "002555.XSHE", # 三七互娱
    # "002624.XSHE", # 完美世界 x
    # "002027.XSHE", # 分众传媒 x
    # "300033.XSHE", # 同花顺

    # "600801.XSHG", # 华新水泥
    # "600585.XSHG", # 海螺水泥
    "002271.XSHE", # 东方雨虹
    "600009.XSHG", # 上海机场
    # "601100.XSHG", # 恒立液压
    "600031.XSHG", # 三一重工

    # "002572.XSHE", # 索菲亚
    "603816.XSHG", # 顾家家居
    "603833.XSHG", # 欧派家居

    "600763.XSHG", # 通策医疗
    "600079.XSHG", # 人福医药
    "601799.XSHG", # 星宇股份
    "600048.XSHG", # 保利地产
    "300413.XSHE", # 芒果超媒
    "600660.XSHG", # 福耀玻璃

                ]
special_dict = {
    "601318.XSHG" : [None, 0], # 中国平安
    "601398.XSHG" : [None, 0], # 工商银行
    "601288.XSHG" : [None, 0], # 农业银行
    "600036.XSHG" : [None, 0], # 招商银行
    "601988.XSHG" : [None, 0], # 中国银行
    "601166.XSHG" : [None, 0], # 兴业银行
    "600000.XSHG" : [None, 0], # 浦发银行
    "000001.XSHE" : [None, 0], # 平安银行
    "600016.XSHG" : [None, 0], # 民生银行
    "601328.XSHG" : [None, 0], # 交通银行
    "002142.XSHE" : [None, 0], # 宁波银行
    "601998.XSHG" : [None, 0], # 中信银行
    "601818.XSHG" : [None, 0], # 光大银行
    "000333.XSHE" : [None, 0], # 美的集团
    "000651.XSHE" : [None, 0], # 格力电器
    # "002032.XSHE" : [None, 0], # 苏泊尔
    "002508.XSHE" : [None, 0], # 老板电器
    # "002242.XSHE" : [None, 0], # 九阳股份
    "603868.XSHG" : [None, 0], # 飞科电器
    "600519.XSHG" : [None, 20], # 贵州茅台
    "600048.XSHG" : [None, 0], # 保利地产




}

def get_baseline_PE():
    """
        get HS300 PE TTM as baseline
    """
    import script.nightly_HS300 as hs300
    global PE_HS300
    PE_HS300 = hs300.launch()

def core(name = None, pe = None, roe = None, inc = None):
    """

        <<< score
    """
    # assess_down & up
    if inc != 0:
        assess_down = roe * ((inc * 2.7 - roe) / 100 + 1)
        assess_up = roe * ((inc * 2.7 - roe) / 100 + 1) * ((inc * 2.7 - roe) / 100 + 1)
 
    else:
        assess_down = roe * ((inc * 2.7 - roe) / 100 + 1) * ((inc * 2.7 - roe) / 100 + 1) * 0.5 * 1.5
        assess_up = roe * ((inc * 2.7 - roe) / 100 + 1) * 0.5 * 1.5

    #  dynamic based on HS300 , PE = 13
    assess_down = assess_down * PE_HS300 / 13
    assess_up = assess_up * PE_HS300 / 13

    # risk   ----- s-1 -----assess_up------ s-2 ----
    fix_level = assess_up
    if pe >= fix_level:
        risk = - (pe - fix_level) * 2
    else:
        risk = - (fix_level - pe)

    #score
    assess_wave = (assess_up - assess_down) / assess_up * 100
    # risk = - (pe - assess_down * 0.4)
    score = roe * 2 + assess_wave * 1 + risk * 2
    # score = roe * 2 + assess_wave * 1 + risk
    return assess_down, assess_up, score

def launch():
    try:
        df = None
        with open(os.path.join(CACHE_NIGHTLY, "finance.pickle"), 'rb') as f:
            df = pickle.load(f)
    except:
        LOG.warning("Fail to load finance.pickle")
        return 1
    ## update special data
    for item in df.index:
        if item in special_dict:
            if special_dict[item][0] != None:
                df.at[item, 'roe'] = special_dict[item][0]
            if special_dict[item][1] != None:
                df.at[item, 'inc'] = special_dict[item][1]
    # make core finance_plus
    core_lambda = lambda row: core(row.name, row["pe_ratio"], row["roe"], row["inc"])
    ss = df.apply(core_lambda, axis=1)
    df[["assess_down","assess_up","score"]] = ss.apply(pd.Series)
    # save to data.pickle
    LOG.info("save finance_plus")
    with open(os.path.join(CACHE_NIGHTLY, "finance_plus.pickle"), 'wb') as f:
        pickle.dump(df, f)

def analysize():
    df = None
    with open(os.path.join(CACHE_NIGHTLY, "finance_plus.pickle"), 'rb') as f:
        df = pickle.load(f)
    with open(os.path.join(CACHE_PATH, "code_mapping.pickle"), 'rb') as f:
        mapping = pickle.load(f)

    sub_df = df.loc[ticker_list]
    sub_df = sub_df.sort_values(by='score',ascending=False)

    # add display name
    sub_df["display_name"] = mapping['display_name'][sub_df.index]

    LOG.info(sub_df)
    print(sub_df)




if __name__ == '__main__':
    get_baseline_PE()
    launch()
    analysize()