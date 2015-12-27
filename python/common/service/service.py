#!/usr/bin/env python
#coding=utf-8

import os
import sys
import signal
import inspect
import platform
import subprocess

def get_current_dir():

    caller_file = inspect.stack()[1][1]
    file_current_dirname = os.path.abspath(os.path.dirname(caller_file))
    return file_current_dirname

class ServiceFrame(object):
    """A ServiceFrame class or subclass can manage the process.
       
    Availability: Linux and Windows.
    """

    def __init__(self):
        self.__name = os.path.basename(sys.argv[0])

    def __get_pid_dir(self):
        """Get pid directory."""

        file_current_dirname = get_current_dir()
        tmp_dir = file_current_dirname + os.sep + r'tmp'
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)
        return tmp_dir

    def __pid_file(self):
        """Get the file which store the pid."""

        pid_file = self.__get_pid_dir() + os.sep + self.__name + r'.pid'
        return pid_file

    def __read_pid(self, file_path):
        """Read pid from file
           
        Args:
            file_path: pid file path
        Returns:
            Return the process pid.
        """

        if os.path.isfile(file_path):
            with open(file_path, 'rb') as fhandler:
                pid = fhandler.read().strip()
            return int(pid)
        else: return 0

    def __write_pid(self, file_path, pid):
        """Write pid to the pid file.
        
        Args:
            pid: process pid.
        """
        if not pid:
            return

        with open(file_path, 'wb') as fhandler:
            fhandler.write(str(pid))
            fhandler.flush()

    def __rm_pid(self):
        """Delete the pid file and directory."""
       
        file_path = self.__pid_file()
        if os.path.isfile(file_path):
            os.unlink(file_path)

        tmp_dir = self.__get_pid_dir()
        if os.path.isdir(tmp_dir):
            try:
                os.removedirs(tmp_dir)
            except OSError, e:
                pass

    def __clear_pid(self):
        """Clear the pid."""

        file_path = self.__pid_file()
        self.__write_pid(file_path, '0')
        self.__rm_pid()

    def __check_pid(self, pid):
        """Check the pid if exists."""

        if not pid:
            return False

        running_pid = None
        os_type = platform.system()
        if 'Linux' == os_type:
            cmd = "ps aux | grep %s | grep python | grep -v grep" %(str(pid))
        elif 'Windows' == os_type:
            cmd = 'tasklist /FI "PID eq %s" /FI "IMAGENAME eq python.exe "' %(str(pid))
        try:
            out = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            return False
        if 'Linux' == os_type:
            running_pid = int(out.split()[1])
        elif 'Windows' == os_type:
            try:
                running_pid = int(out.split()[-5])
            except Exception as e:
                running_pid = None
        if running_pid is not None:				
            if running_pid == int(pid):
                return True
            else: return False
        else: return False

    def __check_running(self):
        """Check the process is running or not."""

        file_path = self.__pid_file()
        pid = self.__read_pid(file_path) 
        if 0 < pid:
            if self.__check_pid(str(pid)):
                is_running = True
            else:
                is_running = False
            return is_running
        else: return False

    def __start(self):
        """Start a process."""

        if True == self.__check_running():
            os._exit(0)
        else: 
            collector_pid = os.getpid()
            file_path = self.__pid_file()
            self.__write_pid(file_path, collector_pid)

    def run(self):
        """Run a process, subclass can overwrite it."""
        pass

    def start(self):
        """Start a process."""

        self.__start()
        self.run()

    def _stop(self):

        """Stop a process"""

        if True == self.__check_running():
            file_path = self.__pid_file()
            pid = self.__read_pid(file_path) 
            os.kill(pid, signal.SIGTERM)
        else:
            print "%s not running" %(self.__name)
        self.__clear_pid()
        os._exit(0)

    def stop(self):
        """Stop a procsess."""

        self._stop()

    def restart(self):
        """Restart process"""

        self.stop()
        self.start()

    def status(self):
        """The process's status."""

        if True == self.__check_running():
            msg = "The %s is running" %(self.__name)
        else:
            msg = "The %s is stoped" %(self.__name)
        print msg

    def help(self):
        """Help info."""

        print "Usage: python %s start[, stop | restart | status | help]" %(self.__name)

def main():

    pass

if __name__ == '__main__':
    main()
