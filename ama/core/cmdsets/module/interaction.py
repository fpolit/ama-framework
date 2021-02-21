#!/usr/bin/env python3
#
# module commands set for ama-framework (Module Commands Category)
# commands set related to interactionw with modules
# defined commands: use, setv, setvg, back, attack
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse

# version import
from ...version import get_version

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)

@with_default_category(Category.MODULE)
class Interaction(CommandSet):
    """
    Module command set category related to interaction with ama modules
    commands set: use, setv, setvg, back, attack
    """

    def __init__(self):
        super().__init__()


    def do_use(self, args):
        """
        Select a avaliable module
        """
        pass

    def do_setv(self, args):
        """
        Set a value to a variable
        """
        pass

    def do_setvg(self, args):
        """
        Set a value to a variable globally
        """
        pass

    def do_back(self, args):
        """
        Stop interaction with selected module and go back to main ama-framework console
        """
        pass

    def do_attack(self, args):
        """
        Perform a attack with the selected module
        """
        pass

    def do_run(self, args):
        """
        Run the selected auxiliary module
        """
        pass
