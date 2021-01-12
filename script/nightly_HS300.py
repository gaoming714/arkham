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
from datetime import datetime
import time
import pytz
import pysnooper
from util.util import haunter

LOG = haunter("nightly_HD300")

CACHE_PATH = os.path.join(BASE_DIR, "cache")

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support import expected_conditions as expected
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


def launch():
    """

    """
    #This example requires Selenium WebDriver 3.13 or newer
    options = Options()
    options.add_argument('--headless')
    with Firefox(options=options) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://eniu.com/gu/sz399300")
        ans = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[1]/div/div[1]/div/div[2]/div/p[1]/a")
        if ans:
            pe = float(ans.text)
        else:
            pe = 0
            LOG.critical("webdriver fail. check web -> eniu.com")

    # save to file
    LOG.info("ticker_map dumps to file, PE_HS300.pickle")
    with open(os.path.join(CACHE_PATH, 'nightly', 'PE_HS300.pickle'), 'wb') as f:
        pickle.dump({"HS300":pe}, f)

    return pe

if __name__ == '__main__':
    launch()
