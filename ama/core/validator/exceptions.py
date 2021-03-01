#!/usr/bin/env python3
#
# Exceptions to manage error generated in validator modules
#
# Feb 23 2021
# Implementation of argument validator
#
# Maintainer: glozanoa <glozanoa@uni.pe>

# varname package imports
from varname import argname

#arg module exceptions
class SomeArgumentHasNoneValue(Exception):
    """
    Exception to catch error when some argument have None value
    """
    def __init__(self, *noneArgs):
        self.warning = "Supplied arguments with None value:"

        names = argname(none_args)

        for index, name in enumerate(names):
            last_index = (len(names)-1)
            if index == last_index:
                self.warning += f" {name}"
            else:
                self.warning += f" {name},"

        super().__init__(self.warning)


class AllArgumentsHaveNoneValue(Exception):
    """
    Exception to catch error when all the supplied arguments are None
    """
    def __init__(self, *none_args):
        self.warning = "All supplied argument have None value"
        super().__init__(self.warning)


class NotAllRequiredArgumentsSupplied(Exception):
    """
    Exception to catch error when not all the required arguments was supplied
    """
    def __init__(self, args_names):
        self.warning = "Required arguments with None value:"

        #names = argname(none_args)
        for index, name in enumerate(args_names):
            last_index = (len(args_names)-1)
            if index == last_index:
                self.warning += f" {name.upper()}"
            else:
                self.warning += f" {name.upper()},"

        super().__init__(self.warning)
