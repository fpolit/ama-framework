#!/usr/bin/env python3
# John class
#
# Jan 9 2021
# Implementation of John class
# using core module of john python package
#
#
# Jan 18 2021 (Feb 22 2021 SOLVED BUG: Install openmpi with pmix support)
# wordlist attack JTRAttacks debugged
# There is a problem when submitting a MPI parallel job in slurm. It exits with error
#
#
# Feb 22 2021
# Reimplementation of John cracker (inheritance of PasswordCracker class)
# Implementing John as a cracker for ama-framework
#
# Maintainer: glozanoa <glozanoa@uni.pe>


import os
import re
from tabulate import tabulate
from sbash import Bash

# cmd2 imports
import cmd2

# slurm imports
from ..slurm import Slurm

# cracker imports
from .cracker import PasswordCracker

# john hashes import
from ama.data.hashes import jtrHashes

# core.file imports
from ..files import Path

# cracker exceptions imports
from .crackerException import (
    InvalidParallelJobError,
    InvalidHashTypeError
)

class John(PasswordCracker):
    """
    John password cracker
    This class implement the diverse attack of john the ripper and its benchmark
    Suported Attacks: wordlist, incremental, masks, single, combination, hybrid
    """

    HASHES = jtrHashes

    def __init__(self):
        super().__init__(["john", "jtr"], version="1.9.0-jumbo-1 MPI + OMP")


    @staticmethod
    def checkHashType(hashType):
        """
        Check if hashType is a valid hash type

        Args:
            hashType (str): hash type

        Raises:
            InvalidHashType: Error if the hasType is an unsopported hash type of a cracker
        """

        if not (hashType in John.HASHES):
            raise InvalidHashTypeError(John, hashType)
        return True

    @staticmethod
    def searchHash(pattern, *, sensitive=False):
        """
        Search  john's hashes types given a pattern
        """
        if not sensitive:
            hashPattern = re.compile(rf"\w*{pattern}\w*", re.IGNORECASE)
        else:
            hashPattern = re.compile(rf"\w*{pattern}\w*")

        filteredhashes = []
        hashId = 0
        for hashType in John.hashes:
            if hashPattern.fullmatch(hashType):
                filteredhashes.append(hashId, hashType)
                hashId += 1

        cmd2.Cmd.poutput(tabulate(filteredhashes, headers=["#", "Name"]))


    @staticmethod
    def hashStatus(queryHash, potfile=None):
        """
        Check the status (broken by John or not) of query hash or hashes file

        Return:
        if queryHash is in potfile then [HASHTYPE, HASH, PASSWORD] list is returned
        otherwise None is returned
        """
        #import pdb;pdb.set_trace()

        try:
            crackedPattern = re.compile(rf"\$(\W*|\w*|.*)\$({queryHash})(\$(\W*|\w*|.*)\$)?:(\W*|\w*|.*)", re.DOTALL)
            if potfile:
                permission = [os.R_OK]
                Path.access(permission, potfile)

                # elif cracker in ["hashcat", "hc"]:
                #     crackedPattern = re.compile(rf"({queryHash}):(\W*|\w*|.*)", re.DOTALL)

            else:
                HOME = os.path.expanduser("~")
                potfile = os.path.join(HOME, ".john/john.pot")
                permission = [os.R_OK]
                Path.access(permission, potfile)

                # elif cracker in ["hashcat", "hc"]:
                #     hashcatPotFile = os.path.join(homePath, ".hashcat/hashcat.potfile")
                #     potFilePath = FilePath(hashcatPotFile)
                #     crackedPattern = re.compile(rf"({queryHash}):(\W*|\w*|.*)", re.DOTALL)

            #print(f"potfile: {potFilePath}")
            with open(potfile, 'r') as potFile:
                while   crackedHash := potFile.readline().rstrip():
                    if crackedHashPot := crackedPattern.fullmatch(crackedHash):
                        hashPot = crackedHashPot.groups()
                        return [hashPot[0], hashPot[1], hashPot[-1]]
                        # elif cracker in ["hashcat", "hc"]:
                        #     return [None, hashPot[0], hashPot[1]]
            return None


        except Exception as error:
            cmd2.Cmd.pexcept(error)


    def benchmark(self, slurm=None):
        """
            Run john benchmark
        """
        if self.status:
            cmd2.Cmd.poutput(f"Performing John Benchmark.")
            if slurm.partition:
                parallelJobType = slurm.parserParallelJob()
                if not  parallelJobType in ["MPI", "OMP"]:
                    raise InvalidParallelJobError(parallelJobType)

                core, extra = slurm.parameters()
                if parallelJobType == "MPI":
                    parallelWork = [
                        (
                            f"srun --mpi={slurm.pmix}"
                            f" {self..mainexec} -b"
                        )
                    ]

                elif parallelJobType == "OMP":
                    parallelWork = [
                            f"{self.mainexec} -b"
                    ]


                Slurm.genScript(core, extra, parallelWork)

                slurmScriptName = extra['slurm-script']
                Bash.exec(f"sbatch {slurmScriptName}")

            else:
                johnBenchmark = f"{self.mainexec} -b"
                Bash.exec(johnBenchmark)
        else:
            cmd2.Cmd.pwarning("Cracker {self.mainName} is disable")


    def wordlistAttack(self , *, hashType, hashesFile, wordlist, slurm=None):
        """
        Wordlist attack using john submiting parallel tasks in a cluster with Slurm

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hash file to attack
        wordlist (str): wordlist to attack
        slurm (Slurm): Instance of Slurm class
        """

        if self.status:
            try:
                permission = [os.R_OK]
                access2args = Path.access(permission, hashesFile, wordlist)
                validHash = John.checkHashType(hashType)
                if  access2args and validHash:
                    cmd2.Cmd.poutput(f"Attacking {hashType} hashes in {hashesFile} file with {wordlist} wordlist.")
                    if slurm.partition:
                        parallelJobType = slurm.parserParallelJob()
                        if not  parallelJobType in ["MPI", "OMP"]:
                            raise InvalidParallelJobError(parallelJobType)

                        core, extra = slurm.parameters()
                        if parallelJobType == "MPI":
                            parallelWork = [
                                (
                                    f"srun --mpi={slurm.pmix}"
                                    f" {self..mainexec} --wordlist={wordlist}"
                                    f" --format={hashType} {hashesFile}"
                                )
                            ]

                        elif parallelJobType == "OMP":
                            parallelWork = [
                                (
                                    f"{self.mainexec}"
                                    f" --wordlist={wordlist}"
                                    f" --format={hashType}"
                                    f" {hashesFile}"
                                )
                            ]

                        Slurm.genScript(core, extra, parallelWork)
                        slurmScriptName = extra['slurm-script']
                        Bash.exec(f"sbatch {slurmScriptName}")

                    else:
                        wordlistAttack =  (
                            f"{self.mainexec}"
                            f" --wordlist={wordlist}"
                            f" --format={hashType}"
                            f" {hashesFile}"
                        )
                        Bash.exec(wordlistAttack)

            except Exception as error:
                cmd2.Cmd.pexcept(error)

        else:
            cmd2.Cmd.pwarning("Cracker {self.mainName} is disable")


    def combinationAttack(self,* , hashType, hashesFile, wordlists=[], slurm=None,
                          combinedWordlist="combined.txt"):
        # John.checkAttackArgs(_hashType=hashType,
        #                      _hashFile=hashFile,
        #                      _wordlist=wordlists)


        # POOR PERFORMANCE IN Combinator.wordlist (rewrite a better combinator)
        Combinator.wordlist(wordlists, combinedWordlist)
        self.wordlistAttack(hashType=hashType,
                            hashesFile=hashesFile,
                            wordlist=combinedWordlist)

    #NOTE: John continue when the hash was cracked
    def incrementalAttack(self, *, hashType, hashesFile, slurm=None):
        """
        Incemental attack using john submiting parallel tasks in a cluster with Slurm

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hash file to attack
        slurm (Slurm): Instance of Slurm class
        """

        if self.status:
            try:
                permission = [os.R_OK]
                access2args = Path.access(permission, hashesFile)
                validHash = John.checkHashType(hashType)
                if  access2args and validHash:
                    cmd2.Cmd.poutput(f"Attacking {hashType} hashes in {hashesFile} using incremental attack.")
                    if slurm.partition:
                        parallelJobType = slurm.parserParallelJob()
                        if not  parallelJobType in ["MPI", "OMP"]:
                            raise InvalidParallelJobError(parallelJobType)

                        core, extra = slurm.parameters()
                        if parallelJobType == "MPI":
                            parallelWork = [
                                (
                                    f"srun --mpi={slurm.pmix}"
                                    f" {self..mainexec} --incremental"
                                    f" --format={hashType} {hashesFile}"
                                )
                            ]

                        elif parallelJobType == "OMP":
                            parallelWork = [
                                (
                                    f"{self.mainexec}"
                                    f" --incremental"
                                    f" --format={hashType}"
                                    f" {hashesFile}"
                                )
                            ]

                        Slurm.genScript(core, extra, parallelWork)
                        slurmScriptName = extra["slurm-script"]
                        Bash.exec(f"sbatch {slurmScriptName}")

                    else:
                        wordlistAttack =  (
                            f"{self.mainexec}"
                            f" --incremental"
                            f" --format={hashType}"
                            f" {hashesFile}"
                        )
                        Bash.exec(wordlistAttack)

            except Exception as error:
                cmd2.Cmd.pexcept(error)

        else:
            cmd2.Cmd.pwarning("Cracker {self.mainName} is disable")


    def masksAttack(self, *, hashType, hashesFile, masksFile, slurm=None):
        # John.checkAttackArgs(_hashType=hashType,
        #                      _hashFile=hashFile,
        #                      _masksFile=masksFile)

        print_successful(f"Attacking {hashType} hashes in {hashesFile} file with {masksFile} mask file.")
        if slurm.partition:
            maskAttackScript = "maskAttack.py"
            John.genMaskAttack(hashType = hashType,
                               hashesFile = hashFile,
                               masksFile = masksFile,
                               hpc = hpc,
                               maskAttackScript = maskAttackScript)

            parallelWork = [f"python3 {maskAttackScript}"]
            slurm, extra = hpc.parameters()
            slurmScriptName = extra['slurm-script']
            HPC.genScript(slurm, extra, parallelWork)
            Bash.exec(f"sbatch {slurmScriptName}")

        else:
            with open(masksFile, 'r') as masks:
                while mask := masks.readline().rstrip():
                    cracked = PasswordCracker.hashFileStatus(jtr.getName(), hashFile)
                    if not cracked:
                        maskAttack =   f"{jtr.mainexec} --mask={mask} --format={hashType} {hashFile}"
                        print_status(f"\nRunning: {maskAttack}")
                        Bash.exec(maskAttack)

            PasswordCracker.reportHashesFileStatus(hashFIle)

    # tested
    @staticmethod
    def genMaskAttack(*, hashType, hashesFile, masksFile, slurm, maskAttackScript="maskAttack.py"):
        _mask = "{mask}"
        _jtr_mainexec = "{jtr.mainexec}"
        _attack = "{attack}"
        _masksFile = f"'{masksFile}'"
        _hashesFile = f"'{hashesFile}'"
        _attack_msg = "{attack_msg}"


        parallelJobType = hpc.parserParallelJob()
        if not  parallelJobType in ["MPI", "OMP"]:
            raise ParallelWorkError(parallelJobType)

        slurm, extra = hpc.parameters()
        #maskAttack = ""
        if parallelJobType == "MPI":
            maskAttack = f"""
#!/bin/env python3

from hattack.cracker.PasswordCracker import PasswordCracker
from hattack.cracker.John import John
from sbash.core import Bash

jtr = John()

with open({_masksFile}, 'r') as masks:
    while mask := masks.readline().rstrip():
        cracked = PasswordCracker.hashFileStatus(jtr.getName(), {_hashesFile})
        if not cracked:
            attack =   f"srun --mpi={hpc.pmix} {_jtr_mainexec} --mask={_mask} --format={hashType} {hashesFile}"
            attack_msg = f"Running: {_attack}"
            Bash.exec(f"echo {_attack_msg}")
            Bash.exec(attack)
            """


        elif parallelJobType == "OMP":
            maskAttack =f"""
#!/usr/bin/env python3

from hattack.cracker.PasswordCracker import PasswordCracker
from hattack.cracker.John import John
from sbash.core import Bash

jtr = John()

with open({_masksFile}, 'r') as masks:
    while mask := masks.readline().rstrip():
        cracked = PasswordCracker.hashFileStatus(jtr.getName(), {_hashesFile})
        if not cracked:
            attack =   f"srun {_jtr_mainexec} --mask={_mask} --format={hashType} {hashesFile}"
            attack_msg = f"Running: {_attack}"
            Bash.exec(f"echo {_attack_msg}")
            Bash.exec(attack)
            """

        with open(maskAttackScript, 'w') as attack:
            attack.write(maskAttack)

        print_status(f"Mask attack script generated: {maskAttackScript}")


    def singleAttack(self, *, hashType, hashesFile, slurm=None):
        """
        Single attack using john submiting parallel tasks in a cluster with Slurm

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hashes file to attack
        slurm (Slurm): Instance of Slurm class
        """

        if self.status:
            try:
                permission = [os.R_OK]
                access2args = Path.access(permission, hashFile)
                validHash = John.checkHashType(hashType)
                if  access2args and validHash:
                    cmd2.Cmd.poutput(f"Attacking {hashType} hashes in {hashesFile} using single attack.")
                    if slurm.partition:
                        parallelJobType = slurm.parserParallelJob()
                        if not  parallelJobType in ["MPI", "OMP"]:
                            raise InvalidParallelJobError(parallelJobType)

                        core, extra = slurm.parameters()
                        if parallelJobType == "MPI":
                            parallelWork = [
                                (
                                    f"srun --mpi={slurm.pmix}"
                                    f" {self..mainexec} --single"
                                    f" --format={hashType} {hashesFile}"
                                )
                            ]

                        elif parallelJobType == "OMP":
                            parallelWork = [
                                (
                                    f"{self.mainexec}"
                                    f" --single"
                                    f" --format={hashType}"
                                    f" {hashesFile}"
                                )
                            ]

                        Slurm.genScript(core, extra, parallelWork)
                        slurmScriptName = extra["slurm-script"]
                        Bash.exec(f"sbatch {slurmScriptName}")

                    else:
                        wordlistAttack =  (
                            f"{self.mainexec}"
                            f" --single"
                            f" --format={hashType}"
                            f" {hashesFile}"
                        )
                        Bash.exec(wordlistAttack)

            except Exception as error:
                cmd2.Cmd.pexcept(error)
        else:
            cmd2.Cmd.pwarning("Cracker {self.mainName} is disable")


    def hybridAttack(self, *, hashType, hashesFile, wordlist, masksFile, slurm=None, inverse=False):
        """
        hybrid attack

        Combine wordlist + masks file (by default, when inverse=False) in other file and
        perform a wordlist attack with that file, if inverse=True combine masks file + wordlist
        """
        # John.checkAttackArgs(_hashType = hashType,
        #                      _hashFile = hashFile,
        #                      #_masksFile = masksFile,
        #                      _wordlist = wordlist)


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

    # @staticmethod
    # def hybridMFW(*, attackMode=7, hashType, hashFile, wordlist, masksFile, hpc=None):
    #     """
    #     hybrid attack (mask file + wordlist) attack
    #     """
    #     John.checkAttackArgs(_hashType = hashType,
    #                          _hashFile = hashFile,
    #                          #_masksFile = masksFile,
    #                          _wordlist = wordlist)

    #     #jtr = John()
    #     print_status(f"Attacking {hashType} hashes in {hashFile} hash with an hybrid MFW attack.")
    #     hybridWordlist = "hybrid.txt"

    #     if Mask.isMask(masksFile): # masksFile is a simple mask
    #         mask = masksFile
    #         with open(hybridWordlist, 'w') as outputFile:
    #             Combinator.genHybridWM(wordlist, mask , outputFile, inverse=True)
    #         print_successful(f"Combinated mask and wordlist was generated: {hybridWordlist}")

    #     else:
    #         Combinator.hybridMFW(masksFile = masksFile,
    #                              wordlist  = wordlist,
    #                              output    = hybridWordlist)

    #     JTRAttacks.wordlist(hashType = hashType,
    #                         hashFile = hashFile,
    #                         wordlist = hybridWordlist,
    #                         hpc = hpc)
