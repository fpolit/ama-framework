#!/usr/bin/env python3

"""
# John class
# Jan 9 2021 - Implementation of John class
                (using core module of john python package)
#
# Maintainer: glozanoa <glozanoa@uni.pe>
"""

import os
import re
from sbash.core import Bash
from fineprint.status import print_status, print_failure, print_successful

# cracker modules
from .PasswordCracker import PasswordCracker

from .PasswordCrackerExceptions import CrackerHashError

# hashes modules
from ..hashes.jtr import hashes

# base module
from ..base.FilePath import FilePath

# hpc module
from ..hpc.HPC import HPC

# hpc exceptions
from ..hpc.HPCExceptions import ParallelWorkError

# utilities module
from ..utilities.combinator import Combinator
from ..utilities.combinator import InvalidWordlistNumber


class John(PasswordCracker):
    hashes = hashes

    attackMode = {0:"single",
                  1:"combination",
                  2:"wordlist",
                  3:"incremental",
                  4:"mask",
                  6:"Hybrid-Wordlist+Mask",
                  7:"Hybrid-Mask+Wordlist"}

    def __init__(self):
        super().__init__(name=["john"])

    @staticmethod
    def benchmark():
        """
            Run john benchmark
        """
        cracker = John()
        if cracker.checkStatus():
            benchmark = f"{cracker.mainexec} -b"
            print_status(f"Running: {benchmark}")
            Bash.exec(benchmark)
        else:
            raise CrackerDisableError("John")



    @staticmethod
    def checkAttackMode(attack):
        if not (attack in John.attackMode):
            raise AttackModeError(attack)


    @staticmethod
    def checkHashType(hashType):
        """ Check if the hash type is correct

        Args:
            hashType (str): hash type

        Raises:
            CrackerHashError: Error if the given hash isn't a valid hash type
        """

        if not (hashType in John.hashes):
            raise CrackerHashError(John, hashType)


    @staticmethod
    def checkAttackArgs(*,
                        _hashType=None,
                        _hashFile=None,
                        _wordlist=None,
                        _maskFile=None):
        PasswordCracker.checkAttackArgs(__hashFile = _hashFile,
                                        __wordlist = _wordlist,
                                        __maskFile = _maskFile)

        John.checkHashType(_hashType)

    @staticmethod
    def selectAttack(*,
                attackMode=None,
                hashType=None,
                hashFile=None,
                wordlist=[],
                maskFile=None,
                hpc = None):

        # contruction of hashcat cmd to execute
        John.checkAttackMode(attackMode)
        if attackMode == 0:# single attack
            JTRAttacks.single(hashType = hashType,
                              hashFile = hashFile,
                              hpc = hpc)

        elif attackMode == 1:# combination attack
            JTRAttacks.combination(hashType = hashType,
                                   hashFile = hashFile,
                                   wordlists = wordlist, # (right) wordlist is a list of wordlist
                                   hpc = hpc)

        elif attackMode == 2: #wordlist attack
            JTRAttacks.wordlist(hashType = hashType,
                                hashFile = hashFile,
                                wordlist = wordlist,
                                hpc = hpc)

        elif attackMode == 3: #incremental attack
            JTRAttacks.incremental(hashType = hashType,
                                   hashFile = hashFile,
                                   hpc = hpc)

        elif attackMode == 4: #mask attack
            JTRAttacks.maskAttack(hashType = hashType,
                                  hashFile = hashFile,
                                  maskFile = maskFile,
                                  hpc = hpc)

        elif attackMode == 6: #hybrid - wordlist + mask  attack
            JTRAttacks.hybridWMF(hashType = hashType,
                                 hashFile = hashFile,
                                 wordlist = wordlist,
                                 maskFile = maskFile,
                                 hpc = hpc)

        elif attackMode == 7: #hybrid - mask + wordlist  attack
            JTRAttacks.hybridMFW(hashType = hashType,
                                 hashFile = hashFile,
                                 wordlist = wordlist,
                                 maskFile = maskFile,
                                 hpc = hpc)



    @staticmethod
    def searchHash(pattern, *, sensitive=False):
        """
        search by a valid john hash type given a pattern
        """
        if not sensitive:
            hashPattern = re.compile(rf"\w*{pattern}\w*", re.IGNORECASE)
        else:
            hashPattern = re.compile(rf"\w*{pattern}\w*")

        print_status(f"John the Ripper posible hash types(pattern: *{pattern}*)")
        for hashType in John.hashes:
            if hashPattern.search(hashType):
                print_successful(hashType)

class JTRAttacks:

    @staticmethod
    def single(*, attackMode=0, hashType, hashFile, hpc=None):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile,
                             _wordlist=wordlist)
        jtr = John()
        print_status(f"Attacking {hashFile} with {wordlist} in straigth mode.")
        if hpc:
            parallelJobType = slurm.parserParallelJob()
            if not  parallelJobType in ["MPI", "OMP"]:
                raise ParallelWorkError(parallelJobType)

            slurm, extra = hpc.parameters()
            if parallelJobType == "MPI":
                parallelWork = [f"srun mpirun {jtr.mainexec} --format={hashType} {hashFile}"]

            elif parallelJobType == "OMP":
                parallelWork = [f"srun {jtr.mainexec} --format={hashType} {hashFile}"]

            slurmScriptName = extra['slurm-script']
            HPC.genScript(slurm, extra, parallelWork)
            Bash.exec("sbatch {slurmScriptName}")

        else:
            singleAttack =   f"{jtr.mainexec} -a {attackMode} -m {hashType} {hashFile} {wordlist}"
            Bash.exec(singleAttack)

    @staticmethod
    def combination(*, attackMode=1, hashType, hashFile, wordlists=[], combinedWordlist="combined.txt", hpc=None):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile,
                             _wordlist=wordlists)


        combinedWordlistPath = Combinator.wordlist(wordlists, combinedWordlist)
        JTRAttacks.wordlist(hashType = hashType,
                            hashFile = hashFile,
                            wordlist = combinedWordlistPath)


    @staticmethod
    def wordlist(*, attackMode=2, hashType, hashFile, wordlist, hpc=None):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile,
                             _wordlist=wordlist)
        jtr = John()
        print_status(f"Attacking {hashFile} with {wordlist} wordlist in straigth mode.")
        if hpc:
            parallelJobType = slurm.parserParallelJob()
            if not  parallelJobType in ["MPI", "OMP"]:
                raise ParallelWorkError(parallelJobType)

            slurm, extra = hpc.parameters()
            if parallelJobType == "MPI":
                parallelWork = [f"srun mpirun {jtr.mainexec} --wordlist={wordlist} --format={hashType} {hashFile}"]

            elif parallelJobType == "OMP":
                parallelWork = [f"srun {jtr.mainexec} --wordlist={wordlist} --format={hashType} {hashFile}"]

            slurmScriptName = extra['slurm-script']
            HPC.genScript(slurm, extra, parallelWork)
            Bash.exec("sbatch {slurmScriptName}")

        else:
            wordlistAttack =   f"{jtr.mainexec} --wordlist={wordlist} --format={hashType} {hashFile}"
            Bash.exec(wordlistAttack)


    @staticmethod
    def incremental(*, attackMode=3, hashType, hashFile, hpc=None):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile)
        jtr = John()
        print_status(f"Attacking {hashFile} with {wordlist} in straigth mode.")
        if hpc:
            parallelJobType = slurm.parserParallelJob()
            if not  parallelJobType in ["MPI", "OMP"]:
                raise ParallelWorkError(parallelJobType)

            slurm, extra = hpc.parameters()
            if parallelJobType == "MPI":
                parallelWork = [f"srun mpirun {jtr.mainexec} --format={hashType} {hashFile}"]

            elif parallelJobType == "OMP":
                parallelWork = [f"srun {jtr.mainexec} --format={hashType} {hashFile}"]

            slurmScriptName = extra['slurm-script']
            HPC.genScript(slurm, extra, parallelWork)
            Bash.exec("sbatch {slurmScriptName}")

        else:
            incrementalAttack =   f"{jtr.mainexec} --format={hashType} {hashFile}"
            Bash.exec(incrementalAttack)


    @staticmethod
    def maskAttack(*, attackMode=4, hashType, hashFile, maskFile, hpc=None):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile,
                             _maskFile=maskFile)
        jtr = John()
        #maskFilePath = FilePath(maskFile)
        #hashFilePath = FilePath(hashFile)

        print_status(f"Attacking {hashFile} with {maskFile} in mask attack mode.")
        if hpc:
            pass
            # parallelJobType = slurm.parserParallelJob()
            # if not  parallelJobType in ["MPI", "OMP"]:
            #     raise ParallelWorkError(parallelJobType)

            # slurm, extra = hpc.parameters()
            # if parallelJobType == "MPI":
            #     parallelWork = [f"srun mpirun {jtr.mainexec} --mask={}--format={hashType} {hashFile}"]

            # elif parallelJobType == "OMP":
            #     parallelWork = [f"srun {jtr.mainexec} --format={hashType} {hashFile}"]

            # slurmScriptName = extra['slurm-script']
            # HPC.genScript(slurm, extra, parallelWork)
            # Bash.exec("sbatch {slurmScriptName}")

        else:
            with open(maskFile, 'r') as masks:
                while mask := masks.readline().rstrip():
                    if not PasswordCracker.statusHashFile(hashFilePath):
                        maskAttack =   f"{jtr.mainexec} --mask={mask} --format={hashType} {hashFile}"
                        print_status(f"Running: {maskAttack}")
                        Bash.exec(maskAttack)



    @staticmethod
    def hybridWMF(*, attackMode=6, hashType, hashFile, wordlist, maskFile, hpc=None):
        """
        hybrid attack (wordlist + mask file) attack
        """
        PasswordCracker.checkAttackArgs(_hashType = hashType,
                                        _hashFile = hashFile,
                                        _maskFile = maskFile,
                                        _wordlist = wordlist)

        jtr = John()
        print_status(f"Attacking {hashFile} with {wordlist} wordlist and {maskFile} mask file in hybrid WMF attack mode.")
        #maskFilePath = FilePath(maskFile)
        combinedWordlistPath = Combinator.hybridWMF(wordlist, maskFile)
        JTRAttacks.wordlist(hashType = hashType,
                            hashFile = hashFile,
                            wordlist = combinedWordlist,
                            hpc = hpc)

    @staticmethod
    def hybridMFW(*, attackMode=7, hashType, hashFile, wordlist, maskFile, hpc=None):
        """
        hybrid attack (mask file + wordlist) attack
        """
        PasswordCracker.checkAttackArgs(_hashType = hashType,
                                        _hashFile = hashFile,
                                        _maskFile = maskFile,
                                        _wordlist = wordlist)

        jtr = John()
        print_status(f"Attacking {hashFile} with {maskFile} mask file and {wordlist} wordlist in hybrid MFW attack mode.")
        #maskFilePath = FilePath(maskFile)
        combinedWordlistPath = Combinator.hybridMFW(maskFile, wordlist)
        JTRAttacks.wordlist(hashType = hashType,
                            hashFile = hashFile,
                            wordlist = combinedWordlist,
                            hpc = hpc)
