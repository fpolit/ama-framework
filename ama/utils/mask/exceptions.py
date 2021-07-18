#!/usr/bin/env python3


class InvalidMaskError(Exception):
    def __init__(self, mask):
        self.mask = mask
        self.warningMsg = f"Invalid mask: {self.mask}"
        super().__init__(self.warningMsg)

class InvalidMaskSymbol(Exception):
    def __init__(self, maskSymbol):
        self.warning = f"Invalid Mask Symbol: {maskSymbol}"
        super().__init__(self.warning)
