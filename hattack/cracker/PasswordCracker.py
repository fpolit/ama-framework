#!/usr/bin/env python3
#
# PasswordCracker - main class to generate password crackers (john, hashcat, ...)
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import re
import os

from fineprint.status import print_failure, print_successful, print_status

# importing PasswordCracker exceptions
from .PasswordCrackerExceptions import CrackerExecNotFound
from .PasswordCrackerExceptions import InvalidCracker
from .PasswordCrackerExceptions import NotSupportedCracker

# base module imports
from ..base.FilePath import FilePath
from ..base.ExecPath import getExecPath

class PasswordCracker:
    """
        PasswordCracker (hashcat, john)
    """
    crackProcesses = None
    crackers = ["john", "hashcat"]
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
                        _hashFile=None,
                        _wordlist=None, # can be a list of wordlists
                        _masksFile=None):
        """
        check the read permission of hashFile, wordlist and masksFile files
        """

        # validation of existence and read access of input file arguments
        if not isinstance(_wordlist, list):
            _wordlist = [_wordlist]

        for inputFile in [_hashFile, *_wordlist, _masksFile]:
            if inputFile:
                inputFilePath = FilePath(inputFile)
                if not inputFilePath.checkReadAccess():
                    print_failure(f"No read permission in {inputFilePath} file")
                    raise PermissionError


    @staticmethod
    def searchHash(pattern, *, sensitive=False):

        if cracker in PasswordCracker.crackers:
            if not sensitive:
                hashPattern = re.compile(rf"\w*{search}\w*", re.IGNORECASE)
            else:
                hashPattern = re.compile(rf"\w*{search}\w*")

            if cracker in ["john", "jtr"]: # search by a jtr hash format
                print_status(f"John the Ripper posible hash types(pattern: *{search}*)")
                for hashType in John.hashes:
                    if hashPattern.search(hashFormat):
                        print_successful(hashFormat)

            if cracker in ["hashcat", "hc"]: # search by an hashcat hash format
                print_status(f"Hashcat posible hash types(pattern: *{search}*)")
                print_status("id\tname")
                for hashId, hashType in Hashcat.hashes.items():
                    if hashPattern.search(hashType['Name']):
                        print_successful(f"{hashId}\t{hashType['Name']}")
        else:
            raise InvalidCracker(cracker)


    @staticmethod
    def hashStatus(cracker, queryHash, potfile=None):
        # NOTE: CHECK crackedPattern
        #import pdb; pdb.set_trace()
        if cracker  in PasswordCracker.crackers:
            if potfile:
                potFilePath = FilePath(potfile)

                if cracker in ["john", "jtr"]:
                    crackedPattern = re.compile(rf"\$(\W*|\w*)\$({queryHash})(\$(\W*|\w*)\$)?:(\W*|\w*|\@*)")

                elif cracker in ["hashcat", "hc"]:
                    crackedPattern = re.compile(rf"({queryHash}):(\W*|\w*)")

            else:
                homePath = os.path.expanduser("~")
                if cracker in ["john", "jtr"]:
                    potFilePath = FilePath(os.path.join(homePath, ".john/john.pot"))
                    crackedPattern = re.compile(rf"\$(\W*|\w*)\$({queryHash})(\$(\W*|\w*)\$)?:(\W*|\w*|\@*)")

                elif cracker in ["hashcat", "hc"]:
                    potFilePath = FilePath(os.path.join(homePath, ".hashcat/hashcat.potfile"))
                    crackedPattern = re.compile(rf"({queryHash}):(\W*|\w*)")

            with open(potFilePath, 'r') as _potFile:
                while   crackedHash := _potFile.readline().rstrip():
                    if crackedPattern.fullmatch(crackedHash):
                        return True
            return False

        else:
            raise NotSupportedCracker(cracker)


    @staticmethod
    def globalHashStatus(queryHash, potfile=None):
        """
        Check the status of queryHash in the potfile of all the supported crackers by PasswordCracker(jtr and hc)

        return the status of the hash (False: hash is uncracked, True: hash is cracked) and the cracker that crack the hash otherwise return None
        """

        crackers = PasswordCracker.crackers
        # staus of hash(False: no cracked, True:cracked)
        #import pdb; pdb.set_trace()
        for cracker in crackers:
            if PasswordCracker.hashStatus(cracker, queryHash, potfile):
                return [True, cracker]
        return [False, None]


    @staticmethod
    def hashFileStatus(cracker, hashFile, potfile=None):
        """
        Check if all the hashes in the hashFile are cracked by cracker

        return:
        True - if all the hashes in hashFile are cracked
        False - if some hashe in hashFile isn't cracked
        """
        hashFilePath = FilePath(hashFile)

        if hashFilePath.checkReadAccess():
            with open(hashFilePath , 'r') as _hashFile:
                while queryHash := _hashFile.readline().rstrip():
                    if not PasswordCracker.hashStatus(cracker, queryHash, potfile):
                        return False
            return True

        else:
            print_failure(f"No read permission in {hashFilePath} file")
            raise PermissionError

    @staticmethod
    def globalHashFileStatus(hashFile, potfile=None):
        """
        Check the status of all the hashes in the hash file in the potfile of the supported crackers by PasswordCracker(jtr and hc)

        return the status of the hash (False: some hash is uncracked, True: all hashes are cracked) and the cracker that crack the hash otherwise return None
        """

        crackers = PasswordCracker.crackers
        # staus of hash(False: no cracked, True:cracked)
        for cracker in crackers:
            if PasswordCracker.hashFileStatus(cracker, hashFile, potfile):
                return [True, cracker]
        return [False, None]


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
            #import pdb; pdb.set_trace()
            execPath = getExecPath()
            self.exec = []
            for name in self.name:
                nameExec = re.compile(rf"{name}(\.exe)?")
                for dirPath in execPath:
                    dirname = dirPath
                    #print(f"dirname: {dirname}")
                    for executable in os.listdir(dirPath):
                        #if os.path.isfile(executable):
                        #print(f"\texecutable : {executable}")
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

    def validateStatus(self):
        if self.checkStatus():
            print_successful(f"Plugin {self.name} is currently active.")
        else:
            raise Exception("PLugin {self.name} is disable.")
