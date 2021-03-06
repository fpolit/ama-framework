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
# Mar 1 2021
# Debug of ama attack module:
# john_benchmark, john_wordlist, john_single, john_incremental, john_masks
#
# Maintainer: glozanoa <glozanoa@uni.pe>


import os
import re
from tabulate import tabulate
from sbash import Bash


# fineprint imports
from fineprint.status import (
    print_status,
    print_failure,
    print_successful
)

# cmd2 imports
import cmd2

# slurm imports
from ...slurm import Slurm

# cracker imports
from .cracker import PasswordCracker
from .crackedHash import CrackedHash

# john hashes import
from ama.data.hashes import jtrHashes

# core.file imports
from ...files import Path

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
    MAINNAME = "john"

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


    # debugged - date: Mar 1 2021
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
    def hash_status(query_hash: str, potfile: str = None):
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
                while cracked_hash := john_potfile.readline().rstrip():
                    if cracked_hashpot := cracked_pattern.fullmatch(cracked_hash):
                        hashpot = cracked_hashpot.groups()
                        return CrackedHash(hash_type = hashpot[0],
                                           cracked_hash= hashpot[1],
                                           password = hashpot[-1],
                                           cracker = John)
            return None


        except Exception as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)

    def are_all_hashes_cracked(hashes_file: str, potfile: str = None):
        """
        Check if all hashes are cracked
        return True if all hashes were cracked otherwise return False
        """
        all_cracked = True
        with open(hashes_file, 'r') as hashes:
            while query_hash := hashes.readline().rstrip():
                if John.hash_status(query_hash, potfile) is None: # query_hash isn't cracked yet
                    all_cracked = False
                    break

        return all_cracked


    @staticmethod
    def hashes_file_status(query_hashes_file, potfile=None):
        """
        Check the status (broken by John or not) of hashes in query_hashes_file
        and return the cracked and uncracked hashes
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
                    query_hash = query_hash[0]
                    if cracker_hash := John.hash_status(query_hash):
                        hashes_status['cracked'].append(cracker_hash.getAttributes())
                    else: #crackedHash is uncracked
                        hashes_status['uncracked'].append([query_hash])

            return hashes_status

        except Exception as error:
            #cmd2.Cmd.pexcept(error, "ERROR")
            print_failure(error)

    # debugged - date: Feb 28 2021
    def benchmark(self,  slurm=None):
        """
        Run john benchmark
        """
        #import pdb; pdb.set_trace()
        if self.enable:
            #cmd2.Cmd.poutput(f"Performing John Benchmark.")
            #print_status(f"Performing John Benchmark.")
            if slurm and slurm.partition:
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

    # debugged - date: Feb 28 2021
    def wordlist_attack(self , *,
                        hash_type: str , hashes_file: str, wordlist: str,
                        slurm):
        """
        Wordlist attack using john submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Jonh's hash type
        hashes_file (str): Hash file to attack
        wordlist (str): wordlist to attack
        slurm (Slurm): Instance of Slurm class
        """
        #import pdb; pdb.set_trace()
        if self.enable:
            try:
                permission = [os.R_OK]
                Path.access(permission, hashes_file, wordlist)
                John.check_hash_type(hash_type)

                #cmd2.Cmd.poutput(f"Attacking {hash_type} hashes in {hashesfile} file with {wordlist} wordlist.")
                print_status(f"Attacking {hash_type} hashes in {hashes_file} file with {wordlist} wordlist")
                if slurm and slurm.partition:
                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["MPI", "OMP"]:
                        raise InvalidParallelJob(parallel_job_type)

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

                    # if report: # show attack report
                    #     from ama.core.modules.auxiliary.hashes import HashesStatus
                    #     attack_report = HashesStatus(hashes_file=hashes_file)
                    #     print("\n Wordlist attack report:\n")
                    #     attack_report.run()

            except Exception as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

        else:
            #cmd2.Cmd.pwarning("Cracker {self.main_name} is disable")
            print_failure("Cracker {self.main_name} is disable")


    def combination_attack(self,* , hashType, hashesFile, wordlists=[], slurm,
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
    # debugged - date: Feb 28 2021
    def incremental_attack(self, *,
                           hash_type: str, hashes_file: str,
                           slurm):
        """
        Incemental attack using john submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): John's hash type
        hashes_file (str): Hash file to attack
        slurm (Slurm): Instance of Slurm class
        """

        #import pdb; pdb.set_trace()

        if self.enable:
            try:
                permission = [os.R_OK]
                Path.access(permission, hashes_file)
                John.check_hash_type(hash_type)
                #cmd2.Cmd.poutput(f"Attacking {hashType} hashes in {hashesFile} using incremental attack.")
                print_status(f"Attacking {hash_type} hashes in {hashes_file} using incremental attack.")
                if slurm and slurm.partition:
                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["MPI", "OMP"]:
                        raise InvalidParallelJob(parallel_job_type)

                    #core, extra = slurm.parameters()
                    if parallel_job_type == "MPI":
                        parallel_work = [
                            (
                                f"srun --mpi={slurm.pmix}"
                                f" {self.main_exec} --incremental"
                                f" --format={hash_type} {hashes_file}"
                            )
                        ]

                    elif parallel_job_type == "OMP":
                        parallel_work = [
                            (
                                f"{self.main_exec}"
                                f" --incremental"
                                f" --format={hash_type}"
                                f" {hashes_file}"
                            )
                        ]

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    incremental_attack =  (
                        f"{self.main_exec}"
                        f" --incremental"
                        f" --format={hash_type}"
                        f" {hashes_file}"
                    )
                    Bash.exec(incremental_attack)

            except Exception as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

        else:
            #cmd2.Cmd.pwarning("Cracker {self.mainName} is disable")
            print_failure("Cracker {self.main_name} is disable")


    # debugged - date: Mar 1 2021
    def masks_attack(self, *,
                     hash_type: str, hashes_file: str, masks_file: str,
                     masks_attack_script: str, slurm):
        """
        Masks attack using john submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): John's hash type
        hashes_file (str): Hash file to attack
        masks_file (str): Masks file
        mask_attack_script (str): Name for generated mask attack script
        slurm (Slurm): Instance of Slurm class
        """

        #import pdb; pdb.set_trace()

        if self.enable:
            try:
                permission = [os.R_OK]
                Path.access(permission, hashes_file, masks_file)
                John.check_hash_type(hash_type)

                print_status(f"Attacking {hash_type} hashes in {hashes_file} file with {masks_file} mask file.")
                if slurm and slurm.partition:
                    John.gen_masks_attack(hash_type = hash_type,
                                          hashes_file = hashes_file,
                                          masks_file = masks_file,
                                          masks_attack_script = masks_attack_script,
                                          slurm = slurm)

                    parallel_work = [f"python3 {masks_attack_script}"]
                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    with open(masks_file, 'r') as masks:
                        while mask := masks.readline().rstrip():
                            all_cracked = John.are_all_hashes_cracked(hashes_file)
                            if not all_cracked:
                                mask_attack =  (
                                    f"{self.main_exec} --mask={mask}"
                                    f" --format={hash_type} {hashes_file}"
                                )
                                print()
                                print_status(f"Running: {mask_attack}")
                                Bash.exec(mask_attack)
                            else:
                                break

            except Exception as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

        else:
            #cmd2.Cmd.pwarning("Cracker {self.main_name} is disable")
            print_failure("Cracker {self.main_name} is disable")


    #debugged - date: Mar 1 2021
    @staticmethod
    def gen_masks_attack(*,
                         hash_type: str, hashes_file: str, masks_file: str,
                         masks_attack_script: str, slurm):
        _mask = "{mask}"
        _jtr_main_exec = "{jtr.main_exec}"
        _masks_file = f"'{masks_file}'"
        _hashes_file = f"'{hashes_file}'"
        _header_attack = "{header_attack}"
        _attack = "{attack}"

        parallel_job_type = slurm.parallel_job_parser()
        if not  parallel_job_type in ["MPI", "OMP"]:
            raise InvalidParallelJob(parallel_job_type)


        if parallel_job_type == "MPI":
            masks_attack = (
                f"""
