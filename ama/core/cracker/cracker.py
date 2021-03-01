#!/usr/bin/env python3
#
# PasswordCracker - main class to generate password crackers (john, hashcat, ...)
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import re
import os
from tabulate import tabulate


# typing import
from typing import List

# fineprint imports
from fineprint.status import (
    print_failure
)

# importing PasswordCracker exceptions
from .crackerException import (
    CrackerExecNotFound,
    InvalidCracker,
    NotSupportedCracker
)

# core.files imports
from ..files import (
    Path,
    get_exec_path
)

class PasswordCracker:
    """
        Password Cracker (hash and credential cracker) - Main Password Cracker class
    """
    # Supported crackers
    HASH_CRACKERS = ["john", "hashcat"]
    CREDENTIAL_CRACKERS = ["hydra"]

    def __init__(self, name, *, version=None, main_exec=None):
        self.name = name #it can be a list of name (e.g. ["hashcat", "hc"])
        self.main_name = name[0] if isinstance(name, list) else name
        self.version = version
        self.main_exec= main_exec
        self.enable = False

        if main_exec:
            self.enable = True
        else:
            self.main_exec = PasswordCracker.search_main_exec(name)
            if self.main_exec is None:
                self.enable = False
            else:
                self.enable = True

    def __repr__(self):
        #return f"Cracker(name: {self.mainName}, version: {self.version})"
        return self.main_name

    #debugged - date: Feb 27 2021
    @staticmethod
    def search_main_exec(cracker_name: List[str]):
        """
        Search an executable file of a password cracker using crackerName (list) as patterns
        """
        # searching the executable plugin in the PATH
        #import pdb; pdb.set_trace()
        exec_path = get_exec_path()
        for name in cracker_name:
            exec_pattern = re.compile(rf"{name}(\.exe)?")
            for dir_path in exec_path:
                dirname = dir_path
                #print(f"dirname: {dirname}")
                for executable in os.listdir(dir_path):
                    #if os.path.isfile(executable):
                    #print(f"\texecutable : {executable}")
                    if exec_pattern.fullmatch(executable):
                        main_exec = os.path.join(dirname, executable)
                        return main_exec

        return None


    @staticmethod
    def hash_status(query_hash: str, potfile: str = None):
        """
        Check the status (broken or not) of query hash or hashes file
        """
        pass # implement for each child class of PasswordCracker
