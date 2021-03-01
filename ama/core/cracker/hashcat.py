#!/usr/bin/env python3
#
# Hashcat class
# Jan 9 2021 - Implementation of Hashcat class
#                (using core module of pyhashcat python package)
#
# Maintainer: glozanoa <glozanoa@uni.pe>



import os
import re
from tabulate import tabulate
from sbash import Bash

# cmd2 imports
import cmd2

# cracker module imports
from .cracker import PasswordCracker
from .crackedHash import CrackedHash
# cracker exceptions imports
from .crackerException import (
    InvalidParallelJob,
    InvalidHashType
)

# hashcat hashes import
from ama.data.hashes import hcHashes

# validator imports
from ama.core.files import Path


class Hashcat(PasswordCracker):
    """
    Hashcat password cracker
    This class implement the diverse attack of hashcat and its benchmark
    Suported Attacks: wordlist, incremental, masks, combination, hybrid
    """

    HASHES = hcHashes

    def __init__(self):
        super().__init__(name=['hashcat', 'hc'], version="v6.1.1")

    @staticmethod
    def checkHashType(hashType):
        """
        Check if the hash type is a valid hashcat hash type

        Args:
            hashType (str): hash type

        Raises:
        InvalidHashType: Error if the hasType is an unsopported hash type of a cracker
        """

        if not (hashType in Hashcat.HASHES):
            raise InvalidHashType(Hashcat, hashType)

    @staticmethod
    def searchHash(pattern, *, sensitive=False):
        """
        Search valid hashcat's hashes types given a pattern
        """

        if sensitive:
            hashPattern = re.compile(rf"[\W|\w|\.]*{pattern}[\W|\w|\.]*")
        else:
            hashPattern = re.compile(rf"[\W|\w|\.]*{pattern}[\W|\w|\.]*", re.IGNORECASE)

        posibleHashes = []
        for hashId, hashType in Hashcat.HASHES.items():
            hashName, description = hashType.values()
            if hashPattern.fullmatch(hashName):
                posibleHashes.append((hashId, hashName, description))

        print(tabulate(posibleHashes, headers=["#", "Name", "Description"]))


    @staticmethod
    def hashStatus(queryHash, potfile=None):
        """
        Check the status (broken by John or not) of query hash

        Return:
        if queryHash is in potfile then [HASHTYPE, HASH, PASSWORD] list is returned
        otherwise None is returned
        """
        #import pdb;pdb.set_trace()

        if potfile is None:
            HOME = os.path.expanduser("~")
            potfile = os.path.join(HOME, ".hashcat/hashcat.potfile")

        try:
            permission = [os.R_OK]
            Path.access(permission, potfile)

            crackedPattern = re.compile(rf"({queryHash}):(\W*|\w*|.*)", re.DOTALL)

            with open(potfile, 'r') as potFile:
                while   crackedHash := potFile.readline().rstrip():
                    if crackedHashPot := crackedPattern.fullmatch(crackedHash):
                        hashPot = crackedHashPot.groups()
                        return CrackedHash(crackedHash = hashPot[0],
                                           password = hashPot[1],
                                           cracker = Hashcat)

            return None


        except Exception as error:
            cmd2.Cmd.pexcept(error)

    @staticmethod
    def hashesFileStatus(queryHashesFile, potfile=None):
        """
        Check the status (broken by Hashcat or not) of hashes in queryHashesFile
        """
        hashesStatus = {'cracked': [], "uncracked": []}

        if potfile is None:
            HOME = os.path.expanduser("~")
            potfile = os.path.join(HOME, ".hashcat/hashcat.pot")

        try:
            permission = [os.R_OK]
            Path.access(permission, potfile, queryHashesFile)


            with open(queryHashesFile, 'r') as hashesFile:
                while queryHash := hashesFile.readline().rsplit():
                    if crackerHash := John.hashStatus(queryHash, potfile):
                        hashesStatus['cracked'].append(crackerHash)
                    else:
                        hashesStatus['uncracked'].append([queryHash])

            return hashesStatus

        except Exception as error:
            cmd2.Cmd.pexcept(error)


    def benchmark(self, slurm=None):
        """
        Hashcat benchmark
        """
        if self.status:
            cmd2.Cmd.poutput(f"Performing Hashcat benchmark.")
            if slurm.partition:
                cmd2.Cmd.pwarning("Hashcat benchmark does not yet support  Slurm execution")
            else:
                johnBenchmark = f"{self.mainexec} -b"
                Bash.exec(johnBenchmark)
        else:
            cmd2.Cmd.pwarning("Cracker {self.mainName} is disable")

    def wordlistAttack(self):
        if self.status:
            cmd2.Cmd.poutput(f"Performing Hashcat benchmark.")
            if slurm.partition:
                cmd2.Cmd.pwarning("Hashcat benchmark does not yet support  Slurm execution")
            else:
                johnBenchmark = f"{self.mainexec} -b"
                Bash.exec(johnBenchmark)
        else:
            cmd2.Cmd.pwarning("Cracker {self.mainName} is disable")

    def wordlist(*, attackMode=0, hashType, hashFile, wordlist, hpc=None):
        Hashcat.checkAttackArgs(_hashType=hashType,
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
    def checkAttackMode(attack):
        if not (attack in Hashcat.attackMode):
            raise AttackModeError(attack)

    @staticmethod
    def checkAttackArgs(*,
                        _hashType=None,
                        _hashFile=None,
                        _wordlist=None,
                        _maskFile=None):
        PasswordCracker.checkAttackArgs(_hashFile = _hashFile,
                                        _wordlist = _wordlist,
                                        _masksFile = _maskFile)

        Hashcat.checkHashType(_hashType)


    # @staticmethod
    # def selectAttack(*,
    #             attackMode=None,
    #             hashType=None,
    #             hashFile=None,
    #             wordlist=[],
    #             masksFile=None,
    #             hpc = None):

    #     # contruction of hashcat cmd to execute
    #     Hashcat.checkAttackMode(attackMode)
    #     if attackMode == 0:   # wordlist(or straight) attack
    #         HCAttacks.wordlist(hashType = hashType,
    #                            hashFile = hashFile,
    #                            wordlist = wordlist,
    #                            hpc = hpc)

    #     elif attackMode==1: #combination attack
    #         HCAttacks.combination(hashType = hashType,
    #                               hashFile = hashFile,
    #                               wordlists = wordlist,
    #                               hpc = hpc)

    #     elif attackMode == 3:   #mask attack
    #         HCAttacks.maskAttack(hashType = hashType,
    #                              hashFile = hashFile,
    #                              maskFile = masksFile,
    #                              hpc = hpc)

    #     elif attackMode == 6:   #hybridWMF attack (wordlist + mask file)
    #         HCAttacks.hybridWMF(hashType = hashType,
    #                             hashFile = hashFile,
    #                             wordlist = wordlist,
    #                             maskFile = masksFile,
    #                             hpc = hpc)
    #     elif attackMode == 7:   #hybridMFW attack (mask file + wordlist)
    #         HCAttacks.hybridMFW(hashType = hashType,
    #                             hashFile = hashFile,
    #                             wordlist = wordlist,
    #                             maskFile = masksFile,
    #                             hpc = hpc)

class HCAttacks:
    @staticmethod
    def wordlist(*, attackMode=0, hashType, hashFile, wordlist, hpc=None):
        Hashcat.checkAttackArgs(_hashType=hashType,
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
        Hashcat.checkAttackArgs(_hashType=hashType,
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
    def incremental(*, attackMode=2, hashType, hashesFile, minlength=1, maxlength, hpc=None):
        if hpc:
            pass
        else:
            mask = '?a'*(minlength-1)
            for k in range(minlength, maxlength):
                if not PasswordCracker.statusHashFile(hashesFile):
                    mask += '?a'
                    incrementalAttack = f"hashcat -a 3 -m {hashType} {mask}"
                    Bash.exec(incrementalAttack)



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
