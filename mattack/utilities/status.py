#!/usr/bin/env python3

import argparse
import os
from .core import MaskAttack

from fineprint.status import print_successful, print_failure, print_status


def status(hash):
    """
        Check the status of a hash in the potfile of the supported crackers(jtr and hc) of mattack

        return: status of tha hash (False: uncracked, True: cracked) and the cracker that crack the hash otherwise return None
    """
    crackers = MaskAttack.crackers
    # staus of hash(False: no cracked)
    for cracker in crackers:
        if MaskAttack.statusHash(hash, cracker):
            return [True, cracker]
    return [False, None]

def main():
    parser = argparse.ArgumentParser(description="Check hash status - mattack utility", prog='mstatus')

    # check subparse
    parser.add_argument('hash', help='Hash (or hash file) to check status')
    # if --file is true, then the hash is a hash file (name of the file) otherwise is a simple hash
    parser.add_argument('--file', action='store_true', help='Allow supplied a hash file (check the status of all the hashes in the file)')

    pargs = parser.parse_args()

    if pargs.file and os.path.isfile(pargs.hash): # an hash file was supplied
        with open(pargs.hash, 'r') as hashfile:
            print_status("Status\tHash")
            while hash := hashfile.readline().rstrip():
                hashStatus, cracker = status(hash)
                if hashStatus:
                    print_successful(f"cracked ({cracker})\t{hash}")
                else:
                    print_failure(f"uncracked\t{hash}")

    else:   # pargs.hash is simply an hash
        hash = pargs.hash
        hashStatus, cracker = status(hash)
        if hashStatus:
            print_successful(f"cracked ({cracker})\t{hash}")
        else:
            print_failure(f"uncracked\t{hash}") 

    

    