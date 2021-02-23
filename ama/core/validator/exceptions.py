#!/usr/bin/env python3
#
# Exceptions to manage error generated in validator modules
#
# Feb 23 2021
# Implementation of argument validator
#
# Maintainer: glozanoa <glozanoa@uni.pe>

# varname package imports
from varname import nameof

# arg module exceptions
class NoneArgumentsError(Exception):
    """
    Exception to catch error when some argument have None value
    """
    def __init__(self, noneArgs):
        self.warning = "supplied arguments with None value:"

        for arg in noneArgs:
            self.warning += f" {nameof(arg)}, "

        super().__init__(self.warning)


class AllNoneArgumentsError(Exception):
    """
    Exception to catch error when all the supplied arguments are None
    """
    def __init__(self, noneArgs):
        self.warning = "All supplied argument have None value:"

        for arg in noneArgs:
            self.warning += f" {nameof(arg)}, "

        super().__init__(self.warning)

