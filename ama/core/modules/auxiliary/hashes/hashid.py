#!/usr/bin/env python3
#
# hash identifier - hashID
#
# date: Feb 23 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os

# cmd2 imports
import cm2
# typing import
from typing import List

# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

# hashid imports
from ama.core.auxiliary.hashes.hashid import (
    HashID,
    getHashIDBanner
)

# validator imports
from ama.core.validator import Args
from ama.core.files import Path


class HashID(Auxiliary):
    """
    hash identifier - hashID
    """
    description = "hash identifier - hashID"
    mname = "auxiliary/hashes/hashid"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    fulldescription = (
        """
        Identify the different types of hashes used to encrypt data
        and return valid Hashcat or John hashes types
        """
    )

    def __init__(self, *,
                 queryHash: str = None, hashesFile: str = None, output: str = None,
                 extended: bool = False, hashcat: bool = True, john: bool = True):
        self.banner = getHashIDBanner()

        auxiliaryOptions = {
            'query_hash': Argument(queryHash, True, "Hash to identify"),
            'hashes_file': Argument(hashesFile, False, "Hashes file ot identify"),
            'output': Argument(output, False, "Output File"),
            'extended': Argument(extended, False, "List all possible hash algorithms including salted passwords"),
            'hashcat': Argument(hashcat, False, "Show corresponding Hashcat mode in output"),
            'john': Argument(john, False, "Show corresponding JohnTheRipper hash format in output")
        }

        initOptions = {
            'mname': mname,
            'author': author,
            'description': description,
            'fulldescription':  fulldescription,
            'auxiliaryOptions': auxiliaryOptions,
        }

        super().__init__(**initOptions)

    def run(self):
        # check that required arguments aren't None
        for option in self.auxiliary.values():
            if option.required:
                Args.notNone(option.value)

        output = self.auxiliary['output'].value
        if output:
            permission = [os.R_OK]
            Path.access(permission, output)

        else:
            pass




# def main():
#     usage = "{0} [-h] [-e] [-m] [-j] [-o FILE] [--version] INPUT".format(os.path.basename(__file__))

#     parser = argparse.ArgumentParser(
#         description="Identify the different types of hashes used to encrypt data",
#         usage=usage,
#         epilog=__license__,
#         add_help=False,
#         formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=27)
#     )
#     # parser.add_argument("strings",
#     #                     metavar="INPUT", type=str, nargs="*",
#     #                     help="input to analyze (default: STDIN)")
#     # group = parser.add_argument_group('options')
#     # group.add_argument("-e", "--extended",
#     #                    action="store_true",
#     #                    help="list all possible hash algorithms including salted passwords")
#     # group.add_argument("-m", "--mode",
#     #                    action="store_true",
#     #                    help="show corresponding Hashcat mode in output")
#     # group.add_argument("-j", "--john",
#     #                    action="store_true",
#     #                    help="show corresponding JohnTheRipper format in output")
#     # group.add_argument("-o", "--outfile",
#     #                    metavar="FILE", type=str,
#     #                    help="write output to file")
#     # group.add_argument("-h", "--help",
#     #                    action="help",
#     #                    help="show this help message and exit")
#     # group.add_argument("--version",
#     #                    action="version",
#     #                    version=__banner__)
#     # args = parser.parse_args()

#     hashID = HashID()

#     if not args.outfile:
#         outfile = sys.stdout
#     else:
#         try:
#             outfile = io.open(args.outfile, "w", encoding="utf-8")
#         except EnvironmentError:
#             parser.error("Could not open {0}".format(args.output))

#     if not args.strings or args.strings[0] == "-":
#         while True:
#             line = sys.stdin.readline()
#             if not line:
#                 break
#             outfile.write(u"Analyzing '{0}'\n".format(line.strip()))
#             writeResult(hashID.identifyHash(line), outfile, args.mode, args.john, args.extended)
#             sys.stdout.flush()
#     else:
#         for string in args.strings:
#             if os.path.isfile(string):
#                 try:
#                     with io.open(string, "r", encoding="utf-8") as infile:
#                         outfile.write("--File '{0}'--\n".format(string))
#                         for line in infile:
#                             if line.strip():
#                                 outfile.write(u"Analyzing '{0}'\n".format(line.strip()))
#                                 writeResult(hashID.identifyHash(line), outfile, args.mode, args.john, args.extended)
#                 except (EnvironmentError, UnicodeDecodeError):
#                     outfile.write("--File '{0}' - could not open--".format(string))
#                 else:
#                     outfile.write("--End of file '{0}'--".format(string))
#             else:
#                 outfile.write(u"Analyzing '{0}'\n".format(string.strip()))
#                 writeResult(hashID.identifyHash(string), outfile, args.mode, args.john, args.extended)
