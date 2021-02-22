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
    hashCrackers = ["john", "hashcat"]
    credentialCrackers = ["hydra"]

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

    # @staticmethod
    # def checkAttackArgs(*,
    #                     _hashFile=None,
    #                     _wordlist=None, # can be a list of wordlists
    #                     _masksFile=None):
    #     """
    #     check the read permission of hashFile, wordlist and masksFile files
    #     """

    #     # validation of existence and read access of input file arguments
    #     if not isinstance(_wordlist, list):
    #         _wordlist = [_wordlist]

    #     for inputFile in [_hashFile, *_wordlist, _masksFile]:
    #         if inputFile:
    #             inputFilePath = FilePath(inputFile)
    #             if not inputFilePath.checkReadAccess():
    #                 print_failure(f"No read permission in {inputFilePath} file")
    #                 raise PermissionError


    # @staticmethod
    # def searchHash(pattern, *, sensitive=False):

    #     if cracker in PasswordCracker.crackers:
    #         if not sensitive:
    #             hashPattern = re.compile(rf"\w*{search}\w*", re.IGNORECASE)
    #         else:
    #             hashPattern = re.compile(rf"\w*{search}\w*")

    #         posibleHashes = []
    #         if cracker in ["john", "jtr"]: # search by a jtr hash format
    #             print_status(f"John the Ripper posible hash types(pattern: *{search}*)")
    #             for hashType in John.hashes:
    #                 if hashPattern.search(hashFormat):
    #                     print_successful(hashFormat)

    #         elif cracker in ["hashcat", "hc"]: # search by an hashcat hash format
    #             print_status(f"Hashcat posible hash types(pattern: *{search}*)")
    #             print_status("id\tname")
    #             for hashId, hashType in Hashcat.hashes.items():
    #                 if hashPattern.search(hashType['Name']):
    #                     print_successful(f"{hashId}\t{hashType['Name']}")
    #     else:
    #         raise InvalidCracker(cracker)


    # @staticmethod
    # def reportHashesFileStatus(hashesFile):
    #     hashesStatus = [] # status of all the hashes in hashesFile

    #     hashesFilePath = FilePath(hashesFile)
    #     with open(hashesFilePath, 'r') as _hashesFile:
    #         while queryHash := _hashesFile.readline().rstrip():
    #             crackedHash = PasswordCracker.globalHashStatus(queryHash)
    #             #print(f"crackedHash: {crackedHash}")

    #             if crackedHash:
    #                 cracker, hashPot = crackedHash
    #                 hashesStatus.append(["cracked", cracker] + hashPot)
    #             else:
    #                 hashesStatus.append(["uncracked", None, None, queryHash, None])


    #     print(tabulate(hashesStatus, headers=["status", "cracker", "hash type", "hash", "password"]))

    # @staticmethod
    # def reportHashStatus(queryHash):
    #     hashStatus = []
    #     crackedHash = PasswordCracker.globalHashStatus(queryHash)

    #     if crackedHash:
    #         cracker, hashPot = crackedHash
    #         hashStatus.append(["cracked", cracker] + hashPot)
    #     else:
    #         hashStatus.append(["uncracked", None, None, queryHash, None])

    #     print(tabulate(hashStatus, headers=["status", "cracker", "hash type", "hash", "password"]))


    # @staticmethod
    # def hashStatus(cracker, queryHash, potfile=None):
    #     """
    #     if the queryHash was cracked by the cracker (is in its potfile) then return [hashType, queryHash, password] otherwise return None
    #     """

    #     #import pdb;pdb.set_trace()

    #     try:
    #         if cracker  in PasswordCracker.crackers:
    #             if potfile:
    #                 potFilePath = FilePath(potfile)

    #                 if cracker in ["john", "jtr"]:
    #                     crackedPattern = re.compile(rf"\$(\W*|\w*|.*)\$({queryHash})(\$(\W*|\w*|.*)\$)?:(\W*|\w*|.*)", re.DOTALL)

    #                 elif cracker in ["hashcat", "hc"]:
    #                     crackedPattern = re.compile(rf"({queryHash}):(\W*|\w*|.*)", re.DOTALL)

    #             else:
    #                 homePath = os.path.expanduser("~")
    #                 if cracker in ["john", "jtr"]:
    #                     johnPotFile = os.path.join(homePath, ".john/john.pot")
    #                     potFilePath = FilePath(johnPotFile)
    #                     crackedPattern = re.compile(rf"\$(\W*|\w*|.*)\$({queryHash})(\$(\W*|\w*|.*)\$)?:(\W*|\w*|.*)", re.DOTALL)

    #                 elif cracker in ["hashcat", "hc"]:
    #                     hashcatPotFile = os.path.join(homePath, ".hashcat/hashcat.potfile")
    #                     potFilePath = FilePath(hashcatPotFile)
    #                     crackedPattern = re.compile(rf"({queryHash}):(\W*|\w*|.*)", re.DOTALL)

    #             #print(f"potfile: {potFilePath}")
    #             with open(potFilePath, 'r') as _potFile:
    #                 while   crackedHash := _potFile.readline().rstrip():
    #                     if crackedHashPot := crackedPattern.fullmatch(crackedHash):
    #                         hashPot = crackedHashPot.groups()
    #                         #_potFile.close()
    #                         if cracker in ["john", "jtr"]:
    #                             return [hashPot[0], hashPot[1], hashPot[-1]]
    #                         elif cracker in ["hashcat", "hc"]:
    #                             return [None, hashPot[0], hashPot[1]]
    #             return None

    #         else:
    #             raise NotSupportedCracker(cracker)

    #     except FileNotFoundError as error:
    #         return None

    #     except NotSupportedCracker as error:
    #         print_failure(f"ERROR: {error}")
    #         return None




    # @staticmethod
    # def globalHashStatus(queryHash, potfile=None):
    #     """
    #     Check the status of queryHash in the potfile of all the supported crackers by PasswordCracker(jtr and hc)

    #     return  the cracker that crack the hash and hashPot(hashType, hash, password) otherwise return None
    #     """

    #     crackers = PasswordCracker.crackers
    #     # staus of hash(False: no cracked, True:cracked)
    #     #import pdb; pdb.set_trace()
    #     for cracker in crackers:
    #         if crackedHashPot := PasswordCracker.hashStatus(cracker, queryHash, potfile):
    #             return [cracker, crackedHashPot]
    #     return None


    # @staticmethod
    # def hashFileStatus(cracker, hashFile, potfile=None):
    #     """
    #     Check if all the hashes in the hashFile are cracked by cracker

    #     return:
    #     True - if all the hashes in hashFile are cracked
    #     False - if some hashe in hashFile isn't cracked
    #     """
    #     hashFilePath = FilePath(hashFile)
    #     if hashFilePath.checkReadAccess():

    #         with open(hashFilePath , 'r') as _hashFile:
    #             while queryHash := _hashFile.readline().rstrip():
    #                 crackedHash = PasswordCracker.hashStatus(cracker, queryHash, potfile)
    #                 if not crackedHash:
    #                     return False
    #             return True
    #     else:
    #         print_failure(f"No read permission: {hashFilePath}")
    #         raise PermissionError



    # @staticmethod
    # def globalHashFileStatus(hashFile, potfile=None):
    #     """
    #     Check the status of all the hashes in the hash file in the potfile of the supported crackers by PasswordCracker(jtr and hc)

    #     return the status of the hash (False: some hash is uncracked, True: all hashes are cracked) and the cracker that crack the hash otherwise return None
    #     """

    #     crackers = PasswordCracker.crackers
    #     # staus of hash(False: no cracked, True:cracked)
    #     for cracker in crackers:
    #         if PasswordCracker.hashFileStatus(cracker, hashFile, potfile):
    #             return [True, cracker]
    #     return [False, None]
