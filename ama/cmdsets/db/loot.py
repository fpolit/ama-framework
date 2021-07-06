#!/usr/bin/env python3
#
# module command set for ama-framework (Databae Commands Category)
#
# implementation - date: Feb 18 2021
#
# debug - date: feb 27 2021
# debugged function: do_loot, loot_hashes ,loot_credentials
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import argparse
from tabulate import tabulate

# cmd2 imports
import cmd2
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)

# tuping imports
from typing import (
    Any,
    List,
)

# commandset categories
from ..category import CmdsetCategory as Category

# psycopg2 imports
import psycopg2

# cracker imports
#from ama.core.cracker.cracker import PasswordCracker

# fineprint imports
from fineprint import (
    print_failure,
    print_status,
    print_successful
)
from fineprint.color import ColorStr


@with_default_category(Category.DB)
class Loot(CommandSet):
    """
    Show loots (cracked hashes)
    """

    loot_parser = cmd2.Cmd2ArgumentParser()
    loot_subparser = loot_parser.add_subparsers(title='type', help='loot type')

    # debugged - date: Feb 27 2021
    @with_argparser(loot_parser)
    def do_loot(self, ns: argparse.Namespace):
        """
        Show loots
        """
        handler = ns.cmd2_handler.get()
        if handler is not None:
            handler(ns)
        else:
            #self._cmd.poutput("No loots type was supplied")
            print_failure("No loots type was supplied")
            self._cmd.do_help('loot')



    hashes_parser = cmd2.Cmd2ArgumentParser()
    db_interact_parser = hashes_parser.add_argument_group('Database Interaction')
    db_interact_parser.add_argument('-r', '--remove', type=str,
                                    help='Remove cracked hash from workspace')

    filterHashes_parser = hashes_parser.add_argument_group('Filters')
    filterHashes_parser.add_argument('-c', '--cracker', type=str,
                                     help="Hash Cracker")
    filterHashes_parser.add_argument('-m', dest='hashType',
                               help="hash type")

    # debugged - date: Apr 3 2021
    @cmd2.as_subcommand_to('loot', 'hashes', hashes_parser)
    def loot_hashes(self, args):
        """
        Interact with cracked hashes in a workspace
        """

        #import pdb; pdb.set_trace()
        cur = None

        try:
            db_conn = self._cmd.db_conn
            if db_conn is None:
                raise Exception("Database not connected")

            cur = db_conn.cursor()
            workspace = self._cmd.workspace
            # validate the argument columns to query for specific columns
            if args.remove:
                rhash = args.remove
                print_status(f"Removing {ColorStr(rhash).StyleBRIGHT} hash from {ColorStr(workspace).StyleBRIGHT} workspace")
                getAllCrackedHashes = (
                    f"""
                    SELECT hash
                    FROM hashes_{workspace}
                    """
                )

                remove_hash_sql = ""
                cur.execute(getAllCrackedHashes)
                for cracked_hash in cur.fetchall():
                    if rhash == cracked_hash[0]:
                        remove_hash_sql = (
                            f"""
                            DELETE FROM hashes_{workspace}
                            WHERE hash = %s;
                            """
                        )
                        break
                if remove_hash_sql:
                    cur.execute(remove_hash_sql, (rhash,))
                    db_conn.commit()
                    print_successful(f"Cracked hash {ColorStr(rhash).StyleBRIGHT} has been deleted from {ColorStr(workspace).StyleBRIGHT} workspace")

                else:
                    print_failure(f"No hash {ColorStr(rhash).StyleBRIGHT} in {ColorStr(workspace).StyleBRIGHT} workspace")

            else:
                queryHashes = (
                    f"""
                    SELECT hash, type, cracker, password
                    FROM hashes_{workspace}
                    """
                )

                where = []
                if args.cracker:
                    where.append(f"cracker ILIKE '%{args.cracker}%'")

                if args.hashType:
                    where.append(f"type ILIKE '%{args.hashType}%'")

                if where:
                    whereQuery = "WHERE"
                    for filterId, filterQuery in enumerate(where):
                        if not(filterId == 0):
                            whereQuery += f" AND {filterQuery}"
                        else:
                            whereQuery += f" {filterQuery}"

                    queryHashes += whereQuery

                cur.execute(queryHashes)

                hashesTableHeaders = ["Hash", "Type", "Password", "Cracker"]

                hashesTable = [crackedHash for crackedHash in cur.fetchall()]
                cur.close()

                print(tabulate(hashesTable, headers=hashesTableHeaders))

        except (Exception, psycopg2.DatabaseError) as error:
            #cmd2.Cmd.poutput(error)
            print_failure(error)

        finally:
            if cur is not None:
                cur.close()


    credentials_parser = cmd2.Cmd2ArgumentParser()
    filterCreds_parser = credentials_parser.add_argument_group('Filters')
    filterCreds_parser.add_argument('target', nargs='?', default=None,
                                    help="target IP or domain name")
    filterCreds_parser.add_argument('-s', '--services', nargs='+',
                                    help="target services")

    # debugged - date: Feb 27 2021
    @cmd2.as_subcommand_to('loot', 'credentials', credentials_parser)
    def loot_credentials(self, args):
        """
        Show loot of cracked credentials
        """

        #import pdb; pdb.set_trace()

        cur = None
        try:
            if self._cmd.db_conn is None:
                raise Exception("Database not connected")

            cur = self._cmd.db_conn.cursor()
            workspace = self._cmd.workspace
            # validate the argument columns to query for specific columns
            queryServices = \
                f"""
                SELECT service, target, service_user, password
                FROM services_{workspace}
                """

            where = []
            if args.services:
                for service in args.services:
                    where.append(f"service ILIKE '%{service}%'")

            # this core is odd (REWRITE PLEASE: Write a general class to made queries to ama database)
            # BEGIN oddy code
            whereQuery = ""
            if args.target:
                whereQuery += f"WHERE target LIKE '{args.target}'"

            if where:
                for filterId, filterQuery in enumerate(where):
                    if not(filterId == 0):
                        if filterId == (len(where) -1): #last conditional
                            whereQuery += f" OR {filterQuery})"
                        else:
                            whereQuery += f" OR {filterQuery}"
                    else:
                        if len(where) == 1:
                            if args.target:
                                whereQuery += f" AND {filterQuery}"
                            else:
                                whereQuery += f" WHERE {filterQuery}"
                        else:
                            if args.target:
                                whereQuery += f" AND ({filterQuery}"
                            else:
                                whereQuery += f" WHERE ({filterQuery}"


            queryServices += whereQuery
            # END oddy code

            cur.execute(queryServices)

            servicesTableHeaders = ["Service", "Target", "User", "Password"]
            servicesTable = [crackedService for crackedService in cur.fetchall()]
            cur.close()

            print(tabulate(servicesTable, headers=servicesTableHeaders))

        except (Exception, psycopg2.DatabaseError) as error:
            #cmd2.Cmd.poutput(error)
            print_failure(error)

        finally:
            if cur is not None:
                cur.close()
