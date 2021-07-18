#!/usr/bin/env python3
#
# Mask class to validate masks in mask attacks
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from math import ceil
from fineprint.status import print_failure
import string


from .exceptions import InvalidMaskError


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
                raise InvalidMaskError(mask)

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
    def is_valid_mask(mask):
        for mask_symbol in Mask._genIterMask(mask):
            if not mask_symbol in Mask.charset:
                raise InvalidMaskError(mask)

    @staticmethod
    def is_mask(mask):
        for mask_symbol in Mask._genIterMask(mask):
            if mask_symbol not in Mask.charset:
                return False
        return True


    def is_valid_charset(charset):
        if charset in Mask.charset:
            return True
        return False

    def __len__(self):
        return ceil(len(self.mask)/2)
