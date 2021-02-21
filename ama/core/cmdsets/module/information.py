#!/usr/bin/env python3
#
# module commands set for ama-framework (Module Commands Category)
# commands set related to information of modules
# defined commands: info, options, advanced
#
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
class Information(CommandSet):
    """
    Module command set category related to supplied information of ama modules
    commands set: info, options, advance
    """

    def __init__(self):
        super().__init__()

    info_parser = argparse.ArgumentParser()
    info_parser.add_argument('module',
                             help="ama module")
    @with_argparser(info_parser)
    def do_info(self, args):
        """
        Supplied information about a module
        """
        pass

    def do_options(self, args):
        """
        Show availables options of a module
        """
        pass
