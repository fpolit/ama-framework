#!/usr/bin/env python3
#
# Hashcat class
# Jan 9 2021 - Implementation of Hashcat class
#                (using core module of pyhashcat python package)
#
# Maintainer: glozanoa <glozanoa@uni.pe>


import time
import os
import re
from tabulate import tabulate
from sbash import Bash
#import psycopg2
from typing import List
from fineprint.status import (
    print_status,
    print_failure,
    print_successful
)
from fineprint.color import ColorStr


from ama.core.slurm import Slurm
from .cracker import PasswordCracker
from .crackedHash import CrackedHash
from ama.data.hashes import hcHashes
from ama.core.files import Path
from .mask import Mask
#from ama.core.cmdsets.db import Connection
from .crackerException import (
    InvalidParallelJob,
    NoValidHashType,
    InvalidWordlistsNumber
)

class Hashcat(PasswordCracker):
    """
    Hashcat password cracker
    This class implement the diverse attack of hashcat and its benchmark
    Suported Attacks: wordlist, incremental, masks, combination, hybrid
    """

    HASHES = hcHashes
    MAINNAME = "hashcat"

    def __init__(self, hc_exec:Path=None):
        super().__init__(name=['hashcat', 'hc'], version="v6.1.1", main_exec=hc_exec)


    #debugged - date: Apr 3 2021
    @staticmethod
    def check_hash_type(hash_types: List[int]):
        """
        Check if hash_type is a valid hash type

        Args:
            hash_type (str): hash type

        Raises:
            InvalidHashType: Error if the hasType is an unsopported hash type of a cracker
        """
        #import pdb;pdb.set_trace()

        any_valid_hash_type = False
        for htype in hash_types:
            if htype in Hashcat.HASHES:
                any_valid_hash_type = True
                break
            else:
                print_failure(f"Invalid hashcat hash type: {htype}")


        if not any_valid_hash_type:
            raise NoValidHashType(Hashcat, hash_types)

    #debugged - date: Mar 6 2021
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

    # CHECK John.hashes_status
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
            HOME = Path.home()
            potfile = Path.joinpath(HOME, ".hashcat/hashcat.potfile")

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


    # debugged - date Apr 2 2021
    @staticmethod
    def are_all_hashes_cracked(hashes_file: Path, potfile: Path = None):
        """
        Check if all hashes are cracked
        return True if all hashes were cracked otherwise return False
        """
        #import pdb;pdb.set_trace()
        all_cracked = True
        with open(hashes_file, 'r') as hashes:
            while query_hash := hashes.readline().rstrip():
                cracker_hash = Hashcat.hash_status(query_hash)
                if cracker_hash is None: # query_hash isn't cracked yet
                    all_cracked = False
                    break

        return all_cracked


    # CHECK John.hahses_file_status
    @staticmethod
    def hashes_file_status(query_hashes_file:Path, potfile=None):
        """
        Check the status (broken by John or not) of hashes in query_hashes_file
        and return the cracked and uncracked hashes
        """
        #import pdb; pdb.set_trace()
        hashes_status = {'cracked': [], "uncracked": []}

        if potfile is None:
            HOME = Path.home()
            potfile = Path.joinpath(HOME, ".hashcat/hashcat.potfile")

        try:
            permission = [os.R_OK]
            Path.access(permission, potfile, query_hashes_file)


            with open(query_hashes_file, 'r') as hashes_file:
                while query_hash := hashes_file.readline().rstrip():
                    if cracker_hash := Hashcat.hash_status(query_hash):
                        hashes_status['cracked'].append(cracker_hash.get_loot())
                    else: #crackedHash is uncracked
                        hashes_status['uncracked'].append([query_hash])

            return hashes_status

        except Exception as error:
            print_failure(error)


    # debugged - date Apr 3 2021
    @staticmethod
    def insert_hashes_to_db(hashes_file: Path, workspace: str, creds_file: Path):
        pass
        # cur = db_conn = None
        # try:
        #     #import pdb;pdb.set_trace()
        #     hashes_status = Hashcat.hashes_file_status(hashes_file)
        #     cracked_hashes = hashes_status['cracked']

        #     db_credentials = Connection.dbCreds(creds_file)
        #     db_conn = psycopg2.connect(**db_credentials)

        #     cur = db_conn.cursor()
        #     cur.execute(f"SELECT hash from hashes_{workspace}")
        #     cracked_hashes_db = cur.fetchall()
        #     new_cracked_hashes = []  #only non-repeated cracked hashes
        #     for cracked_hash in cracked_hashes: # cracked_hash = (hash, type, cracked, password)
        #         repeated = False
        #         for cracked_hash_db in cracked_hashes_db: # cracked_hash_db = (cracked_hash)
        #             if cracked_hash[0] == cracked_hash_db[0]:
        #                 repeated = True
        #                 break

        #         if not repeated:
        #             new_cracked_hashes.append(cracked_hash)

        #     if new_cracked_hashes:
        #         insert_cracked_hash = (
        #             f"""
        #             INSERT INTO hashes_{workspace} (hash, type, cracker, password)
        #             VALUES (%s, %s, %s, %s)
        #             """
        #         )

        #         cur.executemany(insert_cracked_hash, cracked_hashes)
        #         print_successful(f"Cracked hashes were saved to {ColorStr(workspace).StyleBRIGHT} workspace")

        #     else:
        #         print_status(f"No new cracked hashes to save to {ColorStr(workspace).StyleBRIGHT} workspace")

        #     db_conn.commit()
        #     cur.close()

        # except Exception as error:
        #     print_failure(error)

        # finally:
        #     if cur is not None:
        #         cur.close()

        #     if db_conn is not None:
        #         db_conn.close()

    # modify - date: Apr 1 2021 (debugged - date Apr 2 2021)
    def benchmark(self, slurm, local:bool = False):
        """
        Hashcat benchmark
        """
        #import pdb; pdb.set_trace()
        if self.enable:
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
        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    # modify - date: Apr 1 2021 (debugged - date Apr 3 2021)
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

                Hashcat.check_hash_type(hash_types)

                print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file with {ColorStr(wordlists).StyleBRIGHT} wordlists")

                hash_types_names = [Hashcat.HASHES[hash_type]['Name'] for hash_type in hash_types
                                    if hash_type in Hashcat.HASHES]
                print_status(f"Possible hashes identities: {ColorStr(hash_types_names).StyleBRIGHT}")

                #import pdb; pdb.set_trace()
                if (not local) and slurm and slurm.partition:

                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["GPU"]:
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
                    for hash_type in hash_types:
                        for wordlist in wordlists:
                            are_all_hashes_cracked = Hashcat.are_all_hashes_cracked(hashes_file)
                            if  not are_all_hashes_cracked: # some hash isn't cracked yet
                                attack_cmd = (
                                    f"{self.main_exec}"
                                    f" -a {attack_mode}"
                                    f" -m {hash_type}"
                                    f" {hashes_file} {wordlist}"
                                )

                                if rules_file:
                                    Path.access(permission, rules_file)
                                    attack_cmd += f" -r {rules_file}"

                                print()
                                print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                                Bash.exec(attack_cmd)
                                if sleep > 0:
                                    sleeping_msg = ColorStr(f"Sleeping {sleep} seg ...").StyleBRIGHT
                                    print_status(sleeping_msg)
                                    time.sleep(sleep)

                            else:
                                print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                                break

                    #import pdb; pdb.set_trace()
                    if db_status and workspace and db_credential_file:
                        Hashcat.insert_hashes_to_db(hashes_file, workspace, db_credential_file)

            except Exception as error:
                print_failure(error)

        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    # modify - date: Apr 1 2021 (debugged - date Apr 3 2021)
    # NOTE - date Jun 5 2021:
    # Implement: Accept more than 2 wordlists and permute them 2 by 2 (unique combination of 2)
    #            and perform a combination attack with each combination (of 2 wordlists)
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

                if not len(wordlists) == 2:
                    raise InvalidWordlistsNumber(wordlists)

                permission = [os.R_OK]
                Path.access(permission, hashes_file, *wordlists)
                Hashcat.check_hash_type(hash_types)

                print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file with {ColorStr(wordlists).StyleBRIGHT} wordlists")

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
                    for hash_type in hash_types:
                        are_all_hashes_cracked = Hashcat.are_all_hashes_cracked(hashes_file)
                        if  not are_all_hashes_cracked: # some hash isn't cracked yet
                            attack_cmd = (
                                f"{self.main_exec}"
                                f" -a {attack_mode}"
                                f" -m {hash_type}"
                                f" {hashes_file} {wordlists[0]} {wordlists[1]}"
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

        import pdb; pdb.set_trace()
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


    # modify - date: Apr 1 2021
    def incremental_attack(self, *,
                           hash_types:List[int], hashes_file:str, incremental_attack_script:str,
                           charset:str = '?a', min_length:int = 0, max_length:int = 0,
                           masks_file:str = "incremental_masks.txt", sleep:int = 1,
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
                          masks_attack_script=incremental_attack_script,
                          slurm=slurm,
                          sleep = sleep,
                          local = local,
                          db_status = db_status,
                          workspace = workspace,
                          db_credential_file = db_credential_file)

    # modify - date: Apr 1 2021 (debugged - date Apr 3 2021)
    def masks_attack(self,*,
                     hash_types:List[int], hashes_file:str, masks_file:str,
                     masks_attack_script: str,
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
                    Hashcat.gen_masks_attack(hash_types = hash_types,
                                             hashes_file = hashes_file,
                                             masks_file = masks_file,
                                             masks_attack_script = masks_attack_script,
                                             slurm = slurm,
                                             db_status = db_status,
                                             workspace = workspace,
                                             db_credential_file = db_credential_file)

                    parallel_work = [(f"python3 {masks_attack_script}",)]
                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    #import pdb; pdb.set_trace()
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    #import pdb; pdb.set_trace()
                    all_cracked = False
                    for hash_type in hash_types:
                        with open(masks_file, 'r') as masks:
                            while mask := masks.readline().rstrip():
                                if not Mask.is_mask(mask):
                                    print_failure("Invalid mask: {mask}")
                                    break

                                all_cracked = Hashcat.are_all_hashes_cracked(hashes_file)
                                if not all_cracked:
                                    attack_cmd =  (
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
                                    break #all hashes were cracked so stop attack

                        if all_cracked := Hashcat.are_all_hashes_cracked(hashes_file):
                            print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                            break

                    #import pdb; pdb.set_trace()
                    if db_status and workspace and db_credential_file:
                        Hashcat.insert_hashes_to_db(hashes_file, workspace, db_credential_file)

            except Exception as error:
                print_failure(error)

        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    # modify - date: Apr 1 2021 (debugged - date Apr 3 2021)
    @staticmethod
    def gen_masks_attack(*,
                         hash_types: List[str], hashes_file: Path, masks_file: Path,
                         masks_attack_script: Path, slurm: Slurm,
                         db_status:bool, workspace:str, db_credential_file: Path):

        #import pdb; pdb.set_trace()
        parallel_job_type = slurm.parallel_job_parser()
        if not  parallel_job_type in ["GPU"]:
            raise InvalidParallelJob(parallel_job_type)

        _hc_main_exec = "{hc.main_exec}"
        _mask = "{mask}"
        _hash_type = "{hash_type}"
        _hashes_file = "{hashes_file}"
        _mask_attack = "{mask_attack}"
        _header_attack = "{header_attack}"
        _workspace = "{workspace}"

        __hash_types = f"'{hash_types}'"
        __hashes_file = f"'{hashes_file}'"
        __masks_file = f"'{masks_file}'"
        __workspace = f"'{workspace}'"
        __db_credential_file = f"'{db_credential_file}'"

        masks_attack = (
                f"""
#!/bin/env python3

from sbash import Bash

from ama.core.plugins.cracker import Hashcat
from ama.core.files import Path

hash_types = {hash_types}
hashes_file = Path({__hashes_file})
masks_file = {__masks_file}
db_status = {db_status}
workspace = {__workspace if workspace else None}
db_credential_file = Path({__db_credential_file})

hc = Hashcat()

all_cracked = False

for hash_type in hash_types:
    with open(masks_file, 'r') as masks:
        while mask := masks.readline().rstrip():
            all_cracked = Hashcat.are_all_hashes_cracked(hashes_file)
            if not all_cracked:
                mask_attack = (
                    f"srun {_hc_main_exec} -a 3"
                    f" -m {_hash_type} {_hashes_file} {_mask}"
                )

                header_attack = f"[*] Running: {_mask_attack}"
                Bash.exec(f"echo -e '\\n\\n\\n{_header_attack}'")
                Bash.exec(mask_attack)

            else:
                break

    if all_cracked := Hashcat.are_all_hashes_cracked(hashes_file):
        print(f"\\n[*] Hashes in {_hashes_file} were cracked")
        break

if db_status and workspace and db_credential_file:
    Hashcat.insert_hashes_to_db(hashes_file, workspace, db_credential_file)
                """
            )

        with open(masks_attack_script, 'w') as attack:
            attack.write(masks_attack)

        print_successful(f"Masks attack script generated: {ColorStr(masks_attack_script).StyleBRIGHT}")


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

        import pdb; pdb.set_trace()
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

                    for hash_type in hash_types:
                        for wordlist in wordlists:
                            for mask in masks:
                                all_cracked = Hashcat.are_all_hashes_cracked(hashes_file)
                                if  not all_cracked: # some hash isn't cracked yet
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

                                    print()
                                    print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                                    Bash.exec(attack_cmd)
                                    if sleep > 0:
                                        print_status(f"{ColorStr('Sleeping ...').StyleBRIGHT}")
                                        time.sleep(sleep)

                                else:
                                    print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                                    break
                            if all_cracked:
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
