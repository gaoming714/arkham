"""
init code

"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

import pytest
import logging
from util.util import haunter

def test_haunter_name(tmpdir):
    log_file = os.path.join(tmpdir, "test_log.log")
    log_name = "log_name"
    LOG = haunter(log_name, logfile = log_file, loglevel=logging.DEBUG)
    LOG.debug('MSG')
    assert os.path.exists(log_file)
    with open(log_file, 'r', encoding='utf-8') as f:
        data = f.read()
    assert "MSG" in data

def test_haunter_level(tmpdir):
    log_file = os.path.join(tmpdir, "test_log.log")
    log_name = "HAUNTER"
    LOG = haunter(log_name, logfile = log_file, loglevel=logging.INFO)
    LOG.debug('MSG')
    assert os.path.exists(log_file)
    with open(log_file, 'r', encoding='utf-8') as f:
        data = f.read()
    assert "MSG" not in data
