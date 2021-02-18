#!/usr/bin/env python3
#
# ama-framework's database interactor
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import sys

# cliff imports
from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff.command import Command

# fineprint imports
from fineprint.status import print_status


# import ama version
from ama.base.version import get_version

class AmaDBCLI(App):
    """
    CLI App to interact with ama-framework's database
    """
    def __init__(self):
        super(AmaDBCLI, self).__init__(
            description = "ama's database interactor",
            version = get_version(),
            command_manager = CommandManager("amadb.cli"),
            deferred_help=True
        )

def main(argv=sys.argv[1:]):
    amaDB = AmaDBCLI()
    return amaDB.run(argv)


class InitDB(Command):
    """
    Init ama-framework's database
    """
    def get_parser(self, prog_name):
        parser = super(InitDB, self).get_parser(prog_name)
        parser.add_argument('-f', '--force', action='store_true', help="Force init of ama's db")
        return parser

    def take_action(self, parsed_args):
        print_status("Hey! I0m running initDB")

