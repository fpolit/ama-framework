#!/usr/bin/env python3
# John class
#
# Jan 9 2021
## Implementation of John class
#  using core module of john python package
#
# Jan 18 2021
## wordlist attack JTRAttacks debugged
# There is a problem when submitting a MPI parallel job in slurm. It exits with error
# So submit again it solve the problem (with sbatch).
#
#
# Maintainer: Gustavo Lozano <glozanoa@uni.pe>

import os
import re
from tabulate import tabulate
from sbash.core import Bash
from fineprint.status import print_status, print_failure, print_successful

# cracker modules
from .PasswordCracker import PasswordCracker

from .PasswordCrackerExceptions import CrackerHashError

# hashes modules
from ..hashes.jtr import hashes

# base module
from ..base.FilePath import FilePath
from ..base.Mask import Mask

# hpc module
from ..hpc.HPC import HPC

# hpc exceptions
from ..hpc.HPCExceptions import ParallelWorkError

# utilities module
from ..utilities.combinator import Combinator
from ..utilities.combinator import InvalidWordlistNumber


class John(PasswordCracker):
    hashes = hashes

    attackMode = {0:"Wordlist",
                  1:"Combination",
                  2:"Incremental",
                  3:"Mask",
                  #4:"Single",
                  6:"Hybrid:\n\twordlist + masks file or mask",
                  7:"Hybrid:\n\tmasks file or mask + wordlist"}

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
            raise CrackerDisableError("john")



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
                        _wordlist=None, #can be a list of wordlists
                        _masksFile=None):

        PasswordCracker.checkAttackArgs(_hashFile = _hashFile,
                                        _wordlist = _wordlist,
                                        _masksFile = _masksFile)

        John.checkHashType(_hashType)

    @staticmethod
    def selectAttack(*,
                attackMode=None,
                hashType=None,
                hashFile=None,
                wordlist=[],
                masksFile=None,
                hpc = None):

        # contruction of hashcat cmd to execute
        John.checkAttackMode(attackMode)
        if attackMode == 0: #wordlist attack
            wordlist = wordlist[0]
            JTRAttacks.wordlist(hashType = hashType,
                                hashFile = hashFile,
                                wordlist = wordlist,
                                hpc = hpc)


        elif attackMode == 1:# combination attack
            JTRAttacks.combination(hashType = hashType,
                                   hashFile = hashFile,
                                   wordlists = wordlist, # (right) wordlist is a list of wordlist
                                   hpc = hpc)


        elif attackMode == 2: #incremental attack
            JTRAttacks.incremental(hashType = hashType,
                                   hashFile = hashFile,
                                   hpc = hpc)


        elif attackMode == 3: #mask attack
            JTRAttacks.maskAttack(hashType = hashType,
                                  hashFile = hashFile,
                                  masksFile = masksFile,
                                  hpc = hpc)


        elif attackMode == 4:# single attack
            JTRAttacks.single(hashType = hashType,
                              hashFile = hashFile,
                              hpc = hpc)

        elif attackMode == 6: #hybrid - wordlist + mask  attack
            JTRAttacks.hybridWMF(hashType = hashType,
                                 hashFile = hashFile,
                                 wordlist = wordlist,
                                 masksFile = masksFile,
                                 hpc = hpc)

        elif attackMode == 7: #hybrid - mask + wordlist  attack
            JTRAttacks.hybridMFW(hashType = hashType,
                                 hashFile = hashFile,
                                 wordlist = wordlist,
                                 masksFile = masksFile,
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

        print_status(f"Posible John the Ripper hashes(pattern: *{pattern}*)")
        posibleHashes = []
        for hashType in John.hashes:
            if hashPattern.search(hashType):
                posibleHashes.append([hashType])

        print(tabulate(posibleHashes, headers=["name"]))

class JTRAttacks:

    # debugged
    @staticmethod
    def wordlist(*, attackMode=0, hashType, hashFile, wordlist, hpc=None):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile,
                             _wordlist=wordlist)
        jtr = John()
        print_status(f"Attacking {hashType} hashes in {hashFile} file with {wordlist} wordlist.")
        if hpc.partition:
            parallelJobType = hpc.parserParallelJob()
            if not  parallelJobType in ["MPI", "OMP"]:
                raise ParallelWorkError(parallelJobType)

            slurm, extra = hpc.parameters()
            if parallelJobType == "MPI":
                parallelWork = [f"srun --mpi=pmix_v3 {jtr.mainexec} --wordlist={wordlist} --format={hashType} {hashFile}"]

            elif parallelJobType == "OMP":
                parallelWork = [f"{jtr.mainexec} --wordlist={wordlist} --format={hashType} {hashFile}"]


            HPC.genScript(slurm, extra, parallelWork)

            slurmScriptName = extra['slurm-script']
            Bash.exec(f"sbatch {slurmScriptName}")

        else:
            wordlistAttack =   f"{jtr.mainexec} --wordlist={wordlist} --format={hashType} {hashFile}"
            Bash.exec(wordlistAttack)

    #debugged
    @staticmethod
    def combination(*, attackMode=1, hashType, hashFile, wordlists=[], combinedWordlist="combined.txt", hpc=None):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile,
                             _wordlist=wordlists)


        Combinator.wordlist(wordlists, combinedWordlist)
        JTRAttacks.wordlist(hashType = hashType,
                            hashFile = hashFile,
                            wordlist = combinedWordlist,
                            hpc = hpc)


    #debugged
    @staticmethod
    def incremental(*, attackMode=2, hashType, hashFile, hpc=None):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile)
        jtr = John()
        print_status(f"Attacking {hashType} hashes in {hashFile} file in incremental mode.")
        if hpc.partition:
            parallelJobType = hpc.parserParallelJob()
            if not  parallelJobType in ["MPI", "OMP"]:
                raise ParallelWorkError(parallelJobType)

            slurm, extra = hpc.parameters()
            if parallelJobType == "MPI":
                parallelWork = [f"srun --mpi=pmix_v3 {jtr.mainexec} --format={hashType} {hashFile}"]

            elif parallelJobType == "OMP":
                parallelWork = [f"{jtr.mainexec} --format={hashType} {hashFile}"]

            HPC.genScript(slurm, extra, parallelWork)

            slurmScriptName = extra['slurm-script']
            Bash.exec(f"sbatch {slurmScriptName}")

        else:
            incrementalAttack =   f"{jtr.mainexec} --format={hashType} {hashFile}"
            Bash.exec(incrementalAttack)


    @staticmethod
    def maskAttack(*, attackMode=3, hashType, hashFile, masksFile, hpc=None):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile,
                             _masksFile=masksFile)
        jtr = John()

        print_status(f"Attacking {hashType} hashes in {hashFile} file with {masksFile} mask file.")
        if hpc.partition:
            print_failure("No supported yet")

        else:
            with open(masksFile, 'r') as masks:
                while mask := masks.readline().rstrip():
                    cracked = PasswordCracker.hashFileStatus(jtr.getName(), hashFile)
                    if not cracked:
                        maskAttack =   f"{jtr.mainexec} --mask={mask} --format={hashType} {hashFile}"
                        print_status(f"\nRunning: {maskAttack}")
                        Bash.exec(maskAttack)

            PasswordCracker.reportHashesFileStatus(hashFIle)

    # @staticmethod
    # def single(*, attackMode=4, hashType, hashFile, hpc=None):
    #     John.checkAttackArgs(_hashType=hashType,
    #                          _hashFile=hashFile,
    #                          _wordlist=wordlist)
    #     jtr = John()
    #     print_status(f"Attacking {hashType} hashes in {hashFile} hash file in straigth  mode.")
    #     if hpc.partition:
    #         parallelJobType = hpc.parserParallelJob()
    #         if not  parallelJobType in ["MPI", "OMP"]:
    #             raise ParallelWorkError(parallelJobType)

    #         slurm, extra = hpc.parameters()
    #         if parallelJobType == "MPI":
    #             parallelWork = [f"srun mpirun {jtr.mainexec} --format={hashType} {hashFile}"]

    #         elif parallelJobType == "OMP":
    #             parallelWork = [f"{jtr.mainexec} --format={hashType} {hashFile}"]

    #         slurmScriptName = extra['slurm-script']
    #         HPC.genScript(slurm, extra, parallelWork)
    #         #Bash.exec("sbatch {slurmScriptName}")

    #     else:
    #         singleAttack =   f"{jtr.mainexec} -a {attackMode} -m {hashType} {hashFile} {wordlist}"
    #         #Bash.exec(singleAttack)

    @staticmethod
    def hybridWMF(*, attackMode=6, hashType, hashFile, wordlist, masksFile, hpc=None):
        """
        hybrid attack (wordlist + mask file) attack
        """
        John.checkAttackArgs(_hashType = hashType,
                             _hashFile = hashFile,
                             #_masksFile = masksFile,
                             _wordlist = wordlist)

        print_status(f"Attacking {hashType} hashes in {hashFile} file with an hybrid MFW attack.")
        hybridWordlist = "hybrid.txt"

        if Mask.isMask(masksFile): # masksFile is a simple mask
            wordlist = wordlist[0]
            mask = masksFile
            with open(hybridWordlist, 'w') as outputFile:
                Combinator.genHybridWM(wordlist, mask , outputFile, inverse=False)
            print_successful(f"Combinated wordlist and mask was generated: {hybridWordlist}")

        else:
            wordlist = wordlist[0]
            Combinator.hybridWMF(wordlist  = wordlist,
                                 masksFile = masksFile,
                                 output    = hybridWordlist)

        JTRAttacks.wordlist(hashType = hashType,
                            hashFile = hashFile,
                            wordlist = hybridWordlist,
                            hpc = hpc)

    @staticmethod
    def hybridMFW(*, attackMode=7, hashType, hashFile, wordlist, masksFile, hpc=None):
        """
        hybrid attack (mask file + wordlist) attack
        """
        John.checkAttackArgs(_hashType = hashType,
                             _hashFile = hashFile,
                             #_masksFile = masksFile,
                             _wordlist = wordlist)

        #jtr = John()
        print_status(f"Attacking {hashType} hashes in {hashFile} hash with an hybrid MFW attack.")
        hybridWordlist = "hybrid.txt"

        if Mask.isMask(masksFile): # masksFile is a simple mask
            mask = masksFile
            with open(hybridWordlist, 'w') as outputFile:
                Combinator.genHybridWM(wordlist, mask , outputFile, inverse=True)
            print_successful(f"Combinated mask and wordlist was generated: {hybridWordlist}")

        else:
            Combinator.hybridMFW(masksFile = masksFile,
                                 wordlist  = wordlist,
                                 output    = hybridWordlist)

        JTRAttacks.wordlist(hashType = hashType,
                            hashFile = hashFile,
                            wordlist = hybridWordlist,
                            hpc = hpc)
