#!/usr/bin/env python3

class CrackProcess:
    def __init__(self, process, status, cmd):
        self.process=process # popen process
        self.status = status
        self.cmd = cmd
        self.stdout=None
        self.stderr=None
        self.timout=None

    def pid(self):
        return self.process.pid
    def _updateStatus(self):
        if self.process.returncode is None:
            self.status = "Runing"
        else:
            self.status = "Finished"
    
    def getStatus(self):
        self._updateStatus()
        return self.status
    
    def kill(self):
        self.process.kill()
        
    def timeout(self, *, timeout):
        pass