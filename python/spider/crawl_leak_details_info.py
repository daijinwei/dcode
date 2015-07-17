#!/usr/bin/env python
# encoding=utf-8

import os
import sys
import re
import MySQLdb
import datetime
import logging
import urllib2
import chardet
from logging.handlers import RotatingFileHandler
from common import *

#CNNVD_HOST= "http://www.cnnvd.org.cn"
CVEDETAILS_HOST = "http://www.cvedetails.com"
LEAK_INFO_FILE = "nsfocus_leak_brief_list_file"
OUT_LOG_FILE = "crawl_leak_details_info.py.log"
DATABASE_PATH = "vulnerability_lib"
OUT_LEAK_DETAILS = "leak_details_info"
DETAILS_URL_TIMEOUT = "details_url_timeout"

reload(sys)
sys.setdefaultencoding('utf-8')

# Over define the logging
warning = logging.warning
info    = logging.info
debug   = logging.debug
error   = logging.error

gLeakIdGenerator = 104096
def get_leak_id():
    global gLeakIdGenerator
    tmp_id, gLeakIdGenerator = gLeakIdGenerator, gLeakIdGenerator + 1
    return tmp_id

def init_log():
    '''Inits logger files '''
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=OUT_LOG_FILE,
                    filemode='a')

    file_thandler = RotatingFileHandler('/tmp/download_leak_details_info.py.log',
                                         maxBytes=10*1024*1024,backupCount=5)
    file_thandler.setLevel(logging.INFO)
    formatter = logging.Formatter(':%(lineno)d:%(asctime)s-%(levelname)s >> %(message)s')
    file_thandler.setFormatter(formatter)
    logging.getLogger('').addHandler(file_thandler)

def get_software_info_from_evedetails(uri_path):
    '''Get the software product_type, vendor, product, software_version from cvedetails.

        Args:
            uri_path: The cvedetails uri
        return: A list contains (product_type, vendor, product, software_version)
    '''

    result_pattern = list()
    result = list()
    details_info_map = dict()
    url = CVEDETAILS_HOST + uri_path

    try:
        try:
            request = urllib2.Request(url.strip())
            response = urllib2.urlopen(request, timeout = 5)
            response_text = response.read()
            pattern_str = re.compile(r'<td>(\s*\S*\s*)</td>(\s*)<td>(\s*)<a href="(.*?)" title="(.*?)">(.*?)</a>(\s*)</td>(\s*)<td>(\s*)<a href="(.*?)" title="(.*?)">(.*?)</a>(\s*.*)</td>(\s*)<td>(\s*\S*\s*)</td>')
            result_pattern = pattern_str.findall(response_text)
        except Exception, e:
            url = url + '\n'
            write_msg(DETAILS_URL_TIMEOUT, url)
            debug(e)

        # Construct product_type -> vendor -> product
        for item in result_pattern:
            product_type, b, c, d, e, vendor, g, h, i, j, k, product, m, n, version = item
            if not details_info_map.has_key(product_type.strip()):
                details_info_map[product_type.strip()] = dict()
            vendor_info_map = details_info_map[product_type.strip()]

            if not vendor_info_map.has_key(vendor.strip()):
                vendor_info_map[vendor.strip()] = dict()
            product_info_map = vendor_info_map[vendor.strip()]

            if not product_info_map.has_key(product.strip()):
                product_info_map[product.strip()] = list()
            versions = product_info_map[product.strip()]
            if version.strip() not in versions:
                versions.append(version.strip())

        # Generator software item
        for product_type_pattern, vendor_item in details_info_map.items():
            for vendor_pattern, product_item in vendor_item.items():
                for product_pattern, software_list in product_item.items():
                    software_version_pattern = str()
                    if 0 < len(software_list):
                       for version_item in software_list:
                           software_version_pattern = software_version_pattern +  version_item + " "
                    item = (product_type_pattern, vendor_pattern, product_pattern, software_version_pattern)
                    if item not in result:
                        result.append(item)
    except Exception, e:
        debug(e)
    return result

