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
from tabulate import tabulate
import time

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


    PROCESS_INFO = ['id', 'pid', 'elapsed_time', 'submit_state', 'status', 'depends', 'name']

    process_parser = argparse.ArgumentParser()
    process_parser.add_argument('-c', '--columns', nargs='*',
                                default=PROCESS_INFO, choices=PROCESS_INFO, metavar="COLUMN",
                                help='Columns to show')
    process_parser.add_argument('-s', '--submit-state', dest='submit_states', nargs='*', metavar="STATE",
                                default=[], choices=['PROCESSING', 'PENDING', 'COMPLETED'],
                                help='Filter process by submit status')
    process_parser.add_argument('-k', '--kill', nargs='*', default=[],
                                help='ID of processes to kill')

    @with_argparser(process_parser)
    def do_process(self, args):
        """
        Command to show and manage submitted process
        """
        processes_status = self._cmd.manager.report()

        columns = args.columns
        submit_states = args.submit_states

        kill_processes = args.kill

        if kill_processes:
            self._cmd.manager.kill(kill_processes)

        else:
            rows = []
            for sstate, processes_info in processes_status.items():
                if submit_states and sstate.upper() not in submit_states:
                    continue

                for process_info in processes_info:
                    process_info['submit_state'] = sstate.upper()
                    row = []
                    for column in columns:
                        row.append(process_info[column])
                    rows.append(row)

            print(tabulate(rows, headers=columns))
