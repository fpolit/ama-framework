#!/usr/bin/env python3

from .MaskExceptions import MaskError
from fineprint.status import print_failure
from math import ceil

class Mask(str):
    charset = ["?l", "?u", "?d", "?s"]
    def __init__(self, mask):
        try:
            if Mask.isMask(mask):
                self.mask = mask
            else:
                raise MaskError(mask)

        except MaskError as error:
            print_failure(error)


    @staticmethod
    def _genIterMask(mask):
        iterMask = iter(mask)
        maskSymbol = next(iterMask, "") + next(iterMask, "")
        while maskSymbol:
            yield maskSymbol
            maskSymbol = next(iterMask, "") + next(iterMask, "")

    @staticmethod
    def isMask(mask):
        for maskSymbol in Mask._genIterMask(mask):
            if not maskSymbol in Mask.charset:
                return False
        return True
    
    def __len__(self):
        return ceil(len(self.mask)/2)