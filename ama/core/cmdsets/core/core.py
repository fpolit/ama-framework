#!/usr/bin/env python3
#
# core commands set from ama-framework (Core Commands Category)
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse
import hashlib

# version import
from ama.core.version import get_version

#banner import
from ama.core.banner import Banner

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
import cmd2
from cmd2 import (
    Cmd,
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
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

from fineprint.status import print_status, print_successful


@with_default_category(Category.CORE)
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

    hashtype_parser = argparse.ArgumentParser()
    password_crackers = [John.MAINNAME, Hashcat.MAINNAME]
    hashtype_parser.add_argument('-c', '--cracker', choices=password_crackers, required=True,
                               help="Password cracker")

    hashtype_parser.add_argument('-s', '--sensitive', action='store_true',
                               help="Sensitive search")

    hashtype_parser.add_argument('pattern',
                               help="Pattern to search")
    @with_argparser(hashtype_parser)
    def do_hashtype(self, args):
        """
        Search by valid hashes types
        """
        if args.cracker == John.MAINNAME:
            John.search_hash(args.pattern, sensitive=args.sensitive)
        else: # cracker == hc
            Hashcat.search_hash(args.pattern, sensitive=args.sensitive)



    hashgen_parser = Cmd2ArgumentParser()
    hashgen_parser.add_argument('text', type=str,
                                help='Text to encrpt')
    hashgen_parser.add_argument('-t', '--type', dest='hash_type',
                                choices=hashlib.algorithms_available,
                                required=True, metavar='HASH_FUNCTION',
                                help="Hash Type")
    hashgen_parser.add_argument('-o', '--output', default=None, completer=Cmd.path_complete,
                                help='Output file')
    @with_argparser(hashgen_parser)
    def do_hashgen(self, args):
        """
        Hashes Generator
        """

        print_status(f"Generating a {args.hash_type} hash for '{args.text}'")

        hash_algorithm = hashlib.new(args.hash_type)
        hash_algorithm.update(bytes(args.text, 'utf-8'))

        generated_hash = hash_algorithm.hexdigest()
        print_successful(f"Generated hash: {generated_hash}")

        if args.output:
            with open(args.output, 'w') as output:
                output.write(f"{generated_hash}\n")

            print_successful(f"Hash was saved to {args.output} file")

