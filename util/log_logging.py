import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = os.path.dirname(os.getcwd()) # for jupyter
sys.path.append(BASE_DIR)

from datetime import datetime, timedelta
import time
import pytz
import logging

DEFAULT_LOGFILE = os.path.join(BASE_DIR, "log", "main.log")

def haunter(logname = __file__, logfile = DEFAULT_LOGFILE, loglevel = logging.DEBUG):
    """
    """
    # create logger
    logger = logging.getLogger(logname)
    logger.setLevel(loglevel)

    # set gmtime for UTC or lambda for localtime
    # gmtime
    # logging.Formatter.converter = time.gmtime
    # localtime
    tz = pytz.timezone("Asia/Shanghai")
    # localtime = tz.normalize(datetime.now(pytz.utc).astimezone(tz))
    localtime_lambda = lambda *foo: tz.normalize(datetime.now(pytz.utc).astimezone(tz)).timetuple()
    logging.Formatter.converter = localtime_lambda

    # set FileHandler & StreamHandler
    fh = logging.FileHandler(logfile, mode='a', encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # set Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add Handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


if __name__ == '__main__':
    LOG = haunter()
    LOG.debug('debug message')
    LOG.info('info message')
    LOG.warning('warning message')
    LOG.error('error message')
    LOG.critical('critical message')
