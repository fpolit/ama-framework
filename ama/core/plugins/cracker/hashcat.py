#!/usr/bin/env python3
#
# Hashcat class
#
# Jan 9 2021
# Implementation of Hashcat class (using core module of pyhashcat python package)
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from itertools import combinations
import time
import os
import re
from tabulate import tabulate
from sbash import Bash
from typing import List
from fineprint.status import (
    print_status,
    print_failure,
    print_successful
)
from fineprint.color import ColorStr


from ama.core.slurm import Slurm
from .hash_cracker import HashCracker
from .crackedHash import CrackedHash
from ama.data.hashes import hcHashes
from ama.core.files import Path
from .mask import Mask
#from ama.core.cmdsets.db import Connection

class Hashcat(HashCracker):
    """
    Hashcat password cracker
    This class implement the diverse attack of hashcat and its benchmark
    Suported Attacks: wordlist, incremental, masks, combination, hybrid
    """

    HASHES = hcHashes
    MAINNAME = "hashcat"

    def __init__(self, *, hc_exec:Path=None, potfile:Path = None):
        super().__init__(name=['hashcat', 'hc'], version="v6.1.1", main_exec=hc_exec)
        self.potfile = potfile if potfile else os.path.join(Path.home(), ".hashcat/hashcat.potfile")

    def search_hash(self, pattern, *, sensitive=False):
        """
        Search valid hashcat's hashes types given a pattern
        """

        if sensitive:
            hash_pattern = re.compile(rf"[\W|\w|\.]*{pattern}[\W|\w|\.]*")
        else:
            hash_pattern = re.compile(rf"[\W|\w|\.]*{pattern}[\W|\w|\.]*", re.IGNORECASE)

        posible_hashes = []
        for hash_id, hash_type in self.HASHES.items():
            hash_name, description = hash_type.values()
            if hash_pattern.fullmatch(hash_name):
                posible_hashes.append((hash_id, hash_name, description))

        print(tabulate(posible_hashes, headers=["#", "Name", "Description"]))


    def hash_status(self, query_hash: str):
        """
        Check the status of query hash in hashcat potfile

        Return:
        """
        pattern = re.compile(rf"({query_hash}):(\W*|\w*|.*)", re.DOTALL)

        return self.pattern_in_potfile(pattern, self.potfile)



    # debugged (local attack)  - date Jun 13 2021
    def benchmark(self, slurm, local:bool = False):
        """
        Hashcat benchmark
        """
        #import pdb; pdb.set_trace()
        try:
            if not self.enable:
                raise Exception(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")

            if (not local) and slurm and slurm.partition:
                parallel_job_type = slurm.parallel_job_parser()
                if not  parallel_job_type in ["GPU"]:
                    raise InvalidParallelJob(parallel_job_type)

                #core, extra = slurm.parameters()

                attack_cmd = f"srun {self.main_exec} -b"

                header_attack = f"echo -e '\\n\\n[*] Running: {attack_cmd}'"

                parallel_work = [(header_attack, attack_cmd)]
                batch_script_name = slurm.gen_batch_script(parallel_work)

                Bash.exec(f"sbatch {batch_script_name}")

            else:
                attack_cmd = f"{self.main_exec} -b"
                print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                Bash.exec(attack_cmd)

        except Exception as error:
            print_failure(error)


    # debugged (local attack)  - date Jun 13 2021
    def wordlist_attack(self, *,
                        hash_types:List[int] , hashes_file:str, wordlists:List[str], rules_file:str=None,
                        sleep:int = 1, slurm: Slurm, local:bool = False,
                        db_status:bool = False, workspace:str = None, db_credential_file: Path = None):

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
                Path.access(permission, hashes_file, *wordlists)

                self.check_hash_type(hash_types)

                print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file with {ColorStr(wordlists).StyleBRIGHT} wordlists")

                hash_types_names = [Hashcat.HASHES[hash_type]['Name'] for hash_type in hash_types
                                    if hash_type in Hashcat.HASHES]
                print_status(f"Possible hashes identities: {ColorStr(hash_types_names).StyleBRIGHT}")

                #import pdb; pdb.set_trace()
                if (not local) and slurm:

                    enviroment = (
                        f"{self.MAINNAME.upper()}={self.main_exec}",
                    )

                    if slurm.config:
                        slurm.check_partition()

                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in [Slurm.GPU]:
                        raise InvalidParallelJob(parallel_job_type)

                    parallel_work = []
                    for hash_type in hash_types:
                        for wordlist in wordlists:
                            attack_cmd = (
                                f"srun {self.main_exec}"
                                f" -a {attack_mode}"
                                f" -m {hash_type}"
                                f" {hashes_file} {wordlists}"
                            )

                            if rules_file:
                                Path.access(permission, rules_file)
                                attack_cmd += f" -r {rules_file}"

                            header_attack = f"echo -e '\\n\\n[*] Running: {attack_cmd}'"

                            if db_status and workspace and db_credential_file:
                                insert_cracked_hashes = (
                                    f"amadb -c {db_credential_file} -w {workspace}"
                                    f" --cracker {Hashcat.MAINNAME} -j {hashes_file}"
                                )

                                parallel_work.append((header_attack, attack_cmd, insert_cracked_hashes))
                            else:
                                parallel_work.append((header_attack, attack_cmd))

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    #import pdb; pdb.set_trace()
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    #import pdb; pdb.set_trace()
                    for hid in hash_types:
                        for wl in wordlists:
                            all_cracked = self.are_all_cracked(hashes_file)
                            if  not all_cracked: # some hash isn't cracked yet
                                attack_cmd = (
                                    f"{self.main_exec}"
                                    f" -a {attack_mode}"
                                    f" -m {hid}"
                                )

                                if rules_file:
                                    Path.access(permission, rules_file)
                                    attack_cmd += f" -r {rules_file}"

                                attack_cmd += f" {hashes_file} {wl}"

                                print("\n")
                                print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                                Bash.exec(attack_cmd)

                                if sleep > 0:
                                    time.sleep(sleep)

                            else:
                                print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                                break
                        if all_cracked:
                            break

                    #import pdb; pdb.set_trace()
                    # if db_status and workspace and db_credential_file:
                    #     Hashcat.insert_hashes_to_db(hashes_file, workspace, db_credential_file)

            except Exception as error:
                print_failure(error)

        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    # debugged (local attack)  - date Jun 13 2021
    def combination_attack(self, *,
                           hash_types: List[str] , hashes_file:str , wordlists: List[str],
                           sleep:int = 1, slurm: Slurm, local:bool = False,
                           db_status:bool = False, workspace:str = None, db_credential_file: Path = None):

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
            try:
                attack_mode = 1

                permission = [os.R_OK]
                Path.access(permission, hashes_file, *wordlists)
                Hashcat.check_hash_type(hash_types)

                print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file with {ColorStr(wordlists).StyleBRIGHT} wordlists (Combined 2 in 2)")
                combined_wls = list(combinations(wordlists, 2))
                for k, combination in enumerate(combined_wls):
                    print_status(f"Combination {k+1}: {combination}")

                hash_types_names = [Hashcat.HASHES[hash_type]['Name'] for hash_type in hash_types]
                print_status(f"Possible hashes identities: {ColorStr(hash_types_names).StyleBRIGHT}")

                time.sleep(1)

                if (not local) and slurm and slurm.partition:

                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["GPU"]:
                        raise InvalidParallelJob(parallel_job_type)

                    parallel_work = []
                    for hash_type in hash_types:
                        attack_cmd = (
                            f"srun {self.main_exec}"
                            f" -a {attack_mode}"
                            f" -m {hash_type}"
                            f" {hashes_file} {wordlists[0]} {wordlists[1]}"
                        )

                        header_attack = f"echo -e '\\n\\n[*] Running: {attack_cmd}'"

                        if db_status and workspace and db_credential_file:
                            insert_cracked_hashes = (
                                f"amadb -c {db_credential_file} -w {workspace}"
                                f" --cracker {Hashcat.MAINNAME} -j {hashes_file}"
                            )

                            parallel_work.append((header_attack, attack_cmd, insert_cracked_hashes))
                        else:
                            parallel_work.append((header_attack, attack_cmd))

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    #import pdb; pdb.set_trace()
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    #import pdb; pdb.set_trace()
                    for hid in hash_types:
                        for wl1, wl2 in combined_wls:
                            all_cracked = Hashcat.are_all_hashes_cracked(hashes_file)
                            if  not all_cracked: # some hash isn't cracked yet
                                attack_cmd = (
                                    f"{self.main_exec}"
                                    f" -a {attack_mode}"
                                    f" -m {hid}"
                                    f" {hashes_file} {wl1} {wl2}"
                                )

                                print("\n")
                                print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                                Bash.exec(attack_cmd)

                                if sleep > 0:
                                    time.sleep(sleep)

                            else:
                                print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                                break
                        if all_cracked:
                            break

                    #import pdb; pdb.set_trace()
                    if db_status and workspace and db_credential_file:
                        Hashcat.insert_hashes_to_db(hashes_file, workspace, db_credential_file)

            except Exception as error:
                print_failure(error)

        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    # DEBUGGED - date Jun 5 2021
    def brute_force_attack(self, *,
                           hash_types:List[str] , hashes_file:str , mask:str,
                           sleep:int = 1, slurm: Slurm, local:bool = False,
                           db_status:bool = False, workspace:str = None, db_credential_file: Path = None):

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
            try:
                attack_mode = 3
                permission = [os.R_OK]
                Mask.is_valid_mask(mask)
                Path.access(permission, hashes_file)
                Hashcat.check_hash_type(hash_types)

                print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file with {ColorStr(mask).StyleBRIGHT} mask")

                hash_types_names = [Hashcat.HASHES[hash_type]['Name'] for hash_type in hash_types]
                print_status(f"Possible hashes identities: {ColorStr(hash_types_names).StyleBRIGHT}")


                if (not local) and slurm and slurm.partition:

                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["GPU"]:
                        raise InvalidParallelJob(parallel_job_type)

                    parallel_work = []
                    for hash_type in hash_types:
                        attack_cmd = (
                            f"srun {self.main_exec}"
                            f" -a {attack_mode}"
                            f" -m {hash_type}"
                            f" {hashes_file} {mask}"
                        )

                        header_attack = f"echo -e '\\n\\n[*] Running: {attack_cmd}'"

                        if db_status and workspace and db_credential_file:
                            insert_cracked_hashes = (
                                f"amadb -c {db_credential_file} -w {workspace}"
                                f" --cracker {Hashcat.MAINNAME} -j {hashes_file}"
                            )

                            parallel_work.append((header_attack, attack_cmd, insert_cracked_hashes))
                        else:
                            parallel_work.append((header_attack, attack_cmd))

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    #import pdb;pdb.set_trace()
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    #import pdb;pdb.set_trace()
                    for hash_type in hash_types:
                        are_all_hashes_cracked = Hashcat.are_all_hashes_cracked(hashes_file)
                        if  not are_all_hashes_cracked: # some hash isn't cracked yet
                            attack_cmd = (
                                f"{self.main_exec}"
                                f" -a {attack_mode}"
                                f" -m {hash_type}"
                                f" {hashes_file} {mask}"
                            )

                            print()
                            print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                            Bash.exec(attack_cmd)
                            if sleep > 0:
                                print_status(f"{ColorStr('Sleeping ...').StyleBRIGHT}")
                                time.sleep(sleep)

                        else:
                            print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                            break

                    #import pdb;pdb.set_trace()
                    if db_status and workspace and db_credential_file:
                        Hashcat.insert_hashes_to_db(hashes_file, workspace, db_credential_file)

            except Exception as error:
                print_failure(error)

        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    # debugged  - date Jun 13 2021
    def incremental_attack(self, *,
                           hash_types:List[int], hashes_file:str,
                           charset:str = '?a', min_length:int = 0, max_length:int = 0,
                           masks_file:str = "inc.masks", sleep:int = 1,
                           slurm: Slurm, local:bool = False,
                           db_status:bool = False, workspace:str = None, db_credential_file: Path = None):
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

        #import pdb; pdb.set_trace()
        print_status(f"Generating incremental masks file: {ColorStr(masks_file).StyleBRIGHT}")
        masks = None
        if Mask.is_valid_charset(charset):
            masks = [charset*length for length in range(min_length, max_length+1)]
        else:
            masks = ['?a'*length for length in range(min_length, max_length+1)]

        with open(masks_file, 'w') as incremental_masks:
            for mask in masks:
                incremental_masks.write(f"{mask}\n")

        print_successful(f"Incremental masks file {ColorStr(masks_file).StyleBRIGHT} has been generated")

        self.masks_attack(hash_types=hash_types,
                          hashes_file=hashes_file,
                          masks_file= masks_file,
                          sleep = sleep,
                          slurm=slurm,
                          local = local,
                          db_status = db_status,
                          workspace = workspace,
                          db_credential_file = db_credential_file)

    # debugged (local attack) - date Jun 13 2021
    def masks_attack(self,*,
                     hash_types:List[int], hashes_file:str, masks_file:str,
                     sleep:int = 1, slurm: Slurm, local:bool = False,
                     db_status:bool = False, workspace:str = None, db_credential_file: Path = None):

        """
        Masks attack using hashcat submitting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Jonh's hash type
        hashes_file (str): Hash file to attack
        masks_file (str): Masks file to attack
        slurm (Slurm): Instance of Slurm class
        """

        #import pdb; pdb.set_trace()

        if self.enable:
            try:
                attack_mode = 3
                permission = [os.R_OK]
                Path.access(permission, hashes_file, masks_file)
                Hashcat.check_hash_type(hash_types)

                print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file with {ColorStr(masks_file).StyleBRIGHT} masks file.")
                hash_types_names = [Hashcat.HASHES[hash_type]['Name'] for hash_type in hash_types]
                print_status(f"Possible hashes identities: {ColorStr(hash_types_names).StyleBRIGHT}")

                if (not local) and slurm and slurm.partition:
                    pass
                    # Hashcat.gen_masks_attack(hash_types = hash_types,
                    #                          hashes_file = hashes_file,
                    #                          masks_file = masks_file,
                    #                          masks_attack_script = masks_attack_script,
                    #                          slurm = slurm,
                    #                          db_status = db_status,
                    #                          workspace = workspace,
                    #                          db_credential_file = db_credential_file)

                    # parallel_work = [(f"python3 {masks_attack_script}",)]
                    # slurm_script_name = slurm.gen_batch_script(parallel_work)
                    # #import pdb; pdb.set_trace()
                    # Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    #import pdb; pdb.set_trace()
                    for hash_type in hash_types:
                        with open(masks_file, 'r') as masks:
                            while mask := masks.readline().rstrip():
                                if not Mask.is_mask(mask):
                                    print_failure("Invalid mask: {mask}")
                                    continue

                                all_cracked = Hashcat.are_all_hashes_cracked(hashes_file)
                                if not all_cracked:
                                    attack_cmd =  (
                                        f"{self.main_exec}"
                                        f" -a {attack_mode}"
                                        f" -m {hash_type}"
                                        f" {hashes_file} {mask}"
                                    )

                                    print("\n")
                                    print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                                    Bash.exec(attack_cmd)

                                    if sleep > 0:
                                        time.sleep(sleep)

                                else:
                                    print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                                    break #all hashes were cracked so stop attack

                        if all_cracked:
                            break

                    #import pdb; pdb.set_trace()
                    if db_status and workspace and db_credential_file:
                        Hashcat.insert_hashes_to_db(hashes_file, workspace, db_credential_file)

            except Exception as error:
                print_failure(error)

        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")

    #debugged - date Jun 5 2021
    def hybrid_attack(self, *,
                      hash_types: List[str] , hashes_file:str , inverse:bool = False,
                      wordlists: List[str], masks: List[str] = None, masks_file:Path = None,
                      sleep:int = 1, slurm: Slurm, local:bool = False,
                      db_status:bool = False, workspace:str = None, db_credential_file: Path = None):

        """
        hybrid attack using hashcat submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Hashcat's hash type
        hashes_file (str): Hash file to attack
        inverse (bool): If inverse is false the attack combine WORDLISTS + MASKS, otherwise it combine MASKS + WORDLISTS
        wordlists (List[str]): wordlists to attack
        masks (List[str]): masks to attack
        masks_file (str): masks file to attack
        slurm (Slurm): Instance of Slurm class
        """

        #import pdb; pdb.set_trace()
        if self.enable:
            try:
                if not inverse:
                    attack_mode = 6
                else:
                    attack_mode = 7

                permission = [os.R_OK]
                Path.access(permission, hashes_file, *wordlists)
                Hashcat.check_hash_type(hash_types)

                if masks and masks_file:
                    raise Exception("Only supplied masks or a masks file")

                elif masks:
                    valid_masks = []
                    for mask in masks:
                        if Mask.is_mask(mask):
                            valid_masks.append(mask)

                    if not valid_masks:
                        raise Exception("No valid masks supplied")
                    masks = valid_masks

                else: # masks_file supplied
                    Path.access(permission, masks_file)
                    masks = []
                    with open(masks_file, 'r') as _masks_file:
                        while mask := _masks_file.readline().rstrip():
                            if Mask.is_mask(mask):
                                masks.append(mask)

                if not inverse:
                    print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file in hibrid mode {ColorStr('WORDLISTS + MASKS').StyleBRIGHT} ")
                else:
                    print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file in hibrid mode {ColorStr('MASKS + WORDLISTS').StyleBRIGHT}")

                print_status(f"Wordlists: {ColorStr(wordlists).StyleBRIGHT}")
                if masks_file is None:
                    print_status(f"Masks: {ColorStr(masks).StyleBRIGHT}")
                else:
                    print_status(f"Masks file: {ColorStr(masks_file).StyleBRIGHT}")


                wls_masks = []
                counter = 1
                for wl in wordlists:
                    for mask in masks:
                        combination = (wl, mask)
                        if inverse:
                            print_status(f"Combination {counter}: {combination[::-1]}")
                        else:
                            print_status(f"Combination {counter}: {combination}")
                        wls_masks.append(combination)


                hash_types_names = [Hashcat.HASHES[hash_type]['Name'] for hash_type in hash_types]
                print_status(f"Possible hashes identities: {ColorStr(hash_types_names).StyleBRIGHT}")

                #import pdb; pdb.set_trace()
                if (not local) and slurm and slurm.partition:

                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["GPU"]:
                        raise InvalidParallelJob(parallel_job_type)

                    parallel_work = []
                    for hash_type in hash_types:
                        for wordlist in wordlists:
                            for mask in masks:
                                if not inverse:
                                    attack_cmd = (
                                        f"{self.main_exec}"
                                        f" -a {attack_mode}"
                                        f" -m {hash_type}"
                                        f" {hashes_file} {wordlist} {mask}"
                                    )
                                else:
                                    attack_cmd = (
                                        f"{self.main_exec}"
                                        f" -a {attack_mode}"
                                        f" -m {hash_type}"
                                        f" {hashes_file} {mask} {wordlist}"
                                    )

                                header_attack = f"echo -e '\\n\\n[*] Running: {attack_cmd}'"

                                if db_status and workspace and db_credential_file:
                                    insert_cracked_hashes = (
                                        f"amadb -c {db_credential_file} -w {workspace}"
                                        f" --cracker {Hashcat.MAINNAME} -j {hashes_file}"
                                    )

                                    parallel_work.append((header_attack, attack_cmd, insert_cracked_hashes))
                                else:
                                    parallel_work.append((header_attack, attack_cmd))

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    #import pdb; pdb.set_trace()
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    #import pdb; pdb.set_trace()
                    all_cracked = False

                    for hid in hash_types:
                        for wl, mask in wls_masks:
                            all_cracked = Hashcat.are_all_hashes_cracked(hashes_file)
                            if  not all_cracked: # some hash isn't cracked yet
                                if not inverse:
                                    attack_cmd = (
                                        f"{self.main_exec}"
                                        f" -a {attack_mode}"
                                        f" -m {hid}"
                                        f" {hashes_file} {wl} {mask}"
                                    )
                                else:
                                    attack_cmd = (
                                        f"{self.main_exec}"
                                        f" -a {attack_mode}"
                                        f" -m {hid}"
                                        f" {hashes_file} {mask} {wl}"
                                    )

                                print("\n")
                                print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                                Bash.exec(attack_cmd)

                                if sleep > 0:
                                    time.sleep(sleep)

                            else:
                                print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                                break
                        if all_cracked:
                            break

                    #import pdb; pdb.set_trace()
                    if db_status and workspace and db_credential_file:
                        Hashcat.insert_hashes_to_db(hashes_file, workspace, db_credential_file)

            except Exception as error:
                print_failure(error)

        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")
