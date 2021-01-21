#!/usr/bin/env python3

from math import ceil
from fineprint.status import print_failure
import string

# base modules import
from .MaskExceptions import MaskError


class Mask(str):
    charset = {"?l" : string.ascii_lowercase,
               "?u" : string.ascii_uppercase,
               "?d" : string.digits,
               "?s" : string.punctuation,
               "?a" : string.printable
               }

    def __init__(self, mask):
        try:
            if Mask.isMask(mask):
                self.mask = mask
            else:
                raise MaskError(mask)

        except MaskError as error:
            print_failure(error)


    @staticmethod
    def _genIterMask(mask, inverse=False):
        if inverse:
            inverseMask = ""
            for charset in mask[::-2]:
                inverseMask += f"?{charset}"
            iterMask = iter(inverseMask)

        else:
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
