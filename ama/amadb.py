#!/usr/bin/env python3
#
# manager interaction with ama database
#
# date: Apr 1  2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
import argparse
from fineprint.status import (
    print_failure,
    print_status
)

from ama.core.files import Path
from ama.core.plugins.cracker import (
    John,
    Hashcat,
    get_availables_crackers
)

def amadb_parser():
    amadb_parser = argparse.ArgumentParser(prog='amadb', description="Ama database manager")

    amadb_parser.add_argument('-c', '--creds', dest='creds_file', required=True, metavar="CREDENTIALS_FILE",
                              help='Ama database credentials file')
    amadb_parser.add_argument('-w', '--workspace', dest='workspace', required=True,
                              help='Ama workspace')

    available_crackers = get_availables_crackers()
    available_cracker_names = [cracker.MAINNAME for cracker in available_crackers]
    amadb_parser.add_argument('--cracker', required=True, choices=available_cracker_names,
                              help="Password Cracker")
    insert_parser = amadb_parser.add_mutually_exclusive_group(required=True)
    insert_parser.add_argument('-j', '--insert-hashes', dest='insert_hashes', metavar="HASHES_FILE",
                              help='Insert cracked hashes to ama database')
    insert_parser.add_argument('-s', '--insert-services', dest='insert_services', metavar="TARGET_SERVICE",
                              help='Insert cracked services to ama database')

    return amadb_parser

def main():
    try:
        parser = amadb_parser()
        args = parser.parse_args()
        workspace = args.workspace
        credentials_file = Path(args.creds_file)
        cracker = args.cracker
        if args.insert_hashes and cracker in [John.MAINNAME, Hashcat.MAINNAME]:
            hashes_file = Path(args.insert_hashes)
            if cracker == John.MAINNAME:
                John.insert_hashes_to_db(hashes_file, workspace, credentials_file)
            elif cracker == Hashcat.MAINNAME:
                Hashcat.insert_hashes_to_db(hashes_file, workspace, credentials_file)

        elif args.insert_hashes and cracker not in [John.MAINNAME, Hashcat.MAINNAME]:
            raise Exception(f"Cracker {args.cracker} doesn't crack hashes")

        if args.insert_services:
            print_status("Please, implement me")
            #services_file = Path(args.insert_hashes)


    except Exception as error:
        print_failure(error)
