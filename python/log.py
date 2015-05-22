#!/usr/bin/env python
# coding=utf-8

import os
import sys
import datetime
import logging
from logging.handlers import RotatingFileHandler

OUT_LOG_FILE = "david.log"

class Log(object):
    def __init__(self):
        self.rotate_out_file = "/tmp/update.log"
        self.init_log()

    def init_log(self):
        '''Init and config log format '''

        logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=OUT_LOG_FILE,
                        filemode='a')
                                      
        # rotate the log
        file_thandler = RotatingFileHandler('/tmp/update.py.log', maxBytes=10*1024*1024,backupCount=5)
        file_thandler.setLevel(logging.INFO)
        formatter = logging.Formatter(':%(lineno)d:%(asctime)s-%(levelname)s >> %(message)s')
        file_thandler.setFormatter(formatter)
        logging.getLogger('').addHandler(file_thandler)

    def warning(self, message = ""):
        logging.warning(message)

    def info(self, message = ""):
        logging.info(message)

    def debug(self, message = ""):
        logging.debug(message)

    def error(self, message = ""):
        logging.error(message)

def main():
    """main, start the process"""

    log = Log()
    log.warning("guzezuisabug")

if __name__ == '__main__':
    main()
