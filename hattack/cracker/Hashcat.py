#!/usr/bin/env python3

"""
# Hashcat class
# Jan 9 2021 - Implementation of Hashcat class
                (using core module of pyhashcat python package)
#
# Maintainer: glozanoa <glozanoa@uni.pe>
"""



import os
import re
from os.path import dirname
from tabulate import tabulate
from sbash.core import Bash
from fineprint.status import print_status, print_failure, print_successful

# cracker modules
from .PasswordCracker import PasswordCracker
from ..hashes.hc import hashes

# base modules
from ..base.FilePath import FilePath

# importing PasswordCracker exceptions
from .PasswordCrackerExceptions import CrackerDisableError
from .PasswordCrackerExceptions import AttackModeError
from .PasswordCrackerExceptions import CrackerHashError

# hpc module
from ..hpc.HPC import HPC

# hpc exceptions
from ..hpc.HPCExceptions import ParallelWorkError

# utilities module
from ..utilities.combinator import Combinator
from ..utilities.combinator import InvalidWordlistNumber


class Hashcat(PasswordCracker):
    hashes = hashes
    attackMode = {  0:"Wordlist",
                    1:"Combination",
                    3:"Mask",
                    6:"Hybrid Wordlist + Mask",
                    7:"Hybrid Mask + Wordlist"}

    def __init__(self):
        super().__init__(name=['hashcat', 'hc'])


    @staticmethod
    def benchmark():
        cracker = Hashcat()
        if cracker.checkStatus():
            benchmark = f"{cracker.mainexec} -b"
            print_status(f"Running: {benchmark}")
            Bash.exec(benchmark)
        else:
            raise CrackerDisableError("Hashcat")

    @staticmethod
    def checkAttackMode(attack):
        if not (attack in Hashcat.attackMode):
            raise AttackModeError(attack)


    @staticmethod
    def checkHashType(hashType):
        """ Check if the hash type is correct

        Args:
            hashType (str): hash type

        Raises:
            HashcatHashError: Error if the given hash isn't a valid hash type
        """

        if not (hashType in Hashcat.hashes):
            raise HashcatHashError(hashType)


    @staticmethod
    def checkAttackArgs(*,
                        _hashType=None,
                        _hashFile=None,
                        _wordlist=None,
                        _maskFile=None):
        PasswordCracker.checkAttackArgs(__hashFile = _hashFile,
                                        __wordlist = _wordlist,
                                        __maskFile = _maskFile)

        Hashcat.checkHashType(_hashType)


    @staticmethod
    def selectAttack(*,
                attackMode=None,
                hashType=None,
                hashFile=None,
                wordlist=[],
                maskFile=None,
                hpc = None):

        # contruction of hashcat cmd to execute
        Hashcat.checkAttackMode(attackMode)
        if attackMode == 0:   # wordlist(or straight) attack
            HCAttacks.wordlist(hashType = hashType,
                               hashFile = hashFile,
                               wordlist = wordlist,
                               hpc = hpc)

        elif attackMode==1: #combination attack
            HCAttacks.combination(hashType = hashType,
                                  hashFile = hashFile,
                                  wordlists = wordlist,
                                  hpc = hpc)

        elif attackMode == 3:   #mask attack
            HCAttacks.maskAttack(hashType = hashType,
                                 hashFile = hashFile,
                                 maskFile = maskFile,
                                 hpc = hpc)

        elif attackMode == 6:   #hybridWMF attack (wordlist + mask file)
            HCAttacks.hybridWMF(hashType = hashType,
                                hashFile = hashFile,
                                wordlist = wordlist,
                                maskFile = maskFile,
                                hpc = hpc)
        elif attackMode == 7:   #hybridMFW attack (mask file + wordlist)
            HCAttacks.hybridMFW(hashType = hashType,
                                hashFile = hashFile,
                                wordlist = wordlist,
                                maskFile = maskFile,
                                hpc = hpc)


    @staticmethod
    def searchHash(pattern, *, sensitive=False):
        """
        search by a valid hashcat hash type given a pattern
        """

        if not sensitive:
            hashPattern = re.compile(rf"\w*{pattern}\w*", re.IGNORECASE)
        else:
            hashPattern = re.compile(rf"\w*{pattern}\w*")

        print_status(f"Posible Hashcat hashes(pattern: *{pattern}*)")
        posibleHashes = []
        for hashId, hashType in Hashcat.hashes.items():
            hashName, description = hashType.values()
            #print(f"hashcat hash: {hashName}")
            if hashPattern.search(hashName):
                posibleHashes.append([hashId, hashName, description])

        print(tabulate(posibleHashes, headers=["id", "name", "description"]))


