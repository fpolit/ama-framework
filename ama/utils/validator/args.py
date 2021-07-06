#!/usr/bin/env python3
#
# Argument validator
#
# Feb 23 2021
# Implementation of argument validator
#
# Maintainer: glozanoa <glozanoa@uni.pe>

# varname package imports
from varname import argname

# validator exceptions import
from .exceptions import (
    SomeArgumentHasNoneValue,
    AllArgumentsHaveNoneValue,
    NotAllRequiredArgumentsSupplied
)


class Args:

    @staticmethod
    def not_none(*args):
        """
        Check that all its arguments are not None otherwise raise SomeArgumentHasNoneValue exception

        Raise:
        SomeArgumentHasNoneValue: Error if some arguments have None as value
        """
        someNone = False
        none_args = []

        names = argname(args)
        for name, arg in zip(names, args):
            if arg is None:
                someNone = True
                #cmd2.Cmd.pwarning(f"{name} variable is None")
                none_args.append(arg)

        if someNone:
            raise SomeArgumentHasNoneValue(*none_args)

    @staticmethod
    def some_not_none(*args):
        """
        Check if there is an argument not None otherwise raise AllArgumentsHaveNoneValue exception

        Raise:
        AllArgumentsHaveNoneValue: Error if all arguments are None
        """
        #import pdb; pdb.set_trace()

        someNotNone = False
        none_args = []

        names = argname(args)
        for name, arg in zip(names, args):
            if arg is not None:
                someNotNone = True
            else:
                #cmd2.Cmd.pwarning(f"{name} variable is None")
                none_args.append(arg)

        if not someNotNone: #all supplied argument are None
            raise AllArgumentsHaveNoneValue(*noneArgs)

    @staticmethod
    def no_empty_required_options(**kwargs): # kwargs format: {OPTION_NAME: OPTION_VALUE (Instance of Argument),...}
        """
        Check that all required variable are supplied otherwise raise NotAllRequiredArgumentsSupplied exception
        Raise:
           NotAllRequiredArgumentsSupplied: Error if some required argument wasn't supplied
        """

        all_supplied = True
        no_supplied_names = []

        for name, option in kwargs.items():
            if option.value is None:
                all_supplied = False
                no_supplied_names.append(name)

        if not all_supplied:
            raise NotAllRequiredArgumentsSupplied(no_supplied_names)
