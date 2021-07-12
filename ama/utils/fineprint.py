#!/usr/bin/env python3
#
# functions to print and log status of situations
#
# Status:
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import logging
from enum import Enum

from .color import ColorStr



class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    EXCEPTION = 60



def print_failure(msg:str, logger:logging.Logger = None, loglevel = LogLevel.WARNING):
    msg_status = ColorStr.ForeRED("[-] ") + msg
    print(msg_status)

    if isinstance(logger, logging.Logger):

        if loglevel == LogLevel.DEBUG:
            logger.debug(msg)
        elif loglevel == LogLevel.INFO:
            logger.info(msg)
        elif loglevel == LogLevel.WANING:
            logger.warning(msg)
        elif loglevel == LogLevel.ERROR:
            logger.error(msg)
        elif loglevel == LogLevel.CRITICAL:
            logger.critical(msg)
        elif loglevel == LogLevel.EXCEPTION:
            logger.exception(msg)
        else:
            print_failure("Invalid log level", logger, loglevel=LogLevel.ERROR)



def print_successful(msg:str, logger:logging.Logger = None, loglevel = LogLevel.INFO):
    msg_status = ColorStr.ForeGREEN("[+] ") + msg
    print(msg_status)

    if isinstance(logger, logging.Logger):

        if loglevel == LogLevel.DEBUG:
            logger.debug(msg)
        elif loglevel == LogLevel.INFO:
            logger.info(msg)
        elif loglevel == LogLevel.WANING:
            logger.warning(msg)
        elif loglevel == LogLevel.ERROR:
            logger.error(msg)
        elif loglevel == LogLevel.CRITICAL:
            logger.critical(msg)
        elif loglevel == LogLevel.EXCEPTION:
            logger.exception(msg)
        else:
            print_failure(f"Invalid log level: {loglevel}", logger, loglevel=LogLevel.ERROR)

def print_status(msg:str, logger:logging.Logger = None, loglevel = LogLevel.INFO):
    msg_status = ColorStr.ForeCYAN("[*]  ") + msg
    print(msg_status)

    if isinstance(logger, logging.Logger):

        if loglevel == LogLevel.DEBUG:
            logger.debug(msg)
        elif loglevel == LogLevel.INFO:
            logger.info(msg)
        elif loglevel == LogLevel.WANING:
            logger.warning(msg)
        elif loglevel == LogLevel.ERROR:
            logger.error(msg)
        elif loglevel == LogLevel.CRITICAL:
            logger.critical(msg)
        elif loglevel == LogLevel.EXCEPTION:
            logger.exception(msg)
        else:
            print_failure(f"Invalid log level: {loglevel}", logger, loglevel=LogLevel.ERROR)
