#!/usr/bin/env python3
#
# ama-framework's database and home directory interactor
#
# date: mar 31 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
import argparse
# fineprint imports
from fineprint.status import (
    print_failure,
    print_status
)

#from ama.db import AmaDB
from ama.config import (
    init_ama_config,
    create_ama_home,
    AMA_HOME,
    USER_HOME)

from ama.amaconsole import main as amaconsole_main
from ama.core.files import Path

def init(args):
    base_path = USER_HOME
    create_ama_home(base_path)
    init_ama_config()
    # AmaDB.initDB(args.dbName, args.roleName)

# def reinit(args):
#     pass

# def delete(args):
#     pass
#     #AmaDB.deleteDB(args.dbName, args.roleName)


def ama_parser():
    """
    Parse amaconsole options and return the supplied arguments
    """

    ama_parser = argparse.ArgumentParser(prog='ama', description="Ama console")
    ama_subparser = ama_parser.add_subparsers()

    init_parser = ama_subparser.add_parser('init', description="Init ama database and home directory")
    db_parser = init_parser.add_argument_group("Database")
    db_parser.add_argument('-d','--db-name', dest="db_name", default='ama',
                            help="Database name")
    db_parser.add_argument('-u','--ama-user', dest="role_name", default='attacker',
                            help="User name")

    home_dir_parser = init_parser.add_argument_group("Home directory")
    home_dir_parser.add_argument('--base-path', dest="base_path", default=Path.home(),
                                 help="Base path of ama home directory")

    init_parser.set_defaults(func=init)

    # reinit_parser = ama_subparser.add_parser('reinit', description="Reinit ama database and home directory")
    # reinit_parser.set_defaults(func=reinit)

    # delete_parser = ama_subparser.add_parser('delete', description="Delete ama database and home directory")
    # delete_parser.set_defaults(func=delete)

    return ama_parser


def main():
    """
    Ama executable
    """
    #import pdb; pdb.set_trace()
    parser = ama_parser()
    try:
        args = parser.parse_args()
        if 'func' in args:
            args.func(args)
        else:
            amaconsole_main()

    except Exception as error:
        print_failure(error)