class HCAttacks:
    @staticmethod
    def wordlist(*, attackMode=0, hashType, hashFile, wordlist, hpc=None):
        PasswordCracker.checkAttackArgs(_hashType=hashType,
                                        _hashFile=hashFile,
                                        _wordlist=wordlist)
        hc = Hashcat()
        print_status(f"Attacking {hashFile} with {wordlist} in straigth mode.")
        if hpc:
            # develop me please
            pass
        else:
            wordlistAttack =   f"{hc.mainexec} -a {attackMode} -m {hashType} {hashFile} {wordlist}"
            Bash.exec(wordlistAttack)

    @staticmethod
    def combination(*, attackMode=1, hashType, hashFile, wordlists=[], hpc=None):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile,
                             _wordlist=wordlists)


        if hpc:
            pass
        else:
            wordlistNumber = len(wordlists)
            if wordlistNumber != 2:
                raise InvalidWordlistNumber(wordlistNumber)

            firstWordlist, secondWordlist = wordlists
            combinationAttack = f"{hc.mainexec} -a {attackMode} -m {hashType} {hashFile} {firstwordlist} {secondwordlist}"
            Bash.exec(combinationAttack)


    @staticmethod
    def maskAttack(*, attackMode=3, hashType, hashFile, maskFile, hpc=None):
        Hashcat.checkAttackArgs(_hashType=hashType,
                                _hashFile=hashFile,
                                _maskFile=maskFile)
        hc = Hashcat()
        print_status(f"Attacking {hashFile} with {maskFile} in mask attack mode.")

        if hpc:
            #develop me please
            pass
        else:
            with open(maskFile, 'r') as masks:
                while mask := masks.readline().rstrip():
                    if not PasswordCracker.statusHashFile(hashFilePath):
                        maskAttack =   f"{hc.mainexec} -a {attackMode} -m {hashType} {mask}"
                        print_status(f"Running: {maskAttack}")
                        Bash.exec(maskAttack)

    @staticmethod
    def hybridWMF(*, attackMode=6, hashType, hashFile, wordlist, maskFile, hpc=None):
        Hashcat.checkAttackArgs(_hashType = hashType,
                                _hashFile = hashFile,
                                _wordlist = wordlist,
                                _maskFile = maskFile)
        hc = Hashcat()
        print_status(f"Attacking {hashFile} with {wordlist} wordlist and {maskFile} mask file in hybrid WMF attack mode.")
        if hpc:
            # develop me please
            pass
        else:
            with open(maskFile, 'r') as masks:
                while mask := masks.readline().rstrip():
                    if not PasswordCracker.statusHashFile(hashFilePath):
                        hybridWMFAttack =   f"{hc.mainexec} -a {attackMode} -m {hashType} {wordlist} {mask}"
                        print_status(f"Running: {hybridWMFAttack}")
                        Bash.exec(maskAttack)



    @staticmethod
    def hybridMFW(*, attackMode=7, hashType, hashFile, wordlist, maskFile, hpc=None):
        Hashcat.checkAttackArgs(_hashType = hashType,
                                _hashFile = hashFile,
                                _wordlist = wordlist,
                                _maskFile = maskFile)
        hc = Hashcat()
        print_status(f"Attacking {hashFile} with {maskFile} mask file and {wordlist} wordlist in hybrid MFW attack mode.")
        if hpc:
            # develop me please
            pass
        else:
            with open(maskFile, 'r') as masks:
                while mask := masks.readline().rstrip():
                    if not PasswordCracker.statusHashFile(hashFilePath):
                        hybridMFWAttack =   f"{hc.mainexec} -a {attackMode} -m {hashType} {mask} {wordlist}"
                        print_status(f"Running: {hybridMFWAttack}")
                        Bash.exec(maskAttack)
