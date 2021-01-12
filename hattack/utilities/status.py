#!/usr/bin/env python3

# hstatus utilities - check the status of a hash or an hash file
#
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse
from fineprint.status import print_successful, print_failure, print_status

#cracker module imports
from ..cracker.PasswordCracker import PasswordCracker

# utilitie module imports
from .utilitiesExceptions import NoArgumentProvided

# base module imports
from ..base.FilePath import FilePath

def main():
    parser = argparse.ArgumentParser(description="Check hash status - hattack utility", prog='hstatus')

    # check subparse
    parser.add_argument('-qh', '--queryHash', type=str,
                        help='Hash (or hash file) to check status')
    # if --file is true, then the hash is a hash file (name of the file) otherwise is a simple hash
    parser.add_argument('-hf', '--hashFile', type=str,
                        help='Allow supplied a hash file (check the status of all the hashes in the file)')

    pargs = parser.parse_args()

    if not (pargs.hashFile or pargs.queryHash):
        raise NoArgumentProvided
    else:
        if pargs.hashFile: # an hash file was supplied
            hashFilePath = FilePath(pargs.hashFile)
            with open(hashFilePath, 'r') as hashFile:
                while queryHash := hashFile.readline().rstrip():
                    hashStatus, cracker = PasswordCracker.globalHashStatus(queryHash)

                    if hashStatus: # hashStatus = True (is cracked)
                        print_successful(f"cracked ({cracker})\t{queryHash}")
                    else: # hashStatus = False (not cracked yet)
                        print_failure(f"uncracked\t{queryHash}")

        if pargs.queryHash:   # pargs.queryHash is simply an hash
            queryHash = pargs.queryHash
            hashStatus, cracker = PasswordCracker.globalHashStatus(queryHash)

            if hashStatus:
                print_successful(f"cracked ({cracker})\t{queryHash}")
            else:
                print_failure(f"uncracked\t{queryHash}")
