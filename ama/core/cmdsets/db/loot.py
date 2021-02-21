#!/usr/bin/env python3
#
# module command set for ama-framework (Databae Commands Category)
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import argparse

# cmd2 imports
import cmd2
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)

# table formation imports
import cmd2.table_creator import (
    Column,
    SimpleTable,
    HorizontalAligment
)
from cmd2 import ansi
from typing import (
    Any,
    List,
)

# commandset categories
from ..category import CmdsetCategory as Category

# psycopg2 imports
import psycopg2

# cracker imports
from ...modules.cracker import PasswordCracker


@with_default_category(Category.DB)
class Loot(CommandSet):
    """
    Show loots (cracked hashes)
    """

    loot_parser = cmd2.Cmd2ArgumentParser()
    loot_subparser = loot_parser.add_subparsers(title='type', help='loots type')

    @with_argparser(loot_parser)
    def do_loot(self, ns: argparse.Namespace):
        """
        Select the type of loot to show
        """
        handler = ns.cmd2_handler_get()
        if handler is not None:
            handler(ns)
        else:
            self._cmd.poutput("No loots type was supplied ")
            self.do_help('loot')



    hashes_parser = cmd2.Cmd2ArgumentParser()
    hashes_parser.add_argument('-cr', '--cracker', type=str, default=None,
                                 choices=PasswordCracker.hashCrackers, help="Hash Cracker")
    hashes_parser.add_argument('-m', dest='hashType', default=None,
                               help="hash type")

    hashes_parser.add_argument('-c', '--columns' , default=None,
                               help="hash type")

    @cmd2.as_subcommand_to('cut', 'hashes', hashes_parser)
    def loot_hashes(self, args):
        """
        Show loot of cracked hashes
        """

        try:
            cur = self._cmd.db_conn.cursor()
            workspace = self._cmd.workspace
            # validate the argument columns to query for specific columns
            queryHashes = \
                f"""
                SELETECT *
                FROM hashes_{workspace}
                """

            whereQuery = "WHERE"
            if args.cracker:
                whereQuery += f" cracker = '{args.cracker}' "

            if arg.hashType:
                whereQuery += f" AND type = '{args.hashType}'"

            queryHashes += whereQuery

            cur.execute(queryHashes)

            tableColumns: List[Column] = list()
            tableColumns.append(Column("Hash"))
            tableColumns.append(Column("Type"))
            tableColumns.append(Column("Cracker"))
            tableColumns.append(Column("Password"))

            hashesTableFormat = SimpleTable(tableColumns)
            hashesTable = hashesTableFormat.generate_table(cur.fetchall())
            cur.close()
            Loot.ansi_print(hashesTable)

        except (Exception, psycopg2.DatabaseError) as error:
            cmd2.Cmd.poutput(error)

    @staticmethod
    def ansi_print(table):
        ansi.allow_style = ansi.STYLE_TERMINAL
        ansi.style_aware_write(sys.stdout, table + "\n\n")


    credentials_parser = cmd2.Cmd2ArgumentParser()
    credentials_parser.add_argument('target',
                                    help="target IP or domainame")
    credentials_parser.add_argument('-s', '--services', nargs='+',
                                    help="target services")

    credentials_parser.add_argument('-c', '--columns' , default=None,
                                    help="hash type")

    @cmd2.as_subcommand_to('loot', 'credentials', credentials_parser)
    def loot_credentials(self, args):
        """
        Show loot of cracked credentials
        """
        try:
            cur = self._cmd.db_conn.cursor()
            workspace = self._cmd.workspace
            # validate the argument columns to query for specific columns
            queryServices = \
                f"""
                SELETECT *
                FROM services_{workspace}
                """

            whereQuery = "WHERE"
            for service in  args.services:
                whereQuery += f" service = '{args.service}' AND"

            if arg.target:
                whereQuery += f" target = '{args.target}'"

            queryServices += whereQuery

            cur.execute(queryHashes)

            tableColumns: List[Column] = list()
            tableColumns.append(Column("Service"))
            tableColumns.append(Column("Target"))
            tableColumns.append(Column("User"))
            tableColumns.append(Column("Password"))

            servicesTableFormat = SimpleTable(tableColumns)
            servicesTable = servicesTableFormat.generate_table(cur.fetchall())
            cur.close()
            Loot.ansi_print(servicesTable)

        except (Exception, psycopg2.DatabaseError) as error:
            cmd2.Cmd.poutput(error)
