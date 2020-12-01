import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = os.path.dirname(os.getcwd()) # for jupyter
sys.path.append(BASE_DIR)

from loguru import logger

LOG_DIR = os.path.join(BASE_DIR, "log")
DEFAULT_PATH = os.path.join(BASE_DIR, "log", "main.log")


def haunter(logpath = None):

    logger.remove(handler_id=None)
    logger.add(sys.stderr, level="WARNING")
    logger.add(DEFAULT_PATH)
    if logpath:
        if "." in logpath:
            logpath = os.path.join(LOG_DIR, logpath)
        else:
            logpath = os.path.join(LOG_DIR, logpath+".log")
        logger.add(logpath)
    return logger