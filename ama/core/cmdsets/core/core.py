#!/usr/bin/env python3
#
# core commands set from ama-framework (Core Commands Category)
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse

# version import
from ama.core.version import get_version

#banner import
from ama.core.banner import Banner

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
import cmd2
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)

#import hashes
from ama.data.hashes import (
    jtrHashes,
    hcHashes
)

# import crackers
from ama.core.plugins.cracker import (
    John,
    Hashcat,
)



#@with_default_category(Category.CORE)
class Core(CommandSet):
    """
    Core command set category
    """

    def __init__(self):
        super().__init__()

    def do_exit(self,  _: cmd2.Statement):
        """
        Exit ama-framework
        """
        return True

    def do_version(self, _: cmd2.Statement):
        """
        Print version of ama-framework
        """
        print(get_version())

    def do_banner(self, _: cmd2.Statement):
        """
        Print banner of ama-framework
        """

        print(Banner.random())

    hashes_parser = argparse.ArgumentParser()
    hashes_parser.add_argument('-c', '--cracker', choices=['jtr', 'hc'], required=True,
                               help="Password cracker")

    hashes_parser.add_argument('-s', '--sensitive', action='store_true',
                               help="Sensitive search")

    hashes_parser.add_argument('pattern',
                               help="Pattern to search")


    @with_argparser(hashes_parser)
    def do_hashes(self, args):
        """
        Search by valid hashes types
        """
        if args.cracker == "jtr":
            John.search_hash(args.pattern, sensitive=args.sensitive)
        else: # cracker == hc
            Hashcat.search_hash(args.pattern, sensitive=args.sensitive)
