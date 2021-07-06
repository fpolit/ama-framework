#!/usr/bin/env python3
#
# Process class that add mora attribute to multiprocessing.Process class
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from typing import List
from multiprocessing import Process
import time
from enum import Enum

class ProcessStatus(Enum):
    RUNNING = 0
    COMPLETED = 1
    UNSTARTED = 2
    FAILED = 3
    PENDING = 4


class CrackingProcess(Process):

    def __init__(self, id_process:int,
                 group=None, target=None, name=None, args=(), kwargs={},
                 depends:List[ProcessStatus] = [], *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.id_process = id_process
        self.submit_time = time.time()
        self.start_time = None
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
        self.start_time = time.time()
        for dependency_process in self.depends:
            if dependency_process.status() not in [ProcessStatus.COMPLETED, ProcessStatus.RUNNING]:
                dependency_process.start()

        for dependency_process in self.depends:
            dependency_process.join()

        super().start()

    def join(self, timeout=None):
        super().join(timeout)


    def info(self):
        """
        Return information about the process
        """
        information = {
            'id': self.id_process,
            'name': self.name,
            'status': self.status(),
            'start_time': self.start_time
        }

        return information
