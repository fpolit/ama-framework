#!/usr/bin/env python3
#
# database commands set from ama-framework (Database Commands Category)
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse
from argparse import RawTextHelpFormatter

# fineprint import
from fineprint.status import (
    print_status,
    print_failure
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

@with_default_category(Category.DB)
class Connection(CommandSet):
    """
    Database command set category related to database connection
    command sets: db_connect, db_disconnect, db_status
    """
    def __init__(self):
        super().__init__()


    db_connect_help = \
        """
        DB credential file

        connect_amadb.ini

        [postgresql]
        host = localhost
        database = ama
        user = attacker
        """
    db_connect_parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    db_connect_parser.add_argument('-c', '--creds',
                                   help=db_connect_help)

    @with_argparser(db_connect_parser)
    def do_db_connect(self, args):
        """
        Connect to ama-framework database
        """
        self._cmd.db_conn = None
        try:
            self._cmd.db_creds = Databasecmdset.dbCreds(args.creds)
            self._cmd.dbName = self._cmd.db_creds
            if  self._cmd.db_creds:
                self._cmd.db_conn =  psycopg2.connect(**self._cmd.db_creds)
                cmd2.Cmd.poutput(f"Connected to {self._cmd.dbName} database")
                del self._cmd.db_creds['password']

        except (Exception, psycopg2.DatabaseError) as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)


    def do_db_disconnect(self, args):
        """
        Disconnect ama-framework database
        """
        try:
            self._cmd.db_conn.close()
            self._cmd.db_conn = None
            cmd2.Cmd.poutput(f"Database {self._cmd.dbName} disconnected")
            del self._cmd.db_creds

        except (Exception, psycopg2.DatabaseError) as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)

    def do_db_status(self, args):
        """
        Report status of ama-framework database connection
        """
        if self._cmd.db_conn:
            dbName = self._cmd.dbName
            cmd2.Cmd.poutput(f"Connected to {dbName} database")
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
