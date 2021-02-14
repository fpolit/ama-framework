#!/usr/bin/env python3

import os
from fineprint.status import print_failure

class FilePath(str):
    def __init__(self, filePath):
        try:
            self.path = None
            if os.path.isfile(filePath):
                    self.path = filePath

            else:
                if os.path.exists(filePath) and not os.path.isfile(filePath):
                    raise IsADirectoryError

                if not os.path.exists(filePath): # no exist file
                    raise FileNotFoundError

                # elif not os.access(filePath, os.R_OK):
                #     raise PermissionError

        except PermissionError as error:
            print_failure(f"ERROR: {error}")

        except FileNotFoundError as error:
            print_failure(f"ERROR: {error}")

        except IsADirectoryError as error:
            print_failure(f"ERROR: {error}")

    def pathFile(self):
        return self.path

    def checkReadAccess(self):
        filePath = self.path
        if os.access(filePath, os.R_OK):
            return True
        return False

    def checkWriteAccess(self):
        filePath = self.path
        if os.access(filePath, os.W_OK):
            return True
        return False

    def checkrwAccess(self):
        filePath = self.path
        if os.access(filePath, os.W_OK) and os.access(filePath, os.R_OK):
            return True
        return False

    @staticmethod
    def readAccess(path):
        filePath = FilePath(path)
        if os.access(filePath, os.R_OK):
            return True
        return False


    @staticmethod
    def writeAccess(path):
        filePath = FilePath(path)
        if os.access(filePath, os.W_OK):
            return True
        return False

    @staticmethod
    def rwAccess(path):
        filePath = FilePath(path)
        if os.access(filePath, os.W_OK) and os.access(filePath, os.R_OK):
            return True
        return False


    def __repr__(self):
        return self.path

"""
    @staticmethod
    def readBlock(path, BLOCK):
        filePath = FilePath(path)
        if filePath.checkReadAccess():
            with open(filePath, 'r') as fileBlock:
                readBlock = [fileBlock.readline().rstrip() for k in range(BLOCK)]
            return readBlock
"""