#!/bin/env python3

from ama.core.plugins.cracker import John
from sbash import Bash

jtr = John()

with open({_masks_file}, 'r') as masks:
    while mask := masks.readline().rstrip():
        all_cracked = John.are_all_hashes_cracked({_hashes_file})
        if not all_cracked:
            attack =  (
                f"srun --mpi={slurm.pmix}"
                f" {_jtr_main_exec} --mask={_mask}"
                f" --format={hash_type} {hashes_file}"
            )

            header_attack = f"[*] Running: {_attack}"
            Bash.exec(f"echo -e '\\n\\n\\n{_header_attack}'")
            Bash.exec(attack)
                """
            )

        elif parallel_job_type == "OMP":
                        masks_attack = (
                f"""
#!/bin/env python3

from ama.core.plugins.cracker import John
from sbash import Bash

jtr = John()

with open({_masks_file}, 'r') as masks:
    while mask := masks.readline().rstrip():
        all_cracked = John.are_all_hashes_cracked({_hashes_file})
        if not all_cracked:
            attack =  (
                f"srun {_jtr_main_exec} --mask={_mask}"
                f" --format={hash_type} {hashes_file}"
            )

            header_attack = f"[*] Running: {_attack}"
            Bash.exec(f"echo -e '\\n\\n\\n{_header_attack}'")
            Bash.exec(attack)
                """
            )

        with open(masks_attack_script, 'w') as attack:
            attack.write(masks_attack)

        print_successful(f"Masks attack script generated: {masks_attack_script}")

    # debugged - date: Mar 1 2021
    def single_attack(self, *,
                      hash_type: str, hashes_file: str,
                      slurm):
        """
        Single attack using john submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Jonh's hash type
        hashes_file (str): Hashes file to attack
        slurm (Slurm): Instance of Slurm class
        """
        #import pdb; pdb.set_trace()

        if self.enable:
            try:
                permission = [os.R_OK]
                Path.access(permission, hashes_file)
                John.check_hash_type(hash_type)

                #cmd2.Cmd.poutput(f"Attacking {hashType} hashes in {hashesFile} using single attack.")
                print_status(f"Attacking {hash_type} hashes in {hashes_file} using single attack.")
                if slurm and slurm.partition:
                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["MPI", "OMP"]:
                        raise InvalidParallelJob(parallel_job_type)

                    if parallel_job_type == "MPI":
                        parallel_work = [
                            (
                                f"srun --mpi={slurm.pmix}"
                                f" {self.main_exec} --single"
                                f" --format={hash_type} {hashes_file}"
                            )
                        ]

                    elif parallel_job_type == "OMP":
                        parallel_work = [
                            (
                                f"{self.main_exec}"
                                f" --single"
                                f" --format={hash_type}"
                                f" {hashes_file}"
                            )
                        ]

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    single_attack =  (
                        f"{self.main_exec}"
                        f" --single"
                        f" --format={hash_type}"
                        f" {hashes_file}"
                    )
                    Bash.exec(single_attack)

            except Exception as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)
        else:
            #cmd2.Cmd.pwarning("Cracker {self.mainName} is disable")
            print_failure("Cracker {self.main_name} is disable")


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
