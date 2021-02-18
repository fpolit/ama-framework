#!/usr/bin/env python3
#
# ama-framework interactor
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import sys

# cliff imports
from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff.command import Command

# import ama version
from ama.base.version import get_version

class Ama(App):
    """
    CLI App to interact with ama-framework
    """
    def __init__(self):
        super(Ama, self).__init__(
            description="ama-framework interactor",
            version=get_version(),
            command_manager = CommandManager("ama.cli"),
            deferred_help=True
        )


def main(argv=sys.argv[1:]):
    ama = Ama()
    return ama.run(argv)

