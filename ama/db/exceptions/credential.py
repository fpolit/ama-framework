#!/usr/bin/env python3
#
# Database Exception to manage credential errors generated in interelations with ama-framework db
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from psycopg2 import DatabaseError

class InvalidCredentialError(DatabaseError):
    """
    Error related to invalid credentials to connect to db
    """
    def __init__(self, creds):
        self.dbCreds = creds
        self.warning = "Invalid Creadentials:\n"

        for credKey, credValue in creds:
            self.warning += f"{credKey}: {credValue}, "

        super().__init__(self.warning)
