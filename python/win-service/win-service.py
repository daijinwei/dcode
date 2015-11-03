#!/bin/env/python
#coding=utf-8

import os
import sys
import time
import subprocess
import win32event
import win32service
import win32serviceutil
import logging

agent = None
LOGGER = None

# Work directory, assign by yourself.
worker_cwd = ""         
STOP = False
LOG_NAME = ""

def init_logger():
    """Init a log """

    global LOGGER
    MAX_LOG_SIZE = 1048576              # 1*1024*1024, 1M
    BACKUP_COUNT = 2
    LOGLEVEL = logging.INFO
    FORMATTER = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]%(message)s", "%Y-%m-%d %H:%M:%S")
    handler = logging.handlers.RotatingFileHandler(LOG_NAME, mode='a', maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    handler.setFormatter(FORMATTER)

    LOGGER = logging.getLogger()
    LOGGER.setLevel(LOGLEVEL)
    LOGGER.addHandler(handler)

class MyService(win32serviceutil.ServiceFramework):
    """Define the own service class."""

    _svc_name_ = "Service name"
    _svc_display_name_ = "Display service name on win service"
    _svc_description_  = "Describe the service"

    def __init__(self, args): 
        """Init a service."""

        win32serviceutil.ServiceFramework.__init__(self, args) 
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        """Run the process."""

        global agent

        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

        '''
        # We can add own process to run.
        # Add code.

        self.start()
        while not STOP:
            try: 
                ret = agent.poll()
                if ret is not None:
                    LOGGER.info("agent poll is error, Error %s" %(str(ret)))
                    python_path = os.path.dirname(util.get_script_path()) + os.sep + r'tool' + os.sep + r'python' + os.sep + r'install' + os.sep + r'python.exe'
                    agent_py = util.get_script_path() + os.sep + r'agent.py'
                    exc_path = python_path + ' ' + agent_py
                    agent = subprocess.Popen(exc_path,
                                             stdin=subprocess.PIPE, 
											 stdout=subprocess.PIPE,
											 stderr=subprocess.PIPE, 
											 shell = False,
											 cwd=worker_cwd)
                    time.sleep(1)
                else:
                    time.sleep(1)
            except Exception, e:
                LOGGER.error("Check agent failed: %s" %(str(e)))
            time.sleep(1)
        '''

        # Wait a envent terninate 
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        
    def SvcStop(self): 
        """Stop a service."""

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stop()

        # Set a event
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def start(self):
        """Start to do something, do it by yourself."""

        pass
        # TODO: start a process
        """
        global agent
        try:
            LOGGER.info("Agent_Service start")
            python_path = os.path.dirname(util.get_script_path()) + os.sep + r'tool' + os.sep + r'python' + os.sep + r'install' + os.sep + r'python.exe'
            agent_py = util.get_script_path() + os.sep + r'agent.py'
            exc_path = python_path + ' ' + agent_py
            agent = subprocess.Popen(exc_path, stdin=subprocess.PIPE, 
												stdout=subprocess.PIPE, 
												stderr=subprocess.PIPE, 
												shell = False, 
												cwd=worker_cwd)
        except Exception, e:
            LOGGER.error("Agent_Service, cmd: %s start agent.py failed: %s" %(exc_path, str(e)))
            if agent is None:
                sys.exit()
        """
    
    def stop(self):
        """Stop a service, do it by yourself."""
        
        pass

        '''
        global STOP

        agent.terminate()
        STOP = True
        '''

if __name__=='__main__':
    init_logger()
    try:
        win32serviceutil.HandleCommandLine(MyService)
    except Exception, e:
        LOGGER.error("start service failed: %s" %str(e))
