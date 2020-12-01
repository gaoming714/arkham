"""
test util/log.py
"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

import time
import pendulum

import pytest
import script.trade as trade
from celery import Celery

app = Celery('trade',
        backend='redis://127.0.0.1',
        broker='redis://127.0.0.1',)

@pytest.fixture()
def init_env():
    os.system("pm2 reload Trade")
    time.sleep(5)
    os.system("pm2 reload Flower")
    time.sleep(3)
    yield
    # pm2 delete all


# test celery work
def test_trade_basic(init_env):
    assert app.control.inspect().active()['trade@TeX'] == []
    trade.kick.delay("test_ticker")
    time.sleep(5)
    assert app.control.inspect().active()['trade@TeX'] != []


def test_trade_sleep(init_env):
    assert app.control.inspect().active()['trade@TeX'] == []
    trade.kick.delay("test_abc")
    time.sleep(19)
    assert app.control.inspect().active()['trade@TeX'] != []
    time.sleep(250)
    assert app.control.inspect().active()['trade@TeX'] != []
    time.sleep(50)
    assert app.control.inspect().active()['trade@TeX'] == []




