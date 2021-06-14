#!/usr/bin/env python3
#
# john commands set for ama-framework (John Commands Category)
# commands set related to john the ripper
# defined commands:
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
import sys
import argparse

from fineprint.status import (
    print_failure,
    print_status,
    print_successful
)

from fineprint.color import ColorStr

# version import
from ama.core.version import get_version

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
from ama.core.modules.base import (
    Attack,
    Auxiliary
)

from ama.core.files import Path

## ssh utilities scripts
from .ssh2john import read_private_key

@with_default_category(Category.JOHN)
class JohnUtilities(CommandSet):
    """
    John command set category related to transform a key to a hash
    commands:
    """

    def __init__(self):
        super().__init__()

    ssh2john_parser = Cmd2ArgumentParser(description="ssh2john utility")
    ssh2john_parser.add_argument("keys", nargs='+', completer=Cmd.path_complete,
                                 help="RSA/DSA/EC/OpenSSH private key file(s)")
    ssh2john_parser.add_argument("-o", "--output", default=None, completer=Cmd.path_complete,
                                 help="Output File")

    @with_argparser(ssh2john_parser)
    def do_ssh2john(self, args):
        hashes = [read_private_key(key_file) for key_file in args.keys]
        if args.output:
            with open(args.output, 'w') as output:
                for h in hashes:
                    output.write(f"{h}\n")

            print_successful(f"Generated hashes was saved to {ColorStr(args.output).StyleBRIGHT} file")
        else:
            for h in hashes:
                print(f"{h}\n\n")
