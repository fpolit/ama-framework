#!/usr/bin/env python3
#
# Argument validator
#
# Feb 23 2021
# Implementation of argument validator
#
# Maintainer: glozanoa <glozanoa@uni.pe>

# cmd2 imports
import cmd2

# varname package imports
from varname import nameof

# validator exceptions import
from .exceptions import (
    NoneArgumentsError,
    AllNoneArgumentsError
)


class Args:

    @staticmethod
    def notNone(*args):
        """
        Check that all its arguments are not None otherwise raise a exception (NoneArgumentsError)

        Raise:
        NoneArgumentsError: Error if some arguments is None
        """
        someNone = False
        noneArgs = []

        for arg in args:
            if arg is None:
                someNone = True
                cmd2.Cmd.pwarning(f"{nameof(arg) variable is None}")
                noneArgs.append(arg)

        if someNone:
            raise NoneArgumentsError(noneArgs)

    @staticmethod
    def someNotNone(*args):
        """
        Check that if there is a argument not None otherwise raise a exception (AllNoneArgumentsError)

        Raise:
        AllNoneArgumentsError: Error if all arguments are  None
        """
        someNotNone = False
        noneArgs = []

        for arg in args:
            if arg is not None:
                someNotNone = True
            else:
                cmd2.Cmd.pwarning(f"{nameof(arg) variable is None}")
                noneArgs.append(arg)

        if not someNotNone: #some supplied argument is not None
            raise AllNoneArgumentsError(noneArgs)
