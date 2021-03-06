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

from typing import List

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
from ama.data.hashes import hcHashes

# core.file imports
from ...files import Path

# cracker exceptions imports
from .crackerException import (
    InvalidParallelJob,
    InvalidHashType,
    InvalidWordlistsNumber
)

# mask imports
from .mask import Mask


class Hashcat(PasswordCracker):
    """
    Hashcat password cracker
    This class implement the diverse attack of hashcat and its benchmark
    Suported Attacks: wordlist, incremental, masks, combination, hybrid
    """

    HASHES = hcHashes
    MAINNAME = "hashcat"

    def __init__(self):
        super().__init__(name=['hashcat', 'hc'], version="v6.1.1")


    @staticmethod
    def check_hash_type(hash_type):
        """
        Check if hash_type is a valid hash type

        Args:
            hash_type (str): hash type

        Raises:
            InvalidHashType: Error if the hasType is an unsopported hash type of a cracker
        """

        if not (hash_type in Hashcat.HASHES):
            raise InvalidHashType(Hashcat, hash_type)


    @staticmethod
    def search_hash(pattern, *, sensitive=False):
        """
        Search valid hashcat's hashes types given a pattern
        """

        if sensitive:
            hash_pattern = re.compile(rf"[\W|\w|\.]*{pattern}[\W|\w|\.]*")
        else:
            hash_pattern = re.compile(rf"[\W|\w|\.]*{pattern}[\W|\w|\.]*", re.IGNORECASE)

        posible_hashes = []
        for hash_id, hash_type in Hashcat.HASHES.items():
            hash_name, description = hash_type.values()
            if hash_pattern.fullmatch(hash_name):
                posible_hashes.append((hash_id, hash_name, description))

        print(tabulate(posible_hashes, headers=["#", "Name", "Description"]))


    @staticmethod
    def hash_status(query_hash: str, potfile:str = None):
        """
        Check the status (broken by Hashcat or not) of query hash

        Return:
        if query_hash is in potfile then [HASHTYPE, HASH, PASSWORD] list is returned
        otherwise None is returned
        """
        #import pdb;pdb.set_trace()

        if potfile is None:
            HOME = os.path.expanduser("~")
            potfile = os.path.join(HOME, ".hashcat/hashcat.potfile")

        try:
            permission = [os.R_OK]
            Path.access(permission, potfile)

            cracked_pattern = re.compile(rf"({query_hash}):(\W*|\w*|.*)", re.DOTALL)

            with open(potfile, 'r') as hashcat_potfile:
                while   cracked_hash := hashcat_potfile.readline().rstrip():
                    if cracked_hashpot := cracked_pattern.fullmatch(cracked_hash):
                        hashpot = cracked_hashpot.groups()
                        return CrackedHash(cracked_hash = hashpot[0],
                                           password = hashpot[1],
                                           cracker = Hashcat)

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
                if Hashcat.hash_status(query_hash, potfile) is None: # query_hash isn't cracked yet
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
            potfile = os.path.join(HOME, ".hashcat/hashcat.potfile")

        try:
            permission = [os.R_OK]
            Path.access(permission, potfile, query_hashes_file)


            with open(query_hashes_file, 'r') as hashes_file:
                while query_hash := hashes_file.readline().rsplit():
                    query_hash = query_hash[0]
                    if cracker_hash := Hashcat.hash_status(query_hash):
                        hashes_status['cracked'].append(cracker_hash.getAttributes())
                    else: #crackedHash is uncracked
                        hashes_status['uncracked'].append([query_hash])

            return hashes_status

        except Exception as error:
            #cmd2.Cmd.pexcept(error, "ERROR")
            print_failure(error)

    def benchmark(self, slurm=None):
        """
        Hashcat benchmark
        """
        #import pdb; pdb.set_trace()
        if self.enable:
            if slurm and slurm.partition:
                parallel_job_type = slurm.parallel_job_parser()
                if not  parallel_job_type in ["GPU"]:
                    raise InvalidParallelJob(parallel_job_type)

                #core, extra = slurm.parameters()
                parallel_work = [
                        (
                            f"srun {self.main_exec} -b"
                        )
                    ]

                batch_script_name = slurm.gen_batch_script(parallel_work)

                Bash.exec(f"sbatch {batch_script_name}")

            else:
                hashcat_benchmark = f"{self.main_exec} -b"
                Bash.exec(hashcat_benchmark)
        else:
            #cmd2.Cmd.pwarning(f"Cracker {self.mainName} is disable")
            print_failure(f"Cracker {self.main_name} is disable")



    def wordlist_attack(self, *,
                        hash_type:int , hashes_file:str, wordlist:str,
                        slurm):

        """
        Wordlist attack using hashcat submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Hashcat's hash type
        hashes_file (str): Hash file to attack
        wordlist (str): wordlist to attack
        slurm (Slurm): Instance of Slurm class
        """
        #import pdb; pdb.set_trace()
        if self.enable:
            attack_mode = 0
            try:
                permission = [os.R_OK]
                Path.access(permission, hashes_file, wordlist)
                Hashcat.check_hash_type(hash_type)

                #cmd2.Cmd.poutput(f"Attacking {hash_type} hashes in {hashesfile} file with {wordlist} wordlist.")
                print_status(f"Attacking {hash_type} hashes in {hashes_file} file with {wordlist} wordlist")
                if slurm and slurm.partition:
                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["GPU"]:
                        raise InvalidParallelJob(parallel_job_type)

                    parallel_work = [
                            (
                                f"srun {self.main_exec} -a {attack_mode} -m {hash_type}"
                                f" {hashes_file} {wordlist}"
                            )
                        ]

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    wordlist_attack = (
                        f"srun {self.main_exec} -a {attack_mode} -m {hash_type}"
                        f" {hashes_file} {wordlist}"
                    )

                    Bash.exec(wordlist_attack)

            except Exception as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

        else:
            #cmd2.Cmd.pwarning("Cracker {self.main_name} is disable")
            print_failure("Cracker {self.main_name} is disable")


    def combination_attack(self, *,
                           hash_type:str , hashes_file:str , wordlists: List[str],
                           slurm):

        """
        Combination attack using hashcat submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Hashcat's hash type
        hashes_file (str): Hash file to attack
        wordlists (List[str]): wordlists to attack
        slurm (Slurm): Instance of Slurm class
        """

        #import pdb; pdb.set_trace()
        if self.enable:
            attack_mode = 1
            try:
                if not len(wordlists) == 2:
                    raise InvalidWordlistsNumber(wordlists)

                permission = [os.R_OK]
                Path.access(permission, hashes_file, *wordlists)
                Hashcat.check_hash_type(hash_type)

                #cmd2.Cmd.poutput(f"Attacking {hash_type} hashes in {hashesfile} file with {wordlist} wordlist.")
                print_status(f"Attacking {hash_type} hashes in {hashes_file} file with {wordlist} wordlist")
                if slurm and slurm.partition:
                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["GPU"]:
                        raise InvalidParallelJob(parallel_job_type)

                    parallel_work = [
                            (
                                f"srun {self.main_exec} -a {attack_mode} -m {hash_type}"
                                f" {hashes_file} {wordlists[0]} {wordlists[1]}"
                            )
                        ]

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    combination_attack = (
                        f"srun {self.main_exec} -a {attack_mode} -m {hash_type}"
                        f" {hashes_file} {wordlists[0]} {wordlists[1]}"
                    )

                    Bash.exec(combination_attack)

            except Exception as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

        else:
            #cmd2.Cmd.pwarning("Cracker {self.main_name} is disable")
            print_failure("Cracker {self.main_name} is disable")

    def brute_force_attack(self, *,
                           hash_type:str , hashes_file:str , mask:str,
                           slurm):

        """
        Brute force attack using hashcat submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Hashcat's hash type
        hashes_file (str): Hash file to attack
        mask (str): mask to attack
        slurm (Slurm): Instance of Slurm class
        """

        #import pdb; pdb.set_trace()
        if self.enable:
            attack_mode = 3
            try:

                permission = [os.R_OK]
                Mask.is_valid_mask(mask)
                Path.access(permission, hashes_file, *wordlists)
                Hashcat.check_hash_type(hash_type)

                #cmd2.Cmd.poutput(f"Attacking {hash_type} hashes in {hashesfile} file with {wordlist} wordlist.")
                print_status(f"Attacking {hash_type} hashes in {hashes_file} file with {wordlist} wordlist")
                if slurm and slurm.partition:
                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["GPU"]:
                        raise InvalidParallelJob(parallel_job_type)

                    parallel_work = [
                            (
                                f"srun {self.main_exec} -a {attack_mode} -m {hash_type}"
                                f" {hashes_file} {mask}"
                            )
                        ]

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    brute_force_attack = (
                        f"srun {self.main_exec} -a {attack_mode} -m {hash_type}"
                        f" {hashes_file} {mask}"
                    )

                    Bash.exec(brute_force_attack)

            except Exception as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

        else:
            #cmd2.Cmd.pwarning("Cracker {self.main_name} is disable")
            print_failure("Cracker {self.main_name} is disable")


    def incremental_attack(self, *,
                           hash_type:int, hashes_file:str, incremental_attack_script:str,
                           min_length:int = 0, max_length:int = 0, masks_file:str = "incremental_masks.txt",
                           slurm):
        """
        Incremental attack using hashcat submitting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Jonh's hash type
        hashes_file (str): Hash file to attack
        min_length (int):  minimum length of mask ('?a'*min_length)
        max_length (int):  maximum length of mask ('?a'*max_length)
        masks_file (str):  file name to save masks used by incremental attack (default: incremental_masks.txt)
        slurm (Slurm): Instance of Slurm class
        """

        masks = ['?a'*length for length in range(min_length, max_length+1)]
        with open(masks_file, 'w') as incremental_masks:
            for mask in masks:
                incremental_masks.write(f"{mask}\n")

        self.mask_attack(hash_type=hash_type,
                         hashes_file=hashes_file,
                         masks_file= masks_file,
                         masks_attack_script=incremental_attack_script,
                         slurm=slurm)

    def masks_attack(self,*,
                     hash_type:int, hashes_file:str, masks_file:str,
                     masks_attack_script: str, slurm):

        """
        Masks attack using hashcat submitting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Jonh's hash type
        hashes_file (str): Hash file to attack
        masks_file (str): Masks file to attack
        slurm (Slurm): Instance of Slurm class
        """

        if self.enable:
            attackMode = 3
            try:
                permission = [os.R_OK]
                Path.access(permission, hashes_file, masks_file)
                Hashcat.check_hash_type(hash_type)

                print_status(f"Attacking {hash_type} hashes in {hashes_file} file with {masks_file} masks file.")
                if slurm and slurm.partition:
                    Hashcat.gen_masks_attack(hash_type = hash_type,
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
                            all_cracked = Hashcat.are_all_hashes_cracked(hashes_file)
                            if not all_cracked:
                                mask_attack =  (
                                    f"{self.main_exec} -a {attack_mode}"
                                    f" -m {hash_type} {hashes_file} {mask}"
                                )
                                print()
                                print_status(f"Running: {mask_attack}")
                                Bash.exec(mask_attack)
                            else:
                                break #hashes were cracked so stop attack

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
        _hc_main_exec = "{hc.main_exec}"
        _masks_file = f"'{masks_file}'"
        _hashes_file = f"'{hashes_file}'"
        _header_attack = "{header_attack}"
        _attack = "{attack}"

        parallel_job_type = slurm.parallel_job_parser()
        if not  parallel_job_type in ["GPU"]:
            raise InvalidParallelJob(parallel_job_type)


        masks_attack = (
                f"""
#!/bin/env python3

from ama.core.cracker import Hashcat
from sbash import Bash


hc = Hashcat()

with open({_masksFile}, 'r') as masks:
    while mask := masks.readline().rstrip():
        all_cracked = Hashcat.are_all_hashes_cracked({_hashes_file})
        if not all_cracked:
            attack =  (
                f"srun {_hc_main_exec} -a 3"
                f" -m {hash_type} {hashes_file} {_mask}"
            )

            header_attack = f"[*] Running: {_attack}"
            Bash.exec(f"echo -e '\\n{_header_attack}'")
            Bash.exec(attack)
                """
            )

        with open(masks_attack_script, 'w') as attack:
            attack.write(masks_attack)

        print_successful(f"Masks attack script generated: {masks_attack_script}")


    # @staticmethod
    # def hybridWMF(*, attackMode=6, hashType, hashFile, wordlist, maskFile, hpc=None):
    #     Hashcat.checkAttackArgs(_hashType = hashType,
    #                             _hashFile = hashFile,
    #                             _wordlist = wordlist,
    #                             _maskFile = maskFile)
    #     hc = Hashcat()
    #     print_status(f"Attacking {hashFile} with {wordlist} wordlist and {maskFile} mask file in hybrid WMF attack mode.")
    #     if hpc:
    #         # develop me please
    #         pass
    #     else:
    #         with open(maskFile, 'r') as masks:
    #             while mask := masks.readline().rstrip():
    #                 if not PasswordCracker.statusHashFile(hashFilePath):
    #                     hybridWMFAttack =   f"{hc.mainexec} -a {attackMode} -m {hashType} {wordlist} {mask}"
    #                     print_status(f"Running: {hybridWMFAttack}")
    #                     Bash.exec(maskAttack)



    # @staticmethod
    # def hybridMFW(*, attackMode=7, hashType, hashFile, wordlist, maskFile, hpc=None):
    #     Hashcat.checkAttackArgs(_hashType = hashType,
    #                             _hashFile = hashFile,
    #                             _wordlist = wordlist,
    #                             _maskFile = maskFile)
    #     hc = Hashcat()
    #     print_status(f"Attacking {hashFile} with {maskFile} mask file and {wordlist} wordlist in hybrid MFW attack mode.")
    #     if hpc:
    #         # develop me please
    #         pass
    #     else:
    #         with open(maskFile, 'r') as masks:
    #             while mask := masks.readline().rstrip():
    #                 if not PasswordCracker.statusHashFile(hashFilePath):
    #                     hybridMFWAttack =   f"{hc.mainexec} -a {attackMode} -m {hashType} {mask} {wordlist}"
    #                     print_status(f"Running: {hybridMFWAttack}")
    #                     Bash.exec(maskAttack)
