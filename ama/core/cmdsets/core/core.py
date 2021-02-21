#!/usr/bin/env python3
#
# core commands set from ama-framework (Core Commands Category)
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse

# version import
from ..version import get_version

# commandset categories
from .category import CmdsetCategory as Category

# cmd2 imports
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)

#import hashes
from ...data.hashes import (
    jtrHashes,
    hcHashes
)

# import crackers
from ..modules.cracker import (
    John,
    Hashcat,
)

@with_default_category(Category.CORE)
class Core(CommandSet):
    """
    Core command set category
    """

    def __init__(self):
        super().__init__()

    def do_exit(self):
        """
        Exit ama-framework
        """
        return True

    def do_version(self):
        """
        ama-framework version
        """
        return get_version()

    hashes_parser = argparse.ArgumentParser()
    hashes_parser.add_argument('-c', '--cracker', choices=['jtr', 'hc'], required=True,
                               help="Password cracker")

    hashes_parser.add_argument('-s', '--sensitive',
                               help="Sensitive search")

    hashes_parser.add_argument('pattern',
                               help="Pattern to search")

    @with_argparser(hashes_parser)
    def do_hashes(self, args):
        """
        Search by valid hashes types
        """
        if args.cracker == "jtr":
            John.searchHash(args.pattern, sensitive=args.sensitive)
        else: # cracker == hc
            Hashcat.searchHash(args.pattern, sensitive=args.sensitive)
