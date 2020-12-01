"""
test util/log.py
"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

import pytest
import time
import pendulum


from util.util import haunter

@pytest.fixture()
def init_log(tmpdir):
    log_name = "test_log"
    log_file = os.path.join(tmpdir, "test_log.log")
    LOG = haunter(log_name,log_file)
    yield LOG, log_file


# for this project
def test_create_log_name_hard():
    log_name = "test_log"
    log_file = os.path.join(BASE_DIR, "log", "test_log.log")
    if os.path.exists(log_file):
        os.remove(log_file)
    LOG = haunter(log_name)
    assert os.path.exists(log_file)
    LOG.info("test content")
    #remove logfile
    LOG.remove(handler_id=None)
    # os.remove(log_file)

# for tmpdir
def test_create_log_name(tmpdir):
    log_name = "test_log"
    log_file = os.path.join(tmpdir, "test_log.log")
    LOG = haunter(log_name, log_file)
    assert os.path.exists(log_file)

def test_log_msg(init_log):
    LOG, log_file = init_log
    LOG.debug('debug message')
    LOG.info('info message')
    LOG.warning('warning message')
    LOG.error('error message')
    LOG.critical('critical message')
    with open(log_file, 'r', encoding='utf-8') as f:
        data = f.read()
    assert "debug message" in data
    assert "info message" in data
    assert "warning message" in data
    assert "error message" in data
    assert "critical message" in data
    assert "INFO" in data
    assert "DEBUG" in data
    assert "WARNING" in data
    assert "ERROR" in data
    assert "CRITICAL" in data
# @pytest.mark.skip("winpty cause timezone not working")
def test_log_timezone(init_log):
    LOG, log_file = init_log
    #create log & check time
    LOG.debug('debug message')
    utc_now = pendulum.now(tz='utc')
    local_now = pendulum.now("Asia/Shanghai")

    with open(log_file, 'r', encoding='utf-8') as f:
        data = f.read()
    utc_str = utc_now.ctime().split()[3]
    local_str = local_now.ctime().split()[3]
    # print(log_time_str)
    # print(data)
    assert utc_str not in data
    assert local_str in data

# @pytest.mark.skip("long time")
def test_log_time_walk(init_log):
    """longtime. test asctime can walk to next minute"""
    LOG, log_file = init_log
    for item in range(5):
        LOG.debug(["run ",item])
        now = pendulum.now("Asia/Shanghai")
        with open(log_file, 'r', encoding='utf-8') as f:
            data = f.read()
        log_time_str = now.ctime().split()[3]
        assert log_time_str in data

        time.sleep(20)

