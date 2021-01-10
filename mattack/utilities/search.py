#!/usr/bin/env python3

import argparse
from .core import MaskAttack

def main():
    parser = argparse.ArgumentParser(description="Search by a hash format given a pattern - mattack utility", prog='msearch')

    parser.add_argument('pattern', type=str, help='pattern to search hash format', default=None)
    #password_cracker = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('--jtr', action='store_true')
    parser.add_argument('--hc', action='store_true')
    parser.add_argument('-s', '--sensitive', action='store_true', help="Enable sensitive search")

    args = parser.parse_args()
    pattern = args.pattern
    jtr = args.jtr  # if True search a hash format for john the ripper
    hc = args.hc    # if True search a hash format for hashcat
    sensitive = args.sensitive
    
    MaskAttack.search(pattern, sensitive=sensitive, jtrFormats=jtr, hcFormats=hc)