#!/usr/bin/env python
# coding=utf-8

import os
import re
import urllib2
import logging
from logging.handlers import RotatingFileHandler

# Define the logging
warning = logging.warning
info    = logging.info
debug   = logging.debug
error   = logging.error

def is_str_null(msg):
    """ If the msg is NULL, return True

        Args:
            msg: the strings
        Return: 
            If the msg is null, return true, else return False
    """

    if None == msg or "" == msg:
        return True
    return False

# lgo level
TRACE_ERROR_LEVEL =             10
TRACE_WARNING_LEVEL =           6
TRACE_SYSTEM_LOG_LEVEL =        4
TRACE_LOG_LEVEL =               3
gTraceDebugLevel = TRACE_SYSTEM_LOG_LEVEL

def trace_debug(level, header, msg):
    """Trace the process
    
        Args:
            level: Log level
            header: The log header
            msg: log message
    """

    if level < gTraceDebugLevel:
        return
    if is_str_null(header):
        print ("%s " %s (msg))
    else:
        print ("%s: %s" %(header, msg))

def write_msg(file_path, msg):
    """Write a message to a file 

        Args:
            file_path: A file which store message
            msg: The message

        Raises:
            Exception: An error occurred open file 
    """
    try:
        fd = open(file_path, 'a+')
        fd.write(msg)
        fd.close()
    except Exception, e:
        debug(e)
