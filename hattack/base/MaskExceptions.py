#!/usr/bin/env python3


class MaskError(Exception):
    def __init__(self, mask):
        self.mask = mask
        self.warningMsg = f"Invalid mask: {self.mask}"
        super().__init__(self.warningMsg)
