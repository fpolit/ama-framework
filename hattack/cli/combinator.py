#!/usr/bin/env python3

import sys
import argparse
from argparse import RawTextHelpFormatter

# utilities modules import
from ..utilities.combinator import Combinator
from ..utilities.version import get_version

def CombinatorCLIParser():
    VERSION = get_version()
    parser = argparse.ArgumentParser(description=f"Combinator hattack utilitie - {VERSION}", prog="hcombine",
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument('-w', '--wordlist', nargs='+',
                        help='wordlist to combine')

    parser.add_argument('-m', '--masksFiles', nargs='*',
                        help='masks file to combine')


    parser.add_argument('-o', '--output', required=True,
                        help='output file')

    helpAction = "Combination mode\n\n"
    helpAction += "# | action\n----------\n"
    for idAction, action in Combinator.actions.items():
        helpAction += f"{idAction} | {action}\n"

    parser.add_argument('-a', '--action', type=int, required=True,
                        help=helpAction)

    return parser



def main():
    parser = CombinatorCLIParser()
    args = parser.parse_args()

    wordlists = args.wordlist
    masksFile = args.masksFiles
    action = args.action
    output = args.output

    print(f"""
    wordlists  = {wordlists}
    masksFiles = {masksFile}
    action     = {action}
    output     = {output}
    """)

    # Combinator.selectAction(wordlists = wordlists,
    #                         masksFiles = masksFiles,
    #                         action = action,
    #                         output=output)
