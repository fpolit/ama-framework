#!/usr/bin/env python3
#
# Create a role, a database and necessary tables for ama-framework
#
# Date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import json

# cmd2 imports
import cmd2

# getpass imports
from getpass import getpass

# sbash imports
from sbash import Bash

# fineprint imports
from fineprint.status import (
    print_status,
    print_failure,
    print_successful
)
from fineprint.color import ColorStr

# random-password-generator imports
from password_generator import PasswordGenerator

# psycopg2 imports
import psycopg2

# core/validator imports
from ama.core.validator import Answer

from ama.config import AMA_HOME
from ama.core.files import Path
#from ama.core.modules.auxiliary.hashes.hashes_status import HashesStatus


class AmaDB:
    @staticmethod
    def initDB(dbName="ama", roleName="attacker"):
        """
        Database initialization
        (creation of database, role, and initialization of default workspace)
        """
        try:
            #cmd2.Cmd.poutput(f"Creating {roleName} role")
            print_status(f"Creating role:  {ColorStr(roleName).StyleBRIGHT}")

            password = getpass(prompt=f"Password for {ColorStr(roleName).StyleBRIGHT} role (empty for random generation): ")
            if not password:
                passwd = PasswordGenerator()
                passwd.minlen = 16
                passwd.maxlen = 16
                passwd.minnumbers = 2
                passwd.minschars = 3
                passwd.minuchars = 2

                password = passwd.generate()

            Bash.exec(f"psql -U postgres -c \"CREATE ROLE {roleName} WITH LOGIN CREATEDB PASSWORD '{password}'\"", quiet=True)
            Bash.exec(f"psql -U postgres -c \"CREATE DATABASE {roleName} OWNER {roleName}\"", quiet=True)
            #cmd2.Cmd.poutput(f"Role {roleName} has been created")
            print_successful(f"Role {ColorStr(roleName).StyleBRIGHT} has been created")

            #cmd2.Cmd.poutput(f"Creating {dbName} database")
            print_status(f"Creating {ColorStr(dbName).StyleBRIGHT} database")
            Bash.exec(f"psql -U {roleName} -c \"CREATE DATABASE {dbName} OWNER {roleName}\"", quiet=True)
            #cmd2.Cmd.poutput("Database {dbName} has been created")

            # creation workspaces table
            dbCredential = {'host':'localhost', 'database': dbName, 'user': roleName, 'password': password}
            workspace = "default"

            tablesCreation = (
                """
                CREATE TABLE IF NOT EXISTS workspaces (
                name VARCHAR (100) UNIQUE NOT NULL
                )
                """,

                f"""
                CREATE TABLE IF NOT EXISTS hashes_{workspace} (
                hash VARCHAR (128) UNIQUE NOT NULL,
                type VARCHAR (20),
                cracker VARCHAR (20) NOT NULL,
                password VARCHAR (32) NOT NULL
                )
                """,

                f"""
                CREATE TABLE IF NOT EXISTS services_{workspace} (
                service VARCHAR (20) NOT NULL,
                target VARCHAR (15) NOT NULL,
                service_user VARCHAR (20) NOT NULL,
                password VARCHAR (32) NOT NULL
                )
                """
            )

            valueInsert = (
                """
                INSERT INTO workspaces (name)
                VALUES (%s);
                """
            )

            conn = None
            conn = psycopg2.connect(**dbCredential)
            cur = conn.cursor()
            # workspace table creation and
            # hashes and services tables creation for "default" workspace
            for cmdTable in tablesCreation:
                cur.execute(cmdTable)
            conn.commit()
            # default workspace insertion
            cur.execute(valueInsert, (workspace ,))
            conn.commit()
            cur.close()
            print_successful(f"Database {ColorStr(dbName).StyleBRIGHT} has been created")

            #import pdb; pdb.set_trace()
            # writing credential to AMA_HOME/db/database.json file
            database_json_file = Path.joinpath(AMA_HOME, 'db/database.json')
            with open(database_json_file, 'w') as db_credentials:
                json.dump(dbCredential, db_credentials, indent=4)

            print_successful(f"Database credential file has been created: {database_json_file}")
            del dbCredential

        except (Exception, psycopg2.DatabaseError) as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)


    @staticmethod
    def deleteDB(dbName=None, roleName=None):
        """
        Delete ama-framework database
        """
        if dbName:
            if Answer.shortAnwser(f"Do you really want to delete the {ColorStr(dbName).StyleBRIGHT} database(y/n)? "):
                if roleName:
                    Bash.exec(f"psql -U {roleName} -c \"DROP DATABASE {dbName}\"")
                else:
                    Bash.exec(f"psql -U postgres -c \"DROP DATABASE {dbName}\"")

            else:
                #cmd2.Cmd.pwarning("Be carefully you could lose your data")
                print_failure("Be carefully you could lose your data")
        else:
            #cmd2.Cmd.pwarning("No database was selected to delete")
            print_failure("No database was selected to delete")
