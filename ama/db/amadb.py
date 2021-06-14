#!/usr/bin/env python3
#
# Create a role, a database and necessary tables for ama-framework
#
# Date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
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
    def init_db(db_name="ama", role_name="attacker"):
        """
        Database initialization
        (creation of database, role, and initialization of default workspace)
        """

        conn = None
        try:
            print_status(f"Creating role:  {ColorStr(role_name).StyleBRIGHT}")

            password = getpass(prompt=f"Password for {ColorStr(role_name).StyleBRIGHT} role (empty for random generation): ")
            if not password:
                passwd = PasswordGenerator()
                passwd.minlen = 16
                passwd.maxlen = 16
                passwd.minnumbers = 2
                passwd.minschars = 3
                passwd.minuchars = 2

                password = passwd.generate()

            Bash.exec(f"psql -U postgres -c \"CREATE ROLE {role_name} WITH LOGIN CREATEDB PASSWORD '{password}'\"", quiet=True)
            Bash.exec(f"psql -U postgres -c \"CREATE DATABASE {role_name} OWNER {role_name}\"", quiet=True)
            print_successful(f"Role {ColorStr(role_name).StyleBRIGHT} has been created")

            print_status(f"Creating {ColorStr(dbName).StyleBRIGHT} database")
            Bash.exec(f"psql -U {role_name} -c \"CREATE DATABASE {db_name} OWNER {role_name}\"", quiet=True)
            print_successful("Database {db_name} has been created")

            # creation workspaces table
            db_creds = {'host':'localhost', 'database': db_name, 'user': role_name, 'password': password}
            workspace = "default"

            tables_creation = (
                """
                CREATE TABLE IF NOT EXISTS workspaces (
                name VARCHAR (100) NOT NULL PRIMARY KEY
                )
                """,

                f"""
                CREATE TABLE IF NOT EXISTS {workspace}_hashes (
                hash TEXT NOT NULL PRIMARY KEY,
                password TEXT NOT NULL,
                salt TEXT,
                algorithm TEXT NOT NULL,
                status int NOT NULL,
                cracker VARCHAR (20) NOT NULL,
                FOREIGN KEY (status) REFERENCES status (id)
                )
                """,

                """
                CREATE TABLE IF NOT EXISTS status (
                id int NOT NULL PRIMARY KEY,
                description VARCHAR(10) NOT NULL
                )
                """,

                # f"""
                # CREATE TABLE IF NOT EXISTS {workspace}_services (
                # service VARCHAR (20) NOT NULL,
                # target VARCHAR (15) NOT NULL,
                # service_user VARCHAR (20) NOT NULL,
                # password VARCHAR (32) NOT NULL
                # )
                # """
            )

            workspace_insert = (
                """
                INSERT INTO workspaces (name)
                VALUES (%s);
                """
            )

            conn = psycopg2.connect(**db_creds)
            cur = conn.cursor()

            # table creation
            for cmd in tables_creation:
                cur.execute(cmd)
            conn.commit()

            # default workspace insertion
            cur.execute(workspace_insert, (workspace ,))
            conn.commit()
            cur.close()
            print_successful(f"Database {ColorStr(dbName).StyleBRIGHT} has been created")

            #import pdb; pdb.set_trace()
            # writing credential to AMA_HOME/db/database.json file
            database_json_file = Path.joinpath(AMA_HOME, 'db/database.json')
            with open(database_json_file, 'w') as db_credentials:
                json.dump(db_creds, db_credentials, indent=4)

            print_successful(f"Database credential file has been created: {ColorStr(database_json_file).StyleBRIGHT}")
            del db_creds

        except (Exception, psycopg2.DatabaseError) as error:
            print_failure(error)

        finally:
            if conn is not None:
                conn.close()


    # @staticmethod
    # def deleteDB(dbName=None, roleName=None):
    #     """
    #     Delete ama-framework database
    #     """
    #     if dbName:
    #         if Answer.shortAnwser(f"Do you really want to delete the {ColorStr(dbName).StyleBRIGHT} database(y/n)? "):
    #             if roleName:
    #                 Bash.exec(f"psql -U {roleName} -c \"DROP DATABASE {dbName}\"")
    #             else:
    #                 Bash.exec(f"psql -U postgres -c \"DROP DATABASE {dbName}\"")

    #         else:
    #             #cmd2.Cmd.pwarning("Be carefully you could lose your data")
    #             print_failure("Be carefully you could lose your data")
    #     else:
    #         #cmd2.Cmd.pwarning("No database was selected to delete")
    #         print_failure("No database was selected to delete")


    def insert2db(hashes_file: Path, potfile: Path, workspace: str, db_creds):
        """
        Insert hashes in hashes_file that are in potfile to workspace's hashes table
        """
        pass
        # cur = db_conn = None
        # try:
        #     #import pdb;pdb.set_trace()
        #     hashes_status = Hashcat.hashes_file_status(hashes_file)
        #     cracked_hashes = hashes_status['cracked']

        #     db_credentials = Connection.dbCreds(creds_file)
        #     db_conn = psycopg2.connect(**db_credentials)

        #     cur = db_conn.cursor()
        #     cur.execute(f"SELECT hash from hashes_{workspace}")
        #     cracked_hashes_db = cur.fetchall()
        #     new_cracked_hashes = []  #only non-repeated cracked hashes
        #     for cracked_hash in cracked_hashes: # cracked_hash = (hash, type, cracked, password)
        #         repeated = False
        #         for cracked_hash_db in cracked_hashes_db: # cracked_hash_db = (cracked_hash)
        #             if cracked_hash[0] == cracked_hash_db[0]:
        #                 repeated = True
        #                 break

        #         if not repeated:
        #             new_cracked_hashes.append(cracked_hash)

        #     if new_cracked_hashes:
        #         insert_cracked_hash = (
        #             f"""
        #             INSERT INTO hashes_{workspace} (hash, type, cracker, password)
        #             VALUES (%s, %s, %s, %s)
        #             """
        #         )

        #         cur.executemany(insert_cracked_hash, cracked_hashes)
        #         print_successful(f"Cracked hashes were saved to {ColorStr(workspace).StyleBRIGHT} workspace")

        #     else:
        #         print_status(f"No new cracked hashes to save to {ColorStr(workspace).StyleBRIGHT} workspace")

        #     db_conn.commit()
        #     cur.close()

        # except Exception as error:
        #     print_failure(error)

        # finally:
        #     if cur is not None:
        #         cur.close()

        #     if db_conn is not None:
        #         db_conn.close()
