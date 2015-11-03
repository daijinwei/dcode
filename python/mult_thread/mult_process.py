#!/bin/env/python
# -*- coding: utf-8 -*-

import os
import time
import signal
import threading

# global variable
is_stop          = False
threads          = []    # holds all the basic threads
monitor_thread   = ""    # monitor data thread

class MonitorThread(threading.Thread):
    """Moitor the os Thread"""
	
    def __init__(self):
        """Init the MonitorThread."""
		
        threading.Thread.__init__(self)
        self.is_stop = False
        self.setName("MonitorThread")

    def run(self):
        """Run a thread."""
		
        while not self.is_stop:
            # Your code
            pass

    def stop(self):
        """Stop the thread"""
		
        self.is_stop = True

def signal_handler(signo, frame):
    """signal func"""
	
    global is_stop
    if signo == signal.SIGINT:
        is_stop = True
    else:
        pass

# Store the thread info
def push_to_threads(thread, tclass):
    """Push a thread to a list"""
	
    thread_info = {}
    thread_info['name']   = thread.getName()
    thread_info['thread'] = thread
    thread_info['class']  = tclass
    threads.append(thread_info)

def is_in_threads(thread):
    """Judge a thread instance is in list or not"""

    for  v in threads:
        if v['thread'] == thread:
            return True
    return False

def delete_from_threads(thread):
    """Delete a thread from a list"""
	
    for v in threads:
        if v['thread'] == thread:
            threads.remove(v)
            return True
    return False

def main():
    """The main process"""

    tries = -1

    # Signal hander
    signal.signal(signal.SIGINT, signal_handler)

    # Start the threads
    monitor_thread = MonitorThread()
    monitor_thread.setDaemon(True)
    push_to_threads(monitor_thread, MonitorThread)
    monitor_thread.start()

    # check for threads alive, if not, restart it
    while not is_stop:
        for thread_info in threads:
            thread = thread_info['thread']
            name   = thread_info['name']
            if thread.isAlive() == False:
                if name == "MonitorThread":
                    try:
                        monitor_thread = MonitorThread()
                        monitor_thread.setDaemon()
                        push_to_threads(monitor_thread, MonitorThread)
                        monitor_thread.start()
                    except Exception, e:
                        exit(-1)
                else:
                    tclass = thread_info['class']
                    delete_from_threads(thread)
                    new_thread = tclass()
                    new_thread.start()
                    push_to_threads(new_thread, tclass)
        try:
            time.sleep(1)
        except Exception, e:
            pass

    # We receive SIGINT signal, notify all threads to quit
    for thread_info in threads:
        thread = thread_info['thread']
        tries += 1
        if tries == 5:
            exit(-1)

        if thread.isAlive() == True:
            thread.stop()
            try:
                time.sleep(1)
            except Exception as e:
                pass
        else:
            delete_from_threads(thread)
        try:
            time.sleep(1)
        except Exception as e:
            pass

if __name__ == '__main__':
    main()
