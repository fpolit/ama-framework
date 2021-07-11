#!/usr/bin/env python3
#
# Process class that add mora attribute to multiprocessing.Process class
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from typing import List
from multiprocessing import Process as SystemProcess
import time
from enum import Enum

class ProcessStatus(Enum):
    RUNNING = 0
    COMPLETED = 1
    UNSTARTED = 2
    FAILED = 3
    PENDING = 4
    CLOSED = 5


class Process(SystemProcess):
    """
    Process to proccess a module
    """
    def __init__(self, id_process:int,
                 group=None, target=None, name=None, args=(), kwargs={},
                 depends:List[ProcessStatus] = [], *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.id_process = id_process # relative ID
        self.submit_time = time.time()
        self.start_time = None
        self.end_time = None
        self.depends = depends

    def status(self):
        """
        Return status of process
        """
        if self.is_alive():
            return ProcessStatus.RUNNING
        else:
            if self.exitcode is None:
                return ProcessStatus.UNSTARTED

            if self.exitcode == 0:
                return ProcessStatus.COMPLETED

            for dependency in self.depends:
                if dependency.status() in [ProcessStatus.RUNNING, ProcessStatus.PENDING]:
                    return ProcessStatus.PENDING

            return ProcessStatus.FAILED


    def start(self):
        #import pdb; pdb.set_trace()
        self.start_time = time.time()

        any_failed = False
        for dependency_process in self.depends:
            status = dependency_process.status()
            if status not in [ProcessStatus.COMPLETED, ProcessStatus.RUNNING]:
                if status == ProcessStatus.FAILED:
                    any_failed = True
                    continue
                dependency_process.start()

        for dependency_process in self.depends:
            status = dependency_process.status()
            if status != ProcessStatus.FAILED:
                dependency_process.join()

        if not any_failed:
            super().start()
        else:
            self.close()

    def join(self, timeout=None):
        if self._popen:
            super().join(timeout)
            self.end_time = time.time()
            self.close()


    def info(self, quiet:bool = True):
        """
        Return information about the process
        """
        information = {
            'id': self.id_process,
            'name': self.name,
        }

        if self.start_time:
            if self.end_time:
                information['elapse_time'] = self.end_time - self.start_time
            else:
                information['elapse_time'] = time.time() - self.start_time
        else:
            information['elapsed_time'] = None

        pid = None
        try:
            pid = self.pid
            information['pid'] = pid

        except Exception as error: #this process was closed
            if not quiet:
                print(error)
            
            information['pid'] = None

        status = None
        try:
            status = self.status()
            
            information['status'] = status
        except Exception as error:
            if not quiet:
                print(error)

            information['status'] = ProcessStatus.CLOSED



        return information