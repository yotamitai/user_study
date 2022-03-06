import logging
import sys
from os import unlink
from os.path import exists, abspath

APP_LOGGER_NAME = 'MainLogger'

def setup_applevel_logger(logger_name=APP_LOGGER_NAME,
                          is_debug=False,
                          file_name=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(sh)

    if file_name:
        if exists(abspath(file_name)):
            unlink(file_name)
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def get_logger(module_name):
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)


def log(logger, msg, verbose=False):
    if verbose: print(msg)
    logger.info(msg)