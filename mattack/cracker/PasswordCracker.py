#!/usr/bin/env python3

import re
import os

from fineprint.status import print_failure, print_successful, print_status

# importing PasswordCracker exceptions
from .PasswordCrackerExceptions import CrackerExecNotFound

# base module imports
from ..base.FilePath import FilePath

class PasswordCracker:
    """
        PasswordCracker (hashcat, john)
    """
    crackProcesses = None
    def __init__(self, name, *, executable=[], status=None, path=None, version=None):
        self.name = name #it can be a list of name (for example [hashcat, hc])
        self.exec=None
        self.mainexec=None
        if executable:
            self.exec = executable
            self.mainexec = executable[0]
        else:
            self.searchExec()

        self.status = status #False: Disable and True: Active
        self.path = path
        self.version = version


    @staticmethod
    def checkAttackArgs(*,
                        __hashFile=None,
                        __wordlist=None,
                        __maskFile=None):
        """
        check the read permission of hashFile, wordlist and maskFile files
        """

        # validation of existence and read access of input file arguments
        for inputFile in [__hashFile, *__wordlist, __maskFile]:
            if inputFile:
                inputFilePath = FilePath(inputFile)
                if not inputFilePath.checkReadAccess():
                    print_failure(f"No read permission in {inputFilePath} file")
                    raise PermissionError



    @staticmethod
    def statusHash(cracker, queryHash, potfile=None):
        if potfile:
            potFilePath = FilePath(potfile)
            if isinstance(cracker, John):
                crackedPattern = re.compile(rf"\$(\W*|\w*)\$({queryHash})(\$(\W*|\w*)\$)?:(\W*|\w*|\@*)")
            elif isinstance(cracker, Hashcat):
                crackedPattern = re.compile(rf"({queryHash}):(\W*|\w*)")

        else:
            homePath = os.path.expanduser("~")
            if isinstance(cracker, John):
                potFilePath = FilePath(os.path.join(homePath, ".john/john.pot"))
                crackedPattern = re.compile(rf"\$(\W*|\w*)\$({queryHash})(\$(\W*|\w*)\$)?:(\W*|\w*|\@*)")
            elif isinstance(cracker, Hashcat):
                potFilePath = FilePath(os.path.join(homePath, ".hashcat/hashcat.potfile"))
                crackedPattern = re.compile(rf"({queryHash}):(\W*|\w*)")

        with open(potFilePath, 'r') as potFile:
            while   crackedHash := potfile.readline().rstrip():
                if(crackedPattern.fullmatch(crackedHash)):
                    return True
        return False

    @staticmethod
    def statusHashFile(cracker, strHashFile, potfile=None):
        """
        Check if all the hashes in the hashFile are cracked

        return:
        True - if all the hashes in hashFile are cracked
        False - if some hashe in hashFile isn't cracked
        """
        hashFilePath = FilePath(strHashFile)

        if hashFilePath.checkReadAccess():
            with open(hashFilePath , 'r') as hashFile:
                while queryHash := hashFile.readline().rstrip():
                    if not PasswordCracker.statusHash(cracker, queryHash, potfile):
                        return False
            return True

        else:
            print_failure(f"No read permission in {hashFilePath} file")
            raise PermissionError


    def getName(self):
        return self.name

    def getMainExec(self):
        return self.mainexec

    def searchExec(self):
        if self.exec:
            for idx, executable in enumerate(exec):
                if not os.access(self.exec, os.X_OK):
                    self.exec.pop(idx)

            if self.exec: # there are some executable
                self.status = True
                self.mainexec = self.exec[0]
            else:
                self.status = False
        else:
            # searching the executable plugin in the PATH
            execPath = os.get_exec_path()
            for name in self.name:
                nameExec = re.compile(rf"{name}(\.exe)?")
                for dirPath in execPath:
                    dirname = dirPath
                    for executable in os.listdir(dirPath):
                        if nameExec.fullmatch(executable):
                            execPath = os.path.join(dirname, executable)
                            self.exec.append(execPath)
                            print_successful(f"{execPath} executable found.")

            if self.exec:
                self.status = True
                self.mainexec = self.exec[0]
            else:
                raise CrackerExecNotFound(self.name)

    def checkStatus(self):
        if self.status:
            return True
        else:
            self.searchExec()
            if self.status:
                return True
            else:
                print_failure(f"No {self.name} executable in the PATH")
                return False

    def _validate_status(self):
        if self.checkStatus():
            print_successful(f"Plugin {self.name} is currently active.")
        else:
            raise Exception("PLugin {self.name} is disable.")
