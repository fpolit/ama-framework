#!/usr/bin/env python3
#
# Create a role, a database and necessary tables for ama-framework
#
# Date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


# getpass imports
from getpass import getpass

# sbash imports
from sbash import Bash

# fineprint imports
from fineprint.status import print_status
from fineprint.status import print_failure
from fineprint.status import print_successful

# random-password-generator imports
from password_generator import PasswordGenerator

# psycopg2 imports
import psycopg2



class AmaDB:
    def __init__(self, dbName="ama", roleName="attacker"):
        self.name = dbName
        self.role = roleName


    @staticmethod
    def initDBTables(dbName="ama", roleName="attacker"):
        password = getpass(prompt=f"Password of {roleName} role: ")
        dbCredential = {'host':'localhost', 'database': dbName, 'user': roleName, 'password': password}

        cmdsTables = (
            """
            CREATE TABLE IF NOT EXIST hashes (
            hash VARCHAR (100) UNIQUE NOT NULL,
            type VARCHAR (20),
            cracker VARCHAR (20) NOT NULL,
            password VARCHAR (32) NOT NULL
            )
            """,

            """
            CREATE TABLE IF NOT EXIST services (
            service VARCHAR (20) NOT NULL,
            target INET NOT NULL,
            user VARCHAR (20) NOT NULL,
            password VARCHAR (32) NOT NULL
            )
            """
        )

        conn = None
        try:
            conn = psycopg2.connect(**dbCredential)
            cur = conn.cursor()

            for cmd in cmdsTables:
                cur.execute(cmd)

            conn.commit()
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print_failure(error)


    @staticmethod
    def initDB(dbName="ama", roleName="attacker"):
        try:
            print_status(f"Creating {roleName} role")

            password = getpass(prompt=f"Password for {roleName} role (empty for ramdon generation): ")
            randomPasswd = False
            if not password:
                passwd = PasswordGenerator()
                passwd.minlen = 16
                passwd.maxlen = 16
                passwd.minnumbers = 2
                passwd.minschars = 3
                passwd.minuchars = 2

                password = passwd.generate()
                randomPasswd = True

            Bash.exec(f"psql -U postgres -c \"CREATE ROLE {roleName} WITH LOGIN CREATEDB PASSWORD '{password}'\"")
            print_successful(f"Role {roleName} has been created")
            if randomPasswd:
                print_successful(f"Password {roleName} role: {password}")

            print_status(f"Creating {dbName} database")
            Bash.exec(f"psql -U {roleName} -c \"CREATE DATABASE {dbName} OWNER {roleName}\"")
            print_successful("Database {dbName} has been created")



        except Exception as error:
            print_failure(error)

