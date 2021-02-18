#!/usr/bin/env python3
#
# ama subcommand - seach by valid hashes types given a pattern
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


# fineprint imports
from fineprint.status import print_status

# cliff imports
from cliff.command import Command

# import modules of core/crack
#from .cracker import PasswordCracker
#from .cracker import John
#from .cracker import Hashcat


class SearchHashes(Command):
    """
    Seach by valid hashes types given a pattern
    """
    def get_parser(self, prog_name):
        parser = super(SearchHashes, self).get_parser(prog_name)
        parser.add_argument('pattern', type=str,
                            help='pattern to search valid hashes types')

        parser.add_argument('-c', '--cracker', type=str, choices=["jtr", "hc"], #choices=PasswordCracker.crackers,
                            required=True, help="Password Cracker")

        parser.add_argument('-s', '--sensitive', action='store_true', help="Enable sensitive search")

        return parser

    def take_action(self, parsed_args):
        pattern = parsed_args.pattern
        cracker = parsed_args.cracker
        sensitive = parsed_args.sensitive

        if cracker in ["john", "jtr"]:
            #John.searchHash(pattern, sensitive=sensitive)
            print_status("jtr search")

        elif cracker in ["hashcat", "hc"]:
            print_status("hc search")
            #Hashcat.searchHash(pattern, sensitive=sensitive)

