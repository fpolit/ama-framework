#!/usr/bin/env python3
#
# PasswordCracker - main class to generate password crackers (john, hashcat, ...)
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from ..plugin import Plugin

class PasswordCracker(Plugin):
    """
        Password Cracker (hash and credential cracker) - Main Password Cracker class
    """
    # Supported crackers
    HASH_CRACKERS = ["john", "hashcat"]
    CREDENTIAL_CRACKERS = ["hydra"]

    def __init__(self, name, *, version=None, main_exec=None):
        super().__init__(name,
                         version = version,
                         main_exec = main_exec)

    @staticmethod
    def hash_status(query_hash: str, potfile: str = None):
        """
        Check the status (broken or not) of query hash or hashes file
        """
        pass # implement for each child class of PasswordCracker

    def pylist2bash(self, pylist:list):
        bash_array = '('
        for id_list, value in enumerate(pylist):
            if id_list == (len(pylist) - 1):
                bash_array += f"'{value}')"
            else:
                bash_array += f"'{value}' "
        return bash_array
