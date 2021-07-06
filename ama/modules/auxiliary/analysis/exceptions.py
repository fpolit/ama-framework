#!/usr/bin/env python3
#
# Exceptions to manage error of auxiliary/analysis modules
#
# Maintainer: glozanoa <glozanoa@uni.pe>

# analysis/pack_masksgen exceptions
class InvalidSortingMode(Exception):
    def __init__(self, invalid_sorting_mode):
        self.sorting_mode = invalid_sorting_mode
        self.warning = f"Invalid maskgen sorting mode: {self.sorting_mode}"

        super().__init__(self.warning)
