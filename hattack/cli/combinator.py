#!/usr/bin/env python3

import sys
import argparse
from argparse import RawTextHelpFormatter
from tabulate import tabulate

# utilities modules import
from ..utilities.combinator import Combinator
from ..utilities.version import get_version

def CombinatorCLIParser():
    VERSION = get_version()
    parser = argparse.ArgumentParser(description=f"Combinator (hattack utility) - {VERSION}", prog="hcombine",
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument('-w', '--wordlist', nargs='+',
                        help='wordlist to combine')

    parser.add_argument('-mf', '--masksFiles', nargs='*',
                        help='masks file to combine')

    parser.add_argument('-m', '--mask', type=str,
                        help='mask to combine')

    parser.add_argument('-o', '--output', required=True,
                        help='output file')

    helpAction = tabulate(Combinator.actions.items(), headers=["#", "action"])

    parser.add_argument('-a', '--action', type=int, required=True,
                        help=helpAction)

    return parser



def main():
    parser = CombinatorCLIParser()
    args = parser.parse_args()

    wordlists = args.wordlist
    masksFiles = args.masksFiles
    mask = args.mask
    action = args.action
    output = args.output

    print(f"""
    wordlists  = {wordlists}
    masksFiles = {masksFiles}
    mask       = {mask}
    action     = {action}
    output     = {output}
    """)

    Combinator.selectAction(wordlists  = wordlists,
                            masksFiles = masksFiles,
                            mask       = mask,
                            action     = action,
                            output     = output)