class LeakBriefList(object):
    '''Get the leak url from file '''

    def __init__(self):
        '''Init the var'''
        pass

    def get_brief_leak_lists(self, file_path = LEAK_INFO_FILE):
        '''Get the leak url, leak name from file.

            Args:
                file_path: The file path
            return:
                leak_info about leak url, leak name
        '''
        leak_info = list()
        for line in open(file_path, 'r'):
            try:
                if len(line) > 0:
                    url = line.strip().split(',')[0]
                    name = line.strip().split(',')[1]
                    items = (name, url)
                    leak_info.append(items)
                else:
                    continue
            except:      
                debug("Can not find nsfocus leak database")
        return leak_info

class LeakInfoSpider(object):
    '''Get the leak infomation'''

    def __init__(self):
        """Initial"""
        pass

    def get_details_leak_info(self, leak_brief_info_list):
        '''Using CVE to search leak infomation.

           Args:
               leak_name: the leak nameme
           Return:
               The infomation about cve

        '''

        leak_details_info = list()
        for item in leak_brief_info_list:
            try:
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
                leak_references = str()

                #leak_url = item.split(",")[0].strip()
                leak_name, leak_url = item
                #leak_url, leak_name = item
                try:
                    request = urllib2.Request(leak_url.strip())
                    response = urllib2.urlopen(request, timeout = 5)
                    response_text = response.read()
                except Exception,e:
                    debug(e)
                    continue

                # Parse cnnvd
                cnnvd_pattern_str = re.compile(r'<td>CNNVD编号：</td>(\s)*<td class="displayitem">(.*?)</td>')
                cnnvd_text = cnnvd_pattern_str.findall(response_text)
                for item in cnnvd_text:
                    leak_cnnvd = item[1].strip()

                # Parse cve
                cve_pattern_str = re.compile(r'<td><a href="(.*?)" target="(.*?)" >CVE(.*?)</a></td>')
                cve_text = cve_pattern_str.findall(response_text)
                for item in cve_text:
                    url, target, leak_cve = item
                    leak_cve = "CVE" + leak_cve.strip()

                # parse publish time
                published_pattern_str = re.compile(r'<td>发布时间：</td>(\s)*<td class="displayitem"><a href="(.*?)">(.*?)</a></td>')
                published_text = published_pattern_str.findall(response_text)
                for item in published_text:
                    published_time = published_time + item[2].strip() + ' '

                # parse updfate time
                update_pattern_str = re.compile(r'<td>更新时间：</td>(\s)*<td class="displayitem"><a href="(.*?)">(.*?)</a></td>')
                update_text = update_pattern_str.findall(response_text)
                for item in update_text:
                    update_time = update_time + item[2].strip() + ' '

                # parse threat level
                threat_level_pattern_str = re.compile(r'<td>危害等级：</td>(\s)*<td class="displayitem"><a href="(.*?)">(.*?)</a>&nbsp;')
                threat_level_text = threat_level_pattern_str.findall(response_text)
                if 0 < len(threat_level_text):
                    threat_level = threat_level_text[0][2].strip()

                # Parse threat_type
                leak_type_pattern_str = re.compile(r'<td>漏洞类型：</td>(\s)*<td class="displayitem"><a href="(.*?)">(.*?)</a></td>')
                leak_type_text = leak_type_pattern_str.findall(response_text)
                for item in leak_type_text:
                    leak_type = item[2].strip()

                # Parse threat_type
                threat_type_pattern_str = re.compile(r'<td>威胁类型：</td>(\s)*<td class="displayitem"><a href="(.*?)">(.*?)</a></td>')
                threat_type_text = threat_type_pattern_str.findall(response_text)
                for item in threat_type_text:
                    threat_type = item[2].strip()

                # parse descrption
                desc_pattern_str = re.compile(r'<p class="displayitem" style="margin:0;paddng:0;">(.*?)</p>')
                desc_text = desc_pattern_str.findall(response_text)
                for item in desc_text:
                    leak_description = leak_description + item + ' '

                # parse reference
                references_pattern_str = re.compile(r'链接:<a href="(.*?)" target="(.*?)" rel="(.*?)">(.*?)</a>')
                references_text = references_pattern_str.findall(response_text)
                for item in references_text:
                    ref = item[3].strip()
                    if ref not in leak_references:
                        leak_references = leak_references + ref + ' '

                # Get leak product_type, vendor, product, software_version
                if is_str_null(leak_cve.strip()):
                    items = (leak_name, leak_cnnvd, leak_url, leak_cve, 
                         product_type, vendor, product, software_version, 
                         published_time, update_time, threat_level, leak_type,
                         threat_type, leak_description, leak_references)
                    leak_details_info.append(items)
                else:  
                    uri = "/cve/" + leak_cve.strip()
                    software_info_result = get_software_info_from_evedetails(uri)
                    for item in software_info_result:
                        product_type, vendor, product, software_version = item
                        items = (leak_name, leak_cnnvd, leak_url, leak_cve, 
                                 product_type, vendor, product, software_version, 
                                 published_time, update_time, threat_level, leak_type,
                                 threat_type, leak_description, leak_references)
                        leak_details_info.append(items)
            except Exception,e:
                debug(e)
        return leak_details_info

