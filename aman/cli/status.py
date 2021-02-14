#!/usr/bin/env python3
#
# hstatus utilities - check the status of a hash or an hash file
#
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse
from fineprint.status import print_successful, print_failure, print_status

#cracker module imports
from ..cracker.PasswordCracker import PasswordCracker

# utilitie module imports
from ..utilities.utilitiesExceptions import NoArgumentProvided

# base module imports
from ..base.FilePath import FilePath


def main():
    parser = argparse.ArgumentParser(description="Check hash status - hattack utility", prog='hstatus')

    # check subparse
    parser.add_argument('-qh', '--queryHash', type=str, default=None,
                        help='Hash to check status')
    # if --file is true, then the hash is a hash file (name of the file) otherwise is a simple hash
    parser.add_argument('-hf', '--hashesFile', type=str, default=None,
                        help='Allow supplied a hash file (check the status of all the hashes in the file)')

    pargs = parser.parse_args()

    if not (pargs.hashesFile or pargs.queryHash):
        raise NoArgumentProvided
    else:
        # if pargs.hashFile: # an hash file was supplied
        #     hashFilePath = FilePath(pargs.hashFile)
        #     with open(hashFilePath, 'r') as hashFile:
        #         while queryHash := hashFile.readline().rstrip():

        #             crackedHash = PasswordCracker.globalHashStatus(queryHash)

        #             if crackedHash:
        #                 cracker, crackedHashPot = crackedHash
        #                 if cracker in ["john", "jtr"]:
        #                     hashType, queryHash, password = crackedHashPot
        #                     print_successful(f"cracked ({cracker}: {hashType}\t{queryHash}\t{password})")
        #                 elif cracker in ["hashcat", "hc"]:
        #                     queryHash, password = crackedHashPot
        #                     print_successful(f"cracked ({cracker}: {queryHash}\t{password})")
        #             else:
        #                 print_failure(f"uncracked\t{queryHash}")


        # if pargs.queryHash:   # pargs.queryHash is simply an hash
        #     queryHash = pargs.queryHash
        #     crackedHash = PasswordCracker.globalHashStatus(queryHash)

        #     if crackedHash:
        #         cracker, crackedHashPot = crackedHash
        #         hashType, queryHash, password = crackedHashPot
        #         if cracker in ["john", "jtr"]:
        #             print_successful(f"cracked ({cracker}: {hashType}\t{queryHash}\t{password})")
        #         elif cracker in ["hashcat", "hc"]: # NO hashType in hashcat.pot file
        #             print_successful(f"cracked ({cracker}: {queryHash}\t{password})")
        #     else:
        #         print_failure(f"uncracked\t{queryHash}")

        hashesFile = pargs.hashesFile
        queryHash = pargs.queryHash

        if hashesFile:
            PasswordCracker.reportHashesFileStatus(hashesFile)

        elif queryHash:
            PasswordCracker.reportHashStatus(queryHash)
