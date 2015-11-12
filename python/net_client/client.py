#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import select
import time
import logging.handlers
from logging.handlers import RotatingFileHandler

LOGGER = None

def init_logger():
    '''Init a log'''

    global LOGGER

    LOGNAME = "client.log"
    MAX_LOG_SIZE = 5*1024*1024
    BACKUP_COUNT = 2
    LOGLEVEL = logging.DEBUG
    FORMATTER = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]%(message)s", "%Y-%m-%d %H:%M:%S")
    handler = RotatingFileHandler(LOGNAME, mode='a', maxBytes = MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    handler.setFormatter(FORMATTER)
    LOGGER = logging.getLogger()
    LOGGER.setLevel(LOGLEVEL)
    LOGGER.addHandler(handler)
    return LOGGER

class Reporter(object):
    """Reporter, Send data to transfer."""
	
    def __init__(self, addrinfo_list, config, timeout=3):
        """Connect to the server and send data to server"""

        if len(addrinfo_list) <= 0:
            raise ValueError, "transfer address list <= 0"
        self.__logger			= {}
        self.__logger			= config['LOGGER']
        self.__addrinfo_list    = addrinfo_list                 #(ip:port) addr list
        self.__trans_num        = len(addrinfo_list)
        self.__addrinfo         = self.__get_addrinfo_list()
        self.__timeout          = timeout
        self.__sockfd           = self.__create_connect()       # socket fd

    def __get_addrinfo_list(self):
        '''Get addrinfo list.
        For example, [('192.168.1.1', 5986), ('10.1.1.1', 5986)].

        Return: sockfd.
        '''

        addr_info = []
        for index, item in enumerate(self.__addrinfo_list):
            (ip, port) = item.split(':')
            addr_info.append((ip, int(port)))
        return addr_info
        
    def __create_socket(self, ip, port):
        '''Create a socket, protocol-independent
        Args:
            According to ip and port, create a socket

        Returns:
            sockfd: If create socket success, return a sock object, else return None.
        '''

        sockfd = None
        try:
            sockaddrinfo = socket.getaddrinfo(ip, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        except socket.gaierror as msg:
            self.__logger.error("(%s, %d) getaddrinfo is failed, Error: %s" %(ip, port, str(msg)))
            sockfd = None
            return sockfd

        for res in sockaddrinfo:
            family, socktype, proto, canonname, sockaddr = res
            try:
                sockfd = socket.socket(family, socktype, proto)
                sockfd.settimeout(self.__timeout)
                break
            except socket.error as msg:
                self.__logger.error("(%s, %d) create socket failed, Error: %s" %(ip, port, str(msg)))
                sockfd = None 
                continue
        return sockfd

    def __create_connect(self):
        '''Connect to server

        Returns: if connect successfully, return sockfd, else return None.
        '''

        for addr in self.__addrinfo:
            (ip, port) = addr
            sockfd = self.__create_socket(ip, port)
            if None == sockfd:
                continue
            try:
                sockfd.connect((ip, port))
                sockfd.setblocking(False)	                # Set nonblocking
                break
            except Exception as msg:
                if None != sockfd:
                    sockfd.close()
                sockfd = None
                self.__logger.error("address %s:%d Connnect to socket is failed, Error: %s" %(ip, port, str(msg)))
        return sockfd

    def __sendall_data(self, sockfd, data):
        '''Send data to server
        
        Args:
            sockfd: the sock objbect
            data: The data be send.
        
        Returns:
            ret: send data successful, return the length of data, else return -1
        '''

        ret = -1
        try:
            if None == sockfd.sendall(data):
                ret = len(data)
        except Exception, e:
            if None != sockfd:
                sockfd.close()
            ret = -1
            self.__logger.info("socket.sendall data failed, Error: %s" %(str(e)))
        return ret

    def __send(self, sockfd, data):
        """According to select, send data.
           
        Args:
            sockfd: socket fd.
            data:   the string will be sent.
        Returns:
            If send string successfully, return 0, else return -1.
        """

        rlist = []
        wlist = []
        elist = []
        send_success_flag = False

        if None == sockfd:
            return -1

        rlist.append(sockfd)
        wlist.append(sockfd)

        while True:
            if ((len(rlist) < 1) and (len(wlist) < 1)):
                break

            try:
                (read_list, write_list, exception_list) = select.select(rlist, wlist, elist, self.__timeout)
            except select.error, e:
                (errno, msg) = e
                self.__logger.error("select failed, errno: %d, Error: %s" %(errno, msg))
                break

            if not (read_list or write_list or exceptin_list):
                self.__logger.info("select timeout")
                break

            # send data
            for write_fd in write_list:
                ret = self.__sendall_data(write_fd, data)
                if -1 == ret:
                    self.__logger.info("send data failed")
                if wlist:
                    wlist.remove(write_fd)
                
            # Recv data, Judge if send data success
            bufsize = 256
            for read_fd in read_list:
                # Just recv
                msg = read_fd.recv(bufsize)
                if 'ok' == msg:
                    send_success_flag = True
                if rlist:
                    rlist.remove(write_fd)

        if True == send_success_flag:
            return 0
        else:
            self.__logger.info("send data faild")
            return -1

    def send_data_to_server(self, data):
        '''Send data to all server
           
        Args:
            data: The message will be sent.
        Returns:
            If send data successfully, return 0, else return -1;
        '''
       
        ret = int()
        counter = 0
        times = 3
        while counter < times:
            if None == self.__sockfd:
                self.__sockfd = self.__create_connect()
                time.sleep(1)
                counter += 1

            if None != self.__sockfd:
                ret = self.__send(self.__sockfd, data)
                break

        if counter == times:
            return -1
        return ret

def main():
    """The main process"""
	
    global LOGGER

    conf = {}
    LOGGER = init_logger()
    conf["LOGGER"] = LOGGER

    reporter = Reporter(["192.168.1.1:8080", "192.168.1.2:8080"], conf, 3)
    data = "This is just a test string"
    while True:
        try:
            ret = reporter.send_data_to_server(data)
            if ret == 0:
                print "send data ok"
        except Exception, e:
            print "send data failed %s" % str(e)
        time.sleep(5)

if __name__ == '__main__':
    main()
