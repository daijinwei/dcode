#!/usr/bin/env python
# encoding=utf-8

import os
import sys
import re
import pdb
import MySQLdb
import datetime
import logging
import chardet
import urllib2
from logging.handlers import RotatingFileHandler
from crawl_leak_details_info import LeakInfoSpider
from crawl_leak_details_info import LeakDatabase

reload(sys)
sys.setdefaultencoding('utf-8')

#pdb.set_trace()

CNNVD_HOST= "http://www.cnnvd.org.cn"
CVEDETAILS_HOST = "http://www.cvedetails.com"

DATABASE_PATH = "vulnerability_lib"
OUT_LOG_FILE = "update_nsfoucs_leak_databases.py.log"
OUT_LEAK_DETAILS = "leak_details_info"

# Define the logging
warning = logging.warning
info    = logging.info
debug   = logging.debug
error   = logging.error

gLeakIdGenerator = 100
def get_leak_id():
    global gLeakIdGenerator
    tmp_id, gLeakIdGenerator = gLeakIdGenerator, gLeakIdGenerator + 1
    return tmp_id

def init_log():
    ''' '''

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=OUT_LOG_FILE,
                    filemode='a')

    file_thandler = RotatingFileHandler('/tmp/filter_version.py.log', maxBytes=10*1024*1024,backupCount=5)
    file_thandler.setLevel(logging.INFO)
    formatter = logging.Formatter(':%(lineno)d:%(asctime)s-%(levelname)s >> %(message)s')
    file_thandler.setFormatter(formatter)
    logging.getLogger('').addHandler(file_thandler)

class WebSpider(object):
    """Get the leak infomation from Internet"""

    def __init__(self, page_num):
        """Initial the var"""

        self.cnnvd_host = CNNVD_HOST
        self.page = page_num
        pass

    def get_web_info_from_time(self):
        """Get leak info being baseed time"""

        item_list = list()
        # set pattern
        today = datetime.date.today()
        yesterday = str(today - datetime.timedelta(days = 5))
        pattern = """<td width="45%"><a href="(.*?)" title="(.*?)">.*?</a></td>\x0d\x0a.*?align="center">""" + yesterday  + """</td>"""
        pattern_str = re.compile(pattern)
        try:
            for i in range(self.page):
                leak_url = str()
                leak_name = str()
                leak_list_url = self.cnnvd_host + "/" +  "vulnerability/index/p/" + str(i + 1) + '/'
                # request resource
                try:
                    request = urllib2.Request(leak_list_url)
                    response = urllib2.urlopen(request, timeout = 5)
                    response_text = response.read()
                except Exception, e:
                    debug(e)
                    continue

                leak_item_info = pattern_str.findall(response_text)
                for item in leak_item_info:
                    url, leak_name = item
                    leak_url = self.cnnvd_host + url
                    item_parttern = (leak_name, leak_url)
                    if item_parttern not in item_list:
                        item_list.append(item_parttern)
        except Exception,e:
            debug(e)

        return item_list


def get_leak_info():
    '''leak version'''

    count = 0
    try:
        spider = WebSpider(10)
        leak_brief_info_list = spider.get_web_info_from_time()

        leak = LeakInfoSpider()
        ret = leak.get_details_leak_info(leak_brief_info_list)

        leak_db = LeakDatabase()
        db = leak_db.connect()

        fd = open(OUT_LEAK_DETAILS, 'a+')
        for item in ret:
            try:
                count = count + 1
                leak_id = int()
                leak_name = str()
                leak_cnnvd = str()
                leak_url = str()
                leak_cve = str()
                product_type = str()
                vendor = str()
                product = str()
                software_version = str()
                published_time = str()
                update_time = str()
                threat_level = str()
                leak_type = str()
                threat_type = str()
                leak_description = str()
                leak_reference = str()
                leak_insert_time = str()

                leak_name, leak_cnnvd, leak_url, leak_cve, product_type, vendor, product, software_version, published_time, update_time, threat_level, leak_type, threat_type, leak_description, leak_reference = item
                leak_insert_time = datetime.date.today()
                #print leak_name, leak_cnnvd, leak_url, leak_cve, product_type, vendor, product, software_version, published_time, update_time, threat_level, leak_type, threat_type, leak_description, leak_reference, leak_insert_time
                message = '''%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s\n''' %(leak_name, leak_cnnvd, leak_url, leak_cve, product_type, vendor, product, software_version, published_time, update_time, threat_level, leak_type, threat_type, leak_description, leak_reference, leak_insert_time)
                fd.write(message)
                leak_id = get_leak_id()
                leak_db.insert(db, leak_id,  leak_name, leak_cnnvd, leak_url, leak_cve, product_type, vendor, product, software_version, published_time, update_time, threat_level, leak_type, threat_type, leak_description, leak_reference, leak_insert_time)
            except Exception, e:
                debug(e)
                continue
        fd.close()
        db.close()
    except Exception, e:
        debug(e)

def sched():
    """Call insert sched time"""

    try:
        while True:
            hour = datetime.datetime.now().hour
            if 0 == hour:
                break
            else:
                debug("not update time, sleep an hours")
                time.sleep(3600)

        hour = datetime.datetime.now().hour
        while True:
            update_leak_time = random.randint(0,3)
            if update_leak_time == hour:
                get_leak_info()
                debug("insert ok, sleep an hours")
                time.sleep(3600)
                break
    except Exception, e:
        debug(e)

def daemon_work():
    while True:
        try:
            sched()
        except Exception, e:
            debug(e)

def main():
    init_log()
    get_leak_info()
    #daemon_work()
    
if __name__ == '__main__':
    main()
