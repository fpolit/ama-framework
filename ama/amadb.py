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
from ama.db.interaction import (
    insert_hashes
)


def amadb_parser():
    amadb_parser = argparse.ArgumentParser(prog='amadb', description="Ama database manager")

    amadb_parser.add_argument('-c', '--creds', dest='creds_file', required=True, metavar="CREDENTIALS_FILE",
                              help='Ama database credentials file')
    amadb_parser.add_argument('-w', '--workspace', dest='workspace', required=True,
                              help='Ama workspace')

    insert_parser = amadb_parser.add_mutually_exclusive_group(required=True)
    insert_parser.add_argument('-j', '--insert-hashes', dest='insert_hashes', metavar="HASHES_FILE",
                              help='Insert cracked hashes to ama database')
    insert_parser.add_argument('-s', '--insert-services', dest='insert_services',
                              help='Insert cracked services to ama database')

    return amadb_parser

def main():
    try:
        parser = amadb_parser()
        args = parser.parse_args()
        workspace = args.workspace
        credentials_file = Path(args.creds_file)
        if args.insert_hashes:
            hashes_file = Path(args.insert_hashes)
            insert_hashes(hashes_file, workspace, credentials_file)

        if args.insert_services:
            pass
            #services_file = Path(args.insert_hashes)


    except Exception as error:
        print_failure(error)
