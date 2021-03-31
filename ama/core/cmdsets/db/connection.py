#!/usr/bin/env python3
#
# database commands set from ama-framework (Database Commands Category)
#
#
# implementation - date: Feb 20 2021
#
# implemented classes: Connection
# implemented Exception classes: NoDatabaseCredentialsSupplied, InvalidFormatDatabaseCredential
#
# debug - date: Feb 27 2021
#
# debugged functions: do_db_connect, do_db_status, do_db_disconnect, dbCreds
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import re
import argparse
from argparse import RawTextHelpFormatter

# fineprint import
from fineprint.status import (
    print_status,
    print_failure,
    print_successful
)

# import db connection modules
from configparser import ConfigParser
from getpass import getpass
import psycopg2

# version import
from ...version import get_version

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
import cmd2
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)


class NoDatabaseCredentialsSupplied(Exception):
    """
    Exception to catch error when no database credential supplied
    """

    def __init__(self):
        self.warning = "No database credential supplied"
        super().__init__(self.warning)


class InvalidFormatDatabaseCredential(Exception):
    """
    Exception to catch error when
    supplied database credentials are in an invalid format
    """
    def __init__(self, invalidCredentials):
        self.warning = f"Invalid credentials: {invalidCredentials}"
        super().__init__(self.warning)


@with_default_category(Category.DB)
class Connection(CommandSet):
    """
    Database command set category related to database connection
    command sets: db_connect, db_disconnect, db_status
    """
    def __init__(self):
        super().__init__()

    db_connect_parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    db_connect_parser.add_argument('-c', '--creds',
                                   help="Postgres database credential file")
                                   #help=db_connect_help)

    db_connect_parser.add_argument('credentials', nargs='?', default=None,
                                   help="Postgres database credentials (format: <user>@<host>/<database>)")

    @with_argparser(db_connect_parser)
    def do_db_connect(self, args):
        """
        Connect to database
        """
        #import pdb; pdb.set_trace()
        self._cmd.db_conn = None
        try:
            if args.credentials:
                credentialParser = re.compile(r"([\W|\w]*)@([\W|\w]*)/([\W|\w]*)")
                if credentials := credentialParser.fullmatch(args.credentials):
                    user, host, database = credentials.groups()
                    self._cmd.db_creds = {'host': host, 'database': database, 'user': user}
                    password = getpass(prompt=f"Password {user} role: ")
                    self._cmd.db_creds['password'] = password
                else:
                    raise InvalidFormatDatabaseCredential(args.credentials)

            elif args.creds:
                self._cmd.db_creds = Connection.dbCreds(args.creds)

            else: # no database credential supplied
                raise NoDatabaseCredentialsSupplied


            if  self._cmd.db_creds:
                self._cmd.db_conn =  psycopg2.connect(**self._cmd.db_creds)
                dbName = self._cmd.db_creds['database']
                #cmd2.Cmd.poutput(f"Connected to {dbName} database")
                print_successful(f"Connected to {dbName} database")
                del self._cmd.db_creds['password']

        except (Exception, psycopg2.DatabaseError) as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)


    def do_db_disconnect(self, args):
        """
        Disconnect database
        """
        try:
            self._cmd.db_conn.close()
            self._cmd.db_conn = None
            dbName = self._cmd.db_creds['database']
            #cmd2.Cmd.poutput(f"Database {dbName} disconnected")
            print_status(f"Database {dbName} disconnected")
            del self._cmd.db_creds

        except (Exception, psycopg2.DatabaseError) as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)

    def do_db_status(self, args):
        """
        Report status of database connection
        """
        if self._cmd.db_conn:
            dbName = self._cmd.db_creds['database']
            #cmd2.Cmd.poutput(f"Connected to {dbName} database")
            print_successful(f"Connected to {dbName} database")
        else:
            #cmd2.Cmd.poutput(f"Database not connected")
            print_failure(f"Database not connected")

    @staticmethod
    def dbCreds(dbconfig, section='postgresql'):
        db_parser = ConfigParser()
        db_parser.read(dbconfig)

        db_creds = {}

        if db_parser.has_section(section):
            params = db_parser.items(section)
            for key, value in params:
                db_creds[key] = value
            password = getpass("Password: ")
            db_creds['password'] = password

        else:
            #cmd2.Cmd.pwarning(f"Section {section} not found in {dbconfig} file")
            print_failure(f"Section {section} not found in {dbconfig} file")

        return db_creds
