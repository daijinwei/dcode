#!/usr/bin/env python
# coding=utf-8

import os
import re
import urllib2
import logging
from logging.handlers import RotatingFileHandler
from common import *

CNNVD_HOST = "http://www.cnnvd.org.cn"
OUT_LOG_FILE = "crawl_leak_brief_list.py.log"
LEAK_BRIEF_LIST_FILE = "nsfocus_leak_brief_list_file"
EXCEPT_URL_FILE = "except_url_file"

# Define the logging
warning = logging.warning
info    = logging.info
debug   = logging.debug
error   = logging.error

def init_log():
    '''Init logging some parmeters'''

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=OUT_LOG_FILE,
                        filemode='a')

    # /tmp rotate two log files
    file_thandler = RotatingFileHandler('/tmp/crawl_leak_brief_list.py.log', 
                                        maxBytes=10*1024*1024,backupCount=5)
    file_thandler.setLevel(logging.INFO)
    formatter = logging.Formatter(':%(lineno)d:%(asctime)s-%(levelname)s >> %(message)s')
    file_thandler.setFormatter(formatter)
    logging.getLogger('').addHandler(file_thandler)

class WebSpider(object):
    """Crawl the web info 
    
    """
    def __init__(self, page_num = 10):
        """Inits varible"""

        self.common_url = "http://www.cnnvd.org.cn/vulnerability/index/p/"
        self.page = page_num
        pass

    def get_leak_brief_list_info(self):
        """Get leak info, liel leak_url, cnnvd"""

        item_list = list()
        for i in range(self.page):
            try:
                leak_list_url = self.common_url + str(i + 1) + '/'
                try:
                    # Crawal the all web info
                    request = urllib2.Request(leak_list_url)
                    response = urllib2.urlopen(request, timeout = 5)
                    response_text = response.read()
                except Exception, e:
                    message = leak_list_url + '\n'
                    write_msg(EXCEPT_URL_FILE, message)
                    debug(e)

                # Get rul, name
                leak_details_url = str()
                leak_name = str()
                leak_pattern_str = re.compile(r'<td width="45%"><a href="(.*\s*.*)" title="(.*\s*.*)">.*\s*.*</a></td>\x0d\x0a.*align="center">')
                leak_item_info = leak_pattern_str.findall(response_text)
                if 0 >= len(leak_item_info):
                    trace_debug(TRACE_WARNING_LEVEL, leak_list_url, "Not crawal leak items")
                    message = leak_list_url + '\n'
                    write_msg(EXCEPT_URL_FILE, message)

                if 20 != len(leak_item_info):
                    trace_debug( TRACE_WARNING_LEVEL, leak_list_url, "Not crawal all 20 leak items")
                    message = leak_list_url + '\n'
                    write_msg(EXCEPT_URL_FILE, message)
                for item in leak_item_info:
                    uri, name = item
                    if is_str_null(uri.strip()):
                        debug(uri)
                    leak_details_url = CNNVD_HOST.strip() + uri
                    # Filter the '\n'
                    if -1 != name.find('\n'):
                        ret= name.split('\n')
                        for item in ret:
                            leak_name = leak_name + item + " "
                    else:
                        leak_name = name
                    leak_item = "%s,%s\n" %(leak_details_url, leak_name)
                    if leak_item not in item_list:
                        item_list.append(leak_item)
            except Exception, e:
                debug(e)
        return item_list

    def get_leak_file(self):
        """Get the file which store the leak message"""

        all_item = list()
        all_item = self.get_leak_brief_list_info()
        all_leak_info = '''%s\n'''%(''.join(all_item))
        write_msg(LEAK_BRIEF_LIST_FILE, all_leak_info)

def main():
    init_log()
    spider = WebSpider(2)
    spider.get_leak_file()

if '__main__' == __name__:
    main()
