#!/usr/bin/env python3
#
# module commands set for ama-framework (Module Commands Category)
# commands set related to interactionw with modules
# defined commands: use, setv, setvg, back, attack
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
import sys
import argparse
from pathlib import Path
from fineprint.status import (
    print_failure,
    print_status,
    print_successful
)

from fineprint.color import ColorStr

# version import
from ama.version import get_version

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
from cmd2 import (
    Cmd,
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
)

# modules.base import
from ama.modules.base import (
    Attack,
    Auxiliary
)

# crackers
# from ama.plugins.cracker import (
#     John,
#     Hashcat
# )


@with_default_category(Category.MANAGER)
class Manager(CommandSet):
    """
    Command to monitor process manager
    """

    def __init__(self):
        super().__init__()



    def do_process(self, args):
        processes_status = self._cmd.manager.report()

        for status, processes_info in processes_status.items():
            print(f"{status}:\n")
            for process_info in processes_info:
                for key, value in process_info.items():
                    print(f"\t{key:<12}: {value}")
                print()
