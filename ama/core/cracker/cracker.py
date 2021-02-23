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

# importing PasswordCracker exceptions
from .crackerException import (
    CrackerExecNotFound,
    InvalidCracker,
    NotSupportedCracker
)

# core.files imports
from ..files import (
    Path,
    getExecPath
)

class PasswordCracker:
    """
        Password Cracker (hash and credential cracker) - Main Password Cracker class
    """
    # Supported crackers
    HASH_CRACKERS = ["john", "hashcat"]
    CREDENTIAL_CRACKERS = ["hydra"]

    def __init__(self, name, *, version=None, mainexec=None):
        self.name = name #it can be a list of name (e.g. ["hashcat", "hc"])
        self.mainName = name[0]
        self.version = version
        self.mainexec= mainexec

        if mainexec:
            self.status = True
        else:
            self.mainexec = PasswordCracker.searchMainexec(name)
            if self.mainexec is None:
                self.status = False
                cmd2.Cmd.pwarning(f"No executable founded for cracker: {name}")

    @staticmethod
    def searchMainexec(crackerName: List(str)):
        """
        Search an executable file of a password cracker using crackerName (list) as patterns
        """
        # searching the executable plugin in the PATH
        #import pdb; pdb.set_trace()
        execPath = getExecPath()
        executables = []
        for name in crackerName:
            nameExec = re.compile(rf"{crackerName}(\.exe)?")
            for dirPath in execPath:
                dirname = dirPath
                #print(f"dirname: {dirname}")
                for executable in os.listdir(dirPath):
                    #if os.path.isfile(executable):
                    #print(f"\texecutable : {executable}")
                    if nameExec.fullmatch(executable):
                        execPath = os.path.join(dirname, executable)
                        executables.append(execPath)

        if executables:
            mainexec = executables[0]
        else:
            mainexec = None

        return mainexec
