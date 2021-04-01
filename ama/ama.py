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

from ama.db import AmaDB
from ama.config import create_ama_home, AMA_HOME
from ama.amaconsole import main as amaconsoleMain
from ama.core.files import Path

def init(args):
    base_path = Path(args.base_path)
    create_ama_home(base_path)
    AmaDB.initDB(args.dbName, args.roleName)

def reinit(args):
    pass

def delete(args):
    AmaDB.deleteDB(args.dbName, args.roleName)


def amaConsoleParser():
    """
    Parse amaconsole options and return the supplied arguments
    """

    amaconsole_parser = argparse.ArgumentParser(prog='ama', description="Ama console")
    db_parser = amaconsole_parser.add_argument_group("Database")
    db_parser.add_argument('--ama-db', dest="dbName", default='ama',
                            help="Database name")
    db_parser.add_argument('--ama-role', dest="roleName", default='attacker',
                            help="Role name")

    home_dir_parser = amaconsole_parser.add_argument_group("Home directory")
    home_dir_parser.add_argument('--base-path', dest="base_path", default=Path.home(),
                                 help="Base path of ama home directory")

    amaconsole_subparser = amaconsole_parser.add_subparsers()

    init_parser = amaconsole_subparser.add_parser('init', description="Init ama database and home directory")
    init_parser.add_argument('-f', '--force', action='store_true',
                             help='Force init (overwrite database and home directory)')
    init_parser.set_defaults(func=init)

    reinit_parser = amaconsole_subparser.add_parser('reinit', description="Reinit ama database and home directory")
    reinit_parser.set_defaults(func=reinit)

    delete_parser = amaconsole_subparser.add_parser('delete', description="Delete ama database and home directory")
    delete_parser.set_defaults(func=delete)

    return amaconsole_parser


def main():
    """
    Execute the selected action from the parsed arguments
    """
    #import pdb; pdb.set_trace()
    amaconsole_parser = amaConsoleParser()
    try:
        args = amaconsole_parser.parse_args()
        if 'func' in args:
            args.func(args)
        else:
            amaconsoleMain()

    except Exception as error:
        print_failure(error)
        #amaconsole_parser.print_help()


#if __name__=="__main__":
#    main()
