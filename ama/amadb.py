#!/usr/bin/env python3
#
# ama-framework's database interactor
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import argparse

# import ama version
#from ama.base.version import get_version

# ama.db imports
from ama.db import AmaDB



def amadbParser():
    """
    Parse amadb options and return the supplied arguments
    """

    amadb_parser = argparse.ArgumentParser(prog='amadb', description="Manage ama-framework database service")
    db_options = amadb_parser.add_argument_group("Database")
    db_options.add_argument('--ama-db-name', dest="dbName", default='amadb',
                            help="Database name")
    db_options.add_argument('--ama-role-name', dest="roleName", default='attacker',
                            help="Role name")

    amadb_subparser = amadb_parser.add_subparsers()

    init_parser = amadb_subparser.add_parser('init', description="init ama-framework database")
    init_parser.set_defaults(func=initDB)

    #reinit_parser = amadb_subparser.add_parser('reinit', description="reinit ama-framework database")
    #reinit_parser.set_defaults(func=reinitDB)

    delete_parser = amadb_subparser.add_parser('delete', description="delete ama-framework database")
    delete_parser.set_defaults(func=deleteDB)

    return amadb_parser.parse_args()


from fineprint.status import print_status

def initDB(args):
    print_status(f"Executing initDB({args})")
    AmaDB.initDB(args.dbName, args.roleName)

#def reinitDB(args):
#    print_status(f"Executing reinitDB({args})")

def deleteDB(args):
    print_status(f"Executing deleteDB({args})")
    AmaDB.deleteDB(args.dbName, args.roleName)


def main():
    """
    Execute the selected action from the parsed arguments
    """
    args = amadbParser()
    args.func(args)


if __name__=="__main__":
    main()
