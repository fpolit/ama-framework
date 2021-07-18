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


import sys

from enum import Enum
import os
import re
from tabulate import tabulate
from sbash import Bash
from typing import List
#import psycopg2
import psutil
from math import floor
from pathlib import Path
import time

# fineprint imports
from fineprint.status import (
    print_status,
    print_failure,
    print_successful
)
from fineprint.color import ColorStr

# cracker import
from ama.plugins import Plugin
from ama.plugins.cracker import HashCracker
from ama.plugins.cracker import CrackedHash
from ama.data.hashes import jtrHashes
from ama.utils.files import access
from ama.utils.mask import Mask, MasksFile
from ama.utils.shell import Shell

# cracker exceptions imports
from .crackerException import (
    InvalidParallelJob,
    NoValidHashType
)



class JohnAttack(Enum):
    WORDLIST = 0
    COMBINATION = 1
    SINGLE = 2
    BRUTE_FORCE = 3
    MASKS = 4
    INCREMENTAL = 5
    HYBRID_WM = 6
    HYBRID_MW = 7


#from ama.core.cmdsets.db import Connection
class John(HashCracker):
    """
    John password cracker
    This class implement the diverse attack of john the ripper and its benchmark
    Suported Attacks: wordlist, incremental, masks, single, combination, hybrid
    """

    HASHES = jtrHashes
    MAINNAME = "john"

    def __init__(self, john_exec:Path=None):
        super().__init__(["john", "jtr"], version="1.9.0-jumbo-1 MPI + OMP", main_exec=john_exec)
        self.potfile = os.path.join(Path.home(), ".john/john.pot")


    def cmd_gen(self, attack_mode:JohnAttack, **kwargs):

        #import pdb; pdb.set_trace()

        if attack_mode == JohnAttack.WORDLIST:
            """
            kwargs = {'wordlists': [WLPATH, ...], 'htype':'HASH_TYPE', 'hashes_file':'HASHES_FILE'}
            """
            wordlists = kwargs.get('wordlists', [])
            htype = kwargs.get('htype', None)
            hashes_file = kwargs.get('hashes_file', '')

            if wordlists and htype and os.path.isfile(hashes_file):
                # check htype
                return [[self.main_exec, f'--format={htype}', '-w', str(wordlist), str(hashes_file)] for wordlist in wordlists]
            else:
                raise Exception(f"Invalid options to generated attack command: kwargs={kwargs}")

        elif attack_mode == JohnAttack.COMBINATION:
            pass

        elif attack_mode == JohnAttack.SINGLE:
            """
            kwargs = {'htype':'HASH_TYPE', 'hashes_file':'HASHES_FILE'}
            """
            htype = kwargs.get('htype', None)
            hashes_file = kwargs.get('hashes_file', '')

            if htype and os.path.isfile(hashes_file):
                # check htype
                return [self.main_exec, "--single", f"--format={htype}", str(hashes_file)]
            else:
                raise Exception(f"Invalid options to generated attack command: kwargs={kwargs}")

        elif attack_mode == JohnAttack.BRUTE_FORCE:
            """
            kwargs = {'mask':MASK, htype':'HASH_TYPE', 'hashes_file':'HASHES_FILE'}
            """
            mask = kwargs.get('mask', None)
            htype = kwargs.get('htype', None)
            hashes_file = kwargs.get('hashes_file', '')

            if mask and htype and os.path.isfile(hashes_file):
                if not Mask.is_mask(mask):
                    raise Exception(f"Invalid mask: {mask}")

                return [self.main_exec, f"--mask={mask}", f"--format={htype}", str(hashes_file)]
            else:
                raise Exception(f"Invalid options to generated attack command: kwargs={kwargs}")

        elif attack_mode == JohnAttack.MASKS:
            """
            kwargs = {'masks_file':MASK_FILE, htype':'HASH_TYPE', 'hashes_file':'HASHES_FILE'}
            """
            masks_file = kwargs.get('masks_file', '')
            htype = kwargs.get('htype', None)
            hashes_file = kwargs.get('hashes_file', '')

            if os.path.isfile(masks_file) and htype and os.path.isfile(hashes_file):
                masks = MasksFile.get_masks(masks_file)

                if masks:
                    return [[self.main_exec, f"--mask={mask}", f"--format={htype}", str(hashes_file)] for mask in masks]

                else:
                    raise Exception(f"Mask file {masks_file} hasn't any valid mask")

            else:
                raise Exception(f"Invalid options to generated attack command: kwargs={kwargs}")


        elif attack_mode == JohnAttack.INCREMENTAL:
            """
            kwargs = {'htype':'HASH_TYPE', 'hashes_file':'HASHES_FILE'}
            """
            htype = kwargs.get('htype', None)
            hashes_file = kwargs.get('hashes_file', '')

            if htype and os.path.isfile(hashes_file):
                # check htype
                return [self.main_exec, "--incremental", f"--format={htype}", hashes_file]
            else:
                raise Exception(f"Invalid options to generated attack command: kwargs={kwargs}")

        elif attack_mode == JohnAttack.HYBRID_MW:
            pass

        elif attack_mode == JohnAttack.HYBRID_WM:
            pass




    def search_hash_type(pattern, *, sensitive=False):
        """
        Search  john's hashes types given a pattern
        """
        if sensitive:
            hash_pattern = re.compile(rf"[\W|\w|\.]*{pattern}[\W|\w|\.]*")
        else:
            hash_pattern = re.compile(rf"[\W|\w|\.]*{pattern}[\W|\w|\.]*", re.IGNORECASE)

        filtered_hashes = []
        hashId = 0
        for hash_type in self.HASHES:
            if hash_pattern.fullmatch(hash_type):
                filtered_hashes.append((hashId, hash_type))
                hashId += 1

        print(tabulate(filtered_hashes, headers=["#", "Name"]))

    def hash_status(self, query_hash: str):
        """
        Check the status of query hash in john potfile

        Return:
        """
        pattern = re.compile(rf"(\$(\W*|\w*|.*)\$)?({query_hash})(\$(\W*|\w*|.*)\$)?:(\W*|\w*|.*)",
                             re.DOTALL)

        return self.pattern_in_potfile(pattern, self.potfile)

    # def are_all_cracked(self, hashes_file: Path):
    #     """
    #     Check if all hashes are cracked
    #     return True if all hashes were cracked otherwise return False
    #     """
    #     #import pdb;pdb.set_trace()
    #     cracked = True
    #     with open(hashes_file, 'r') as hashes:
    #         while query_hash := hashes.readline().rstrip():
    #             hstatus = self.hash_status(query_hash)
    #             if hstatus is None: # query_hash isn't cracked yet
    #                 cracked = False
    #                 break

    #     return cracked



    # debugged - date: Jun 8 2021
    def benchmark(self, *, cores=1, threads=1, local:bool = True):
        """
        Run john benchmark
        """
        #import pdb; pdb.set_trace()
        try:
            if not self.enable:
                raise Exception(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")

            max_cores = psutil.cpu_count(logical=False)
            max_threads = psutil.cpu_count(logical=True)

            if cores == -1 or cores > max_cores:
                cores = max_cores
            if threads == -1 or threads > max_threads:
                threads = max_threads

            if cores > 1:
                mpirun = Plugin(["mpirun", "mpiexec"])
                os.environ['OMP_NUM_THREADS'] = str(threads)
                attack_cmd = f"{mpirun.main_exec} -n {cores} {self.main_exec} --test"
            else:
                os.environ['OMP_NUM_THREADS'] = str(threads)
                attack_cmd = f"{self.main_exec} --test"

            print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
            Bash.exec(attack_cmd)

        except Exception as error:
            print_failure(error)

    # Status: DEBUGGED - date: Jun 8 2021
    def wordlist_attack(self , htype: str , hashes_file: Path, wordlists: List[Path],
                        rules:str = None, rules_file:Path = None,
                        cores:int = 1, threads:int = -1,):
        """
        Wordlist attack using john submiting parallel tasks in a cluster with Slurm

        Args:
        hash_type (str): Jonh's hash type
        hashes_file (str): Hash file to attack
        wordlist (str): wordlist to attack
        slurm (Slurm): Instance of Slurm class
        """

        #import pdb; pdb.set_trace()
        try:
            if not self.enable:
                raise Exception(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")

            permission = [os.R_OK]
            access(permission, hashes_file, *wordlists)

            # check hash type
            #if htype:
            #    self.check_hash_type(htype)

            if rules and rules_file:
                access(permission, rules_file)

            max_cores = psutil.cpu_count(logical=False)
            max_threads = psutil.cpu_count(logical=True)

            if cores <= -1 or cores > max_cores:
                cores = max_cores
            if threads <= -1 or threads > max_threads:
                threads = max_threads

            os.environ['OMP_NUM_THREADS'] = str(threads)


            for attack_cmd in self.cmd_gen(JohnAttack.WORDLIST, wordlists=wordlists, htype=htype, hashes_file=hashes_file):
                #all_cracked = self.are_all_cracked(hashes_file)
                all_cracked = False
                if  not all_cracked: # some hash isn't cracked yet
                    attack_cmd_str = ' '.join(attack_cmd)
                    Shell.exec(f"echo -e '\n\n[*] Running: {attack_cmd_str}'")
                    Shell.exec(attack_cmd)
                else:
                    print(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                    break

        except Exception as error:
            print(error) # print_failure



    def masks_attack(self, htype: str, hashes_file: Path, masks_file: Path):
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

        try:

            if not self.enable:
                raise Exception(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")

            permission = [os.R_OK]
            access(permission, hashes_file, masks_file)
            #if hash_types:
            #self.check_hash_type(hash_types)

            for attack_cmd in self.cmd_gen(JohnAttack.MASKS, masks_file=masks_file, htype=htype, hashes_file=hashes_file):
                all_cracked = False # check if all hashes were cracked
                if  not all_cracked: # some hash isn't cracked yet
                    attack_cmd_str = ' '.join(attack_cmd)
                    Shell.exec(f"echo -e '\n\n[*] Running: {attack_cmd_str}'")
                    Shell.exec(attack_cmd)
                else:
                    print(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                    break

        except Exception as error:
            print(error) # failure

    #     # POOR PERFORMANCE IN Combinator.wordlist (rewrite a better combinator)
    #     #Combinator.wordlist(wordlists, combinedWordlist)
    #     # self.wordlistAttack(hashType=hashType,
    #     #                     hashesFile=hashesFile,
    #     #                     wordlist=combinedWordlist)
    #     pass

    # #NOTE: John continue when the hash was cracked
    # # modify - date: Apr 1 2021 (debugged - date Apr 2 2021)
    # # debugged - date: Jun 9 2021
    # def incremental_attack(self, *,
    #                        hash_types: List[str] = None, hashes_file: str,
    #                        slurm: Slurm , local:bool = False,
    #                        db_status:bool = False, workspace:str = None, db_credential_file: Path = None):
    #     """
    #     Incemental attack using john submiting parallel tasks in a cluster with Slurm

    #     Args:
    #     hash_type (str): John's hash type
    #     hashes_file (str): Hash file to attack
    #     slurm (Slurm): Instance of Slurm class
    #     """

    #     #import pdb; pdb.set_trace()

    #     if self.enable:
    #         try:
    #             permission = [os.R_OK]
    #             Path.access(permission, hashes_file)
    #             if hash_types:
    #                 self.check_hash_type(hash_types)

    #             print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file in incremental mode")
    #             print_status(f"Possible hashes identities: {ColorStr(hash_types).StyleBRIGHT}")

    #             if (not local) and slurm:

    #                 enviroment = (
    #                     f"{self.MAINNAME.upper()}={self.main_exec}",
    #                 )

    #                 slurm.check_partition()

    #                 parallel_job_type = slurm.parallel_job_parser()
    #                 if not  parallel_job_type in [Slurm.MPI, Slurm.OMP]:
    #                     raise InvalidParallelJob(parallel_job_type)

    #                 HID = self.pylist2bash(hash_types)

    #                 variables_definition_block = (
    #                     f"HID={HID}",
    #                 )

    #                 attack_cmd = f"srun --mpi={slurm.pmix} ${self.MAINNAME.upper()} --incremental"
    #                 attack_cmd += f" --format=$IDENTITY {hashes_file}"

    #                 header_attack = f"echo -e '\\n\\n[*] Running: {attack_cmd}'"

    #                 insert_cracked_hashes = ''
    #                 if db_status and workspace and db_credential_file:
    #                     insert_cracked_hashes = (
    #                         f"amadb -c {db_credential_file} -w {workspace}"
    #                         f" --cracker {John.MAINNAME} -j {hashes_file}"
    #                     )

    #                 cracking_block = (
    #                     "for IDENTITY in ${HID[@]}; do",
    #                     "\t" + header_attack,
    #                     "\t" + attack_cmd,
    #                     "\t" + insert_cracked_hashes,
    #                     "\t" + "all_cracked=false",
    #                     "\t" + "if $all_cracked; then break; fi",
    #                     "done",
    #                     )

    #                 parallel_work = (enviroment,
    #                                  variables_definition_block,
    #                                  cracking_block)

    #                 batch_script = slurm.gen_batch_script(parallel_work)
    #                 Bash.exec(f"sbatch {batch_script}")

    #             else:
    #                 #import pdb;pdb.set_trace()
    #                 for hash_type in hash_types:
    #                     all_cracked = self.are_all_cracked(hashes_file)
    #                     if not all_cracked:
    #                         attack_cmd = (
    #                             f"{self.main_exec} --incremental"
    #                             f" --format={hash_type}"
    #                             f" {hashes_file}"
    #                         )

    #                         print("\n")
    #                         print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
    #                         Bash.exec(attack_cmd)

    #                     else:
    #                         print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
    #                         break

    #                 # if db_status and workspace and db_credential_file:
    #                 #     # rename insert_hashes_to_db function by insert2db
    #                 #     John.insert_hashes_to_db(hashes_file, workspace, db_credential_file, pretty=True)

    #         except Exception as error:
    #             print_failure(error)

    #     else:
    #         print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")



    # # modify - date: Apr 1 2021 (debugged - date: Apr 2 2021)
    # def single_attack(self, *,
    #                   hash_types: str, hashes_file: str,
    #                   slurm: Slurm, local: bool = False,
    #                   db_status:bool = False, workspace:str = None, db_credential_file: Path = None):
    #     """
    #     Single attack using john submiting parallel tasks in a cluster with Slurm

    #     Args:
    #     hash_type (str): Jonh's hash type
    #     hashes_file (str): Hashes file to attack
    #     slurm (Slurm): Instance of Slurm class
    #     """
    #     #import pdb; pdb.set_trace()

    #     if self.enable:
    #         try:
    #             permission = [os.R_OK]
    #             Path.access(permission, hashes_file)
    #             self.check_hash_type(hash_types)

    #             print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file in single attack mode")
    #             print_status(f"Possible hashes identities: {ColorStr(hash_types).StyleBRIGHT}")

    #             if (not local) and slurm:
    #                 enviroment = (
    #                     f"{self.MAINNAME.upper()}={self.main_exec}",
    #                 )

    #                 if slurm.config:
    #                     slurm.check_partition()

    #                 parallel_job_type = slurm.parallel_job_parser()
    #                 if not  parallel_job_type in [Slurm.MPI, Slurm.OMP]:
    #                     raise InvalidParallelJob(parallel_job_type)


    #                 #parallel_work = []
    #                 # for hash_type in hash_types:
    #                 #     attack_cmd = f"{self.main_exec} --single"
    #                 #     if parallel_job_type == "MPI":
    #                 #         attack_cmd = f"srun --mpi={slurm.pmix} "  + attack_cmd

    #                 #     elif parallel_job_type == "OMP":
    #                 #         attack_cmd = f"srun "  + attack_cmd

    #                 #     if hash_type:
    #                 #         attack_cmd += f" --format={hash_type}"

    #                 #     attack_cmd += f" {hashes_file}"
    #                 #     header_attack = f"echo -e '\\n\\n[*] Running: {attack_cmd}'"

    #                 #     if db_status and workspace and db_credential_file:
    #                 #         insert_cracked_hashes = (
    #                 #             f"amadb -c {db_credential_file} -w {workspace}"
    #                 #             f" --cracker {John.MAINNAME} -j {hashes_file}"
    #                 #         )
    #                 #         parallel_work.append((header_attack, attack_cmd, insert_cracked_hashes))
    #                 #     else:
    #                 #         parallel_work.append((header_attack, attack_cmd))

    #                 #     slurm_script_name = slurm.gen_batch_script(parallel_work)
    #                 #     Bash.exec(f"sbatch {slurm_script_name}")

    #             else:
    #                 #import pdb; pdb.set_trace()
    #                 for hash_type in hash_types:
    #                     all_cracked = self.are_all_cracked(hashes_file)
    #                     if  not all_cracked: # some hash isn't cracked yet
    #                         attack_cmd = (
    #                             f"{self.main_exec} --single"
    #                             f" --format={hash_type}"
    #                             f" {hashes_file}"
    #                         )

    #                         print()
    #                         print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
    #                         Bash.exec(attack_cmd)
    #                     else:
    #                         print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
    #                         break

    #                 # if db_status and workspace and db_credential_file:
    #                 #     John.insert_hashes_to_db(hashes_file, workspace, db_credential_file, pretty=True)

    #         except Exception as error:
    #             print_failure(error)
    #     else:
    #         print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    # def hybridAttack(self, *, hashType, hashesFile, wordlist, masksFile, slurm=None, inverse=False):
    #     """
    #     hybrid attack

    #     Combine wordlist + masks file (by default, when inverse=False) in other file and
    #     perform a wordlist attack with that file, if inverse=True combine masks file + wordlist
    #     """
    #     pass
    #     # print_status(f"Attacking {hashType} hashes in {hashFile} file with an hybrid MFW attack.")
    #     # hybridWordlist = "hybrid.txt"

    #     # if Mask.isMask(masksFile): # masksFile is a simple mask
    #     #     wordlist = wordlist[0]
    #     #     mask = masksFile
    #     #     with open(hybridWordlist, 'w') as outputFile:
    #     #         Combinator.genHybridWM(wordlist, mask , outputFile, inverse=False)
    #     #     print_successful(f"Combinated wordlist and mask was generated: {hybridWordlist}")

    #     # else:
    #     #     wordlist = wordlist[0]
    #     #     Combinator.hybridWMF(wordlist  = wordlist,
    #     #                          masksFile = masksFile,
    #     #                          output    = hybridWordlist)

    #     # JTRAttacks.wordlist(hashType = hashType,
    #     #                     hashFile = hashFile,
    #     #                     wordlist = hybridWordlist,
    #     #                     hpc = hpc)
