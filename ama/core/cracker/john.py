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


# fineprint imports
from fineprint.status import (
    print_status,
    print_failure
)

# cmd2 imports
import cmd2

# slurm imports
from ..slurm import Slurm

# cracker imports
from .cracker import PasswordCracker
from .crackedHash import CrackedHash

# john hashes import
from ama.data.hashes import jtrHashes

# core.file imports
from ..files import Path

# cracker exceptions imports
from .crackerException import (
    InvalidParallelJob,
    InvalidHashType
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
    def check_hash_type(hash_type):
        """
        Check if hash_type is a valid hash type

        Args:
            hash_type (str): hash type

        Raises:
            InvalidHashType: Error if the hasType is an unsopported hash type of a cracker
        """

        if not (hash_type in John.HASHES):
            raise InvalidHashType(John, hash_type)
        return True

    @staticmethod
    def search_hash(pattern, *, sensitive=False):
        """
        Search  john's hashes types given a pattern
        """
        if sensitive:
            hash_pattern = re.compile(rf"[\W|\w|\.]*{pattern}[\W|\w|\.]*")
        else:
            hash_pattern = re.compile(rf"[\W|\w|\.]*{pattern}[\W|\w|\.]*", re.IGNORECASE)

        filtered_hashes = []
        hashId = 0
        for hash_type in John.HASHES:
            if hash_pattern.fullmatch(hash_type):
                filtered_hashes.append((hashId, hash_type))
                hashId += 1

        print(tabulate(filtered_hashes, headers=["#", "Name"]))


    @staticmethod
    def hash_status(query_hash, potfile=None):
        """
        Check the status (broken by John or not) of query hash

        Return:
        if query_hash is in potfile then [HASHTYPE, HASH, PASSWORD] list is returned
        otherwise None is returned
        """
        #import pdb;pdb.set_trace()

        if potfile is None:
            HOME = os.path.expanduser("~")
            potfile = os.path.join(HOME, ".john/john.pot")

        try:
            permission = [os.R_OK]
            Path.access(permission, potfile)

            cracked_pattern = re.compile(rf"\$(\W*|\w*|.*)\$({query_hash})(\$(\W*|\w*|.*)\$)?:(\W*|\w*|.*)",
                                        re.DOTALL)

            with open(potfile, 'r') as john_potfile:
                while   cracked_hash := john_potfile.readline().rstrip():
                    if cracked_hashpot := cracked_pattern.fullmatch(cracked_hash):
                        hashpot = cracked_hashpot.groups()
                        return CrackedHash(hashType = hashpot[0],
                                           crackedHash= hashpot[1],
                                           password = hashpot[2],
                                           cracker = John)

            return None


        except Exception as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)

    @staticmethod
    def hashes_file_status(query_hashes_file, potfile=None):
        """
        Check the status (broken by John or not) of hashes in query_hashes_file
        """
        #import pdb; pdb.set_trace()
        hashes_status = {'cracked': [], "uncracked": []}

        if potfile is None:
            HOME = os.path.expanduser("~")
            potfile = os.path.join(HOME, ".john/john.pot")

        try:
            permission = [os.R_OK]
            Path.access(permission, potfile, query_hashes_file)


            with open(query_hashes_file, 'r') as hashes_file:
                while query_hash := hashes_file.readline().rsplit():
                    if cracker_hash := John.hash_status(queryHash[0]):
                        hashes_status['cracked'].append(cracker_hash.getAttributes())
                    else: #crackedHash is uncracked
                        hashes_status['uncracked'].append([query_hash])

            return hashes_status

        except Exception as error:
            #cmd2.Cmd.pexcept(error, "ERROR")
            print_failure(error)


    def benchmark(self, slurm=None):
        """
        Run john benchmark
        """
        #import pdb; pdb.set_trace()
        if self.enable:
            #cmd2.Cmd.poutput(f"Performing John Benchmark.")
            #print_status(f"Performing John Benchmark.")
            if slurm.partition:
                parallel_job_type = slurm.parallel_job_parser()
                if not  parallel_job_type in ["MPI", "OMP"]:
                    raise InvalidParallelJob(parallel_job_type)

                #core, extra = slurm.parameters()
                if parallel_job_type == "MPI":
                    parallel_work = [
                        (
                            f"srun --mpi={slurm.pmix}"
                            f" {self.main_exec} --test"
                        )
                    ]

                elif parallel_job_type == "OMP":
                    parallel_work = [
                            f"{self.main_exec} --test"
                    ]


                batch_script_name = slurm.gen_batch_script(parallel_work)

                Bash.exec(f"sbatch {batch_script_name}")

            else:
                john_benchmark = f"{self.main_exec} --test"
                Bash.exec(john_benchmark)
        else:
            #cmd2.Cmd.pwarning(f"Cracker {self.mainName} is disable")
            print_failure(f"Cracker {self.main_name} is disable")

    
    def wordlist_attack(self , *, hash_type, hashes_file, wordlist, slurm=None):
        """
        Wordlist attack using john submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Jonh's hash type
        hashesfile (str): Hash file to attack
        wordlist (str): wordlist to attack
        slurm (Slurm): Instance of Slurm class
        """
        import pdb; pdb.set_trace()
        if self.enable:
            try:
                permission = [os.R_OK]
                Path.access(permission, hashes_file, wordlist)
                John.check_hash_type(hash_type)

                #cmd2.Cmd.poutput(f"Attacking {hash_type} hashes in {hashesfile} file with {wordlist} wordlist.")
                print_status(f"Attacking {hash_type} hashes in {hashes_file} file with {wordlist} wordlist")
                if slurm.partition:
                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["MPI", "OMP"]:
                        raise InvalidParallelJob(parallel_job_type)

                    #core, extra = slurm.parameters()
                    if parallel_job_type == "MPI":
                        parallel_work = [
                            (
                                f"srun --mpi={slurm.pmix}"
                                f" {self.main_exec} --wordlist={wordlist}"
                                f" --format={hash_type} {hashes_file}"
                            )
                        ]

                    elif parallel_job_type == "OMP":
                        parallel_work = [
                            (
                                f"{self.main_exec}"
                                f" --wordlist={wordlist}"
                                f" --format={hash_type}"
                                f" {hashes_file}"
                            )
                        ]

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    wordlist_attack =  (
                        f"{self.main_exec}"
                        f" --wordlist={wordlist}"
                        f" --format={hash_type}"
                        f" {hashes_file}"
                    )
                    Bash.exec(wordlist_attack)
            except Exception as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

        else:
            #cmd2.Cmd.pwarning("Cracker {self.main_name} is disable")
            print_failure("Cracker {self.main_name} is disable")


    def combination_attack(self,* , hashType, hashesFile, wordlists=[], slurm=None,
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
    def incremental_attack(self, *, hash_type, hashes_file, slurm=None):
        """
        Incemental attack using john submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Jonh's hash type
        hashes_file (str): Hash file to attack
        slurm (Slurm): Instance of Slurm class
        """

        import pdb; pdb.set_trace()

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
                                    f" {self.mainexec} --incremental"
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
                                    f" {self.mainexec} --single"
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
