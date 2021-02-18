#!/usr/bin/env python3
#
# hsearch -  hattack utility
#search by valids hash types in the hashes of supported crackers by PasswordCracker given a pattern
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import argparse

# cracker modules - import
from ..cracker.PasswordCracker import PasswordCracker
from ..cracker.John import John
from ..cracker.Hashcat import Hashcat

def main():
    parser = argparse.ArgumentParser(description="Search by a hash format given a pattern - mattack utility", prog='hsearch')

    parser.add_argument('pattern', type=str,
                        help='pattern to search hash format')

    parser.add_argument('-c', '--cracker', type=str, choices=PasswordCracker.crackers,
                                required=True, help="Password Cracker")

    parser.add_argument('-s', '--sensitive', action='store_true', help="Enable sensitive search")

    args = parser.parse_args()

    pattern = args.pattern
    cracker = args.cracker
    sensitive = args.sensitive

    if cracker in ["john", "jtr"]:
        John.searchHash(pattern, sensitive=sensitive)

    elif cracker in ["hashcat", "hc"]:
        Hashcat.searchHash(pattern, sensitive=sensitive)