class LeakDatabase(object):
    """ """
    def __init__(self):
        self.db_path = DATABASE_PATH
        pass

    def connect(self):
        #db = MySQLdb.connect(host = '10.24.20.151')
        try:
            db = MySQLdb.connect(host = 'localhost', 
                                 user = 'root', 
                                 passwd = 'root', 
                                 db = DATABASE_PATH, 
                                 charset = 'utf8')
            return db
        except Exception, e:
            debug(e)

    def close(self, db):
        db.close()

    def insert(self, db, *leak_items):
        cursor = db.cursor()
        leak_id, leak_name, leak_cnnvd, leak_url, leak_cve, product_type,vendor, product, software_version, published_time,update_time, threat_level, leak_type, threat_type, leak_info, leak_ref, leak_insert_time = leak_items

        sql = '''insert into leak8 values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        try:
            # execute the sql
            cursor.execute(sql, (str(leak_id), leak_name, leak_cnnvd, leak_url, 
                                 leak_cve, product_type, vendor, 
                                 product, software_version,
                                 published_time, update_time, threat_level, 
                                 leak_type, threat_type, leak_info, 
                                 leak_ref, leak_insert_time))
            # commit to db
            db.commit()
            pass
        except Exception, e:
            debug(e)
            db.rollback()

def insert():
    """Using leak_name to search leak info using leak_name.

       Args:
           leak_name: The leak name 
       Return: The infomation about leak

    """

    try:
        leak_brief = LeakBriefList()
        leak_brief_info_list = leak_brief.get_brief_leak_lists(LEAK_INFO_FILE)

        leak = LeakInfoSpider()
        ret = leak.get_details_leak_info(leak_brief_info_list)

        leak_db = LeakDatabase()
        db = leak_db.connect()
        fd = open(OUT_LEAK_DETAILS, 'a+')
        for item in ret:
            try:
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
                

                leak_name, leak_cnnvd, leak_url, leak_cve, product_type,\
                vendor, product, software_version, published_time, update_time,\
                threat_level, leak_type, threat_type, leak_description,\
                                                           leak_reference = item
                leak_insert_time = datetime.date.today()

                message = '''%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s\n''' %\
                             (leak_name, leak_cnnvd, leak_url, leak_cve, 
                              product_type, vendor, product, software_version,
                              published_time, update_time, threat_level,
                              leak_type, threat_type, leak_description, 
                              leak_reference, leak_insert_time)
                fd.write(message)
                leak_id = get_leak_id()
                leak_db.insert(db, leak_id, leak_name, leak_cnnvd, leak_url, 
                                           leak_cve, product_type, vendor, 
                                           product, software_version, 
                                           published_time, update_time, 
                                           threat_level, leak_type, threat_type,
                                           leak_description, leak_reference, 
                                           leak_insert_time)
            except Exception, e:
                debug(e)
                continue
        fd.close()
        db.close()
    except Exception, e:
        debug(e)

def main():
    '''main, start the process'''
    # Initialize the log
    init_log()
    insert()

if __name__ == '__main__':
    main()
