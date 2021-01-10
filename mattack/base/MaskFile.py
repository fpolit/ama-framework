#!/usr/bin/env python3

import os
from fineprint.status import print_failure


from .FilePath import FilePath
from .Mask import Mask


class MaskFile(FilePath):
    def __init__(self, maskFilePath):
        super().__init__(maskFilePath)

    @staticmethod
    def isMaskFile(pathFile):
        masks = MaskFile(pathFile)
        with open(masks.pathFile(), 'r') as masksFile:
            while mask := masksFile.readline().rstrip():
                    if not Mask.isMask(mask):
                        return False
        return True