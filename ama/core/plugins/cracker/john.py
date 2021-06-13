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
from typing import List
#import psycopg2
import psutil
from math import floor

# fineprint imports
from fineprint.status import (
    print_status,
    print_failure,
    print_successful
)
from fineprint.color import ColorStr

# cmd2 imports
import cmd2

# slurm imports
from ama.core.slurm import Slurm

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
    NoValidHashType
)

from ama.core.plugins import Plugin

#from ama.core.cmdsets.db import Connection

class John(PasswordCracker):
    """
    John password cracker
    This class implement the diverse attack of john the ripper and its benchmark
    Suported Attacks: wordlist, incremental, masks, single, combination, hybrid
    """

    HASHES = jtrHashes
    MAINNAME = "john"

    def __init__(self, john_exec:Path=None):
        super().__init__(["john", "jtr"], version="1.9.0-jumbo-1 MPI + OMP", main_exec=john_exec)

    # debugged - date: Apr 2 2021
    @staticmethod
    def check_hash_type(hash_types: List[str]):
        """
        Check if hash_type is a valid hash type

        Args:
            hash_type (str): hash type

        Raises:
            InvalidHashType: Error if the hasType is an unsopported hash type of a cracker
        """

        any_valid_hash_type = False
        for htype in hash_types:
            htype = htype.lower()
            if htype in John.HASHES:
                any_valid_hash_type = True
                break

        if not any_valid_hash_type:
            raise NoValidHashType(John, hash_types)

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


    # debugged - date: Apr 2 2021
    @staticmethod
    def hash_status(query_hash: str, potfile: Path = None):
        """
        Check the status (broken by John or not) of query hash

        Return:
        if query_hash is in potfile then [HASHTYPE, HASH, PASSWORD] list is returned
        otherwise None is returned
        """
        #import pdb;pdb.set_trace()

        if potfile is None:
            HOME = Path.home()
            potfile = Path.joinpath(HOME, ".john/john.pot")

        try:
            permission = [os.R_OK]
            Path.access(permission, potfile)

            cracked_pattern = re.compile(rf"(\$(\W*|\w*|.*)\$)?({query_hash})(\$(\W*|\w*|.*)\$)?:(\W*|\w*|.*)",
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

    # debugged - date Apr 2 2021
    @staticmethod
    def are_all_hashes_cracked(hashes_file: Path, potfile: Path = None):
        """
        Check if all hashes are cracked
        return True if all hashes were cracked otherwise return False
        """

        #import pdb; pdb.set_trace()
        all_cracked = True
        query_hash_pattern = re.compile(r"(\w*|\w*|.*):?(\w*|\w*|.*)") #parser to analize: NAME:HASH hashes
        with open(hashes_file, 'r') as hashes:
            while qhash := hashes.readline().rstrip():
                if parser_hash := query_hash_pattern.fullmatch(qhash):
                    query_hash = None
                    if parser_hash.group(2):
                        query_hash = parser_hash.group(2)
                    else:
                        query_hash = parser_hash.group(1)

                    cracked_hash = John.hash_status(query_hash, potfile)
                    if cracked_hash is None: # query_hash isn't cracked yet
                        all_cracked = False
                        break
                else:
                    all_cracked = False
                    break

        return all_cracked


    # debugged - date Apr 2 2021
    @staticmethod
    def hashes_file_status(hashes_file: Path, potfile:Path = None):
        """
        Check the status (broken by John or not) of hashes in query_hashes_file
        and return the cracked and uncracked hashes
        """
        #import pdb; pdb.set_trace()
        hashes_status = {'cracked': [], "uncracked": []}

        if potfile is None:
            HOME = Path.home()
            potfile = Path.joinpath(HOME, ".john/john.pot")

        try:
            permission = [os.R_OK]
            Path.access(permission, potfile, hashes_file)


            with open(hashes_file, 'r') as hashes:
                while qhash := hashes.readline().rstrip():
                    query_hash_pattern = re.compile(r"(\w*|\w*|.*):?(\w*|\w*|.*)") #parser to analize: NAME:HASH hashes
                    if parser_hash := query_hash_pattern.fullmatch(qhash):
                        query_hash = None
                        if parser_hash.group(2):
                            query_hash = parser_hash.group(2)
                        else:
                            query_hash = parser_hash.group(1)

                        if cracker_hash := John.hash_status(query_hash):
                            hashes_status['cracked'].append(cracker_hash.get_loot())
                        else: #crackedHash is uncracked
                            hashes_status['uncracked'].append([query_hash])
                    else:
                        hashes_status['uncracked'].append([qhash])

            return hashes_status

        except Exception as error:
            print_failure(error)


    # debugged - date: Apr 2 2021
    @staticmethod
    def insert_hashes_to_db(hashes_file: Path, workspace: str, creds_file: Path, *, pretty:bool = False):
        pass
        # cur = db_conn = None
        # try:
        #     #import pdb;pdb.set_trace()
        #     hashes_status = John.hashes_file_status(hashes_file)
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

        #         cur.executemany(insert_cracked_hash, new_cracked_hashes)
        #         if pretty:
        #             print_status(f"Cracked hashes were saved to {ColorStr(workspace).StyleBRIGHT} workspace database")
        #         else:
        #             print(f"\n[*] Cracked hashes were saved to {workspace} workspace database")

        #     else:
        #         if pretty:
        #             print_status(f"No new cracked hashes to save to {ColorStr(workspace).StyleBRIGHT} workspace database")
        #         else:
        #             print(f"\n[*] No new cracked hashes to save to {workspace} workspace database")

        #     db_conn.commit()
        #     cur.close()

        # except Exception as error:
        #     print_failure(error)

        # finally:
        #     if cur is not None:
        #         cur.close()

        #     if db_conn is not None:
        #         db_conn.close()


    # debugged - date: Jun 8 2021
    def benchmark(self, *, cores=1, threads=1, slurm=None, local:bool = True):
        """
        Run john benchmark
        """
        #import pdb; pdb.set_trace()
        try:
            if self.enable:
                if (not local) and slurm and slurm.partition:

                    enviroment = (
                        f"{self.MAINNAME.upper()}={self.main_exec}",
                    )

                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["MPI", "OMP", "MPI_OMP"]:
                        raise InvalidParallelJob(parallel_job_type)

                    attack_cmd = f"srun --mpi={slurm.pmix} ${self.MAINNAME.upper()} --test"
                    header_attack = f"echo -e \"\\n\\n[*] Running: {attack_cmd}\""

                    parallel_work = [enviroment, (header_attack, attack_cmd)]
                    batch_script_name = slurm.gen_batch_script(parallel_work)

                    Bash.exec(f"sbatch {batch_script_name}")

                else:
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
            else:
                raise Exception(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")

        except Exception as error:
            print_failure(error)

    # Status: DEBUGGED - date: Jun 8 2021
    def wordlist_attack(self , *, cores:int = 1, threads:int = -1,
                        hash_types: List[str] = None , hashes_file: Path, wordlists: List[Path],
                        rules:str = None, rules_file:Path = None,
                        slurm: Slurm, local:bool = False,
                        db_status:bool = False, workspace:str = None, db_credential_file: Path = None):
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
                Path.access(permission, hashes_file, *wordlists)

                if hash_types:
                    John.check_hash_type(hash_types)

                if rules and rules_file:
                    Path.access(permission, rules_file)

                print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file in wordlist mode")
                print_status(f"Wordlists: {ColorStr(wordlists).StyleBRIGHT}")
                print_status(f"Possible hashes identities: {ColorStr(hash_types).StyleBRIGHT}")

                #import pdb; pdb.set_trace()
                if (not local) and slurm and slurm.partition:
                    enviroment = (
                        f"{self.MAINNAME.upper()}={self.main_exec}",
                    )

                    if slurm.config:
                        self.check_slurm_partition(slurm.partition, slurm.config['partitions'])

                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in [Slurm.MPI, Slurm.OMP, slurm.MPI_OMP]:
                        raise InvalidParallelJob(parallel_job_type)

                    hash_types_len = len(hash_types)
                    wordlists_len = len(wordlists)
                    array_tasks = slurm.sbatch['array'].value
                    #import pdb;pdb.set_trace()
                    if array_tasks is None:
                        array_tasks = 1

                    if array_tasks > 1:
                        if array_tasks > wordlists_len:
                            print_failure(f"These is more array jobs that work to process (ARRAY={array_tasks}, WLS={wordlists_len})")
                            print_status(f"Adjusting {ColorStr('ARRAY').StyleBRIGHT} to {wordlists_len} (1 job per wordlist)")
                            array_tasks = wordlists_len
                            slurm.set_option('array', array_tasks)

                        for array_task_id in range(array_tasks):
                            init = floor(wordlists_len/array_tasks)*array_task_id
                            if array_task_id == (array_tasks - 1):
                                end = wordlists_len
                            else:
                                end = floor(wordlists_len/array_tasks)*(array_task_id+1)

                            print_status(f"(array id {array_task_id}) Processing: wordlists={ColorStr(wordlists[init:end]).StyleBRIGHT}, hash_types={ColorStr('ALL').StyleBRIGHT}")

                        WLS = self.pylist2bash(wordlists)
                        HID = self.pylist2bash(hash_types)
                        ARRAY = slurm.sbatch['array'].value  #array enumeration:  0-(ARRAY-1)
                        LEN_WLS = "${#WLS[@]}"
                        INIT = "$((LEN_WLS/ARRAY * SLURM_ARRAY_TASK_ID))"
                        END = "$((LEN_WLS/ARRAY * (SLURM_ARRAY_TASK_ID+1)))"

                        variable_definition_block = (
                            f"WLS={WLS}",
                            f"HID={HID}",
                            f"LEN_WLS={LEN_WLS}",
                            f"ARRAY={ARRAY}",
                            f"INIT={INIT}",
                            "\nif [[ $SLURM_ARRAY_TASK_ID -eq $((ARRAY -1)) ]]; then",
                            "\t" + "END=$LEN_WLS",
                            "else",
                            "\t" + f"END={END}",
                            "fi",
                        )

                    else:
                        WLS = self.pylist2bash(wordlists)
                        HID = self.pylist2bash(hash_types)
                        INIT = 0
                        END = wordlists_len

                        variable_definition_block = (
                            f"WLS={WLS}",
                            f"HID={HID}",
                            f"INIT={INIT}",
                            f"END={END}",
                        )


                    attack_cmd = f"srun --mpi={slurm.pmix} ${self.MAINNAME.upper()}"
                    attack_cmd += " --format=$IDENTITY"
                    attack_cmd += " -w $WL"

                    if rules and rules_file:
                        attack_cmd += f" --rules={rules} {rules_file}"

                    attack_cmd += f" {hashes_file}"
                    header_attack = f"echo -e \"\\n\\n[*] Running: {attack_cmd}\""

                    insert_cracked_hashes = ''
                    if db_status and workspace and db_credential_file:
                        insert_cracked_hashes = (
                            f"amadb -c {db_credential_file} -w {workspace}"
                            f" --cracker {John.MAINNAME} -j {hashes_file}"
                        )

                    cracking_block = (
                        "for WL in ${WLS[@]:INIT:END-INIT}; do",
                        "\tfor IDENTITY in ${HID[@]}; do",
                        "\t\t" + header_attack,
                        "\t\t" + attack_cmd,
                        "\t\t" + insert_cracked_hashes,
                        "\t\t" + "all_cracked=false",
                        "\t\t" + "if $all_cracked; then break; fi",
                        "\tdone",
                        "done"
                    )

                    parallel_work = (enviroment,
                                     variable_definition_block,
                                     cracking_block)


                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    #import pdb;pdb.set_trace()
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    #import pdb;pdb.set_trace()
                    max_cores = psutil.cpu_count(logical=False)
                    max_threads = psutil.cpu_count(logical=True)

                    if cores <= -1 or cores > max_cores:
                        cores = max_cores
                    if threads <= -1 or threads > max_threads:
                        threads = max_threads

                    os.environ['OMP_NUM_THREADS'] = str(threads)
                    if cores > 1:
                        mpirun = Plugin(["mpirun", "mpiexec"])

                    for hid in hash_types:
                        for wl in wordlists:
                            all_cracked = John.are_all_hashes_cracked(hashes_file)
                            if  not all_cracked: # some hash isn't cracked yet
                                attack_cmd = f"{self.main_exec} --wordlist={wl} --format={hid}"

                                if cores > 1:
                                    attack_cmd = f"{mpirun.main_exec} -n {cores} " + attack_cmd

                                if rules and rules_file:
                                    attack_cmd += f" --rules={rules} {rules_file}"

                                attack_cmd += f" {hashes_file}"

                                print("\n")
                                print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                                Bash.exec(attack_cmd)

                            else:
                                print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                                break
                        if all_cracked:
                            break

                    if db_status and workspace and db_credential_file:
                        John.insert_hashes_to_db(hashes_file, workspace, db_credential_file, pretty=True)

            except Exception as error:
                print_failure(error)

        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    def combination_attack(self,* , hashType, hashesFile, wordlists=[], slurm,
                          combinedWordlist="combined.txt"):
        # John.checkAttackArgs(_hashType=hashType,
        #                      _hashFile=hashFile,
        #                      _wordlist=wordlists)


        # POOR PERFORMANCE IN Combinator.wordlist (rewrite a better combinator)
        #Combinator.wordlist(wordlists, combinedWordlist)
        # self.wordlistAttack(hashType=hashType,
        #                     hashesFile=hashesFile,
        #                     wordlist=combinedWordlist)
        pass

    #NOTE: John continue when the hash was cracked
    # modify - date: Apr 1 2021 (debugged - date Apr 2 2021)
    # debugged - date: Jun 9 2021
    def incremental_attack(self, *,
                           hash_types: List[str] = None, hashes_file: str,
                           slurm: Slurm , local:bool = False,
                           db_status:bool = False, workspace:str = None, db_credential_file: Path = None):
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
                if hash_types:
                    John.check_hash_type(hash_types)

                print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file in incremental mode")
                print_status(f"Possible hashes identities: {ColorStr(hash_types).StyleBRIGHT}")

                if (not local) and slurm and slurm.partition:

                    enviroment = (
                        f"{self.MAINNAME.upper()}={self.main_exec}",
                    )

                    if slurm.config is not None:
                        self.check_slurm_partition(slurm.partition, slurm.config['partitions'])

                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in [Slurm.MPI, Slurm.OMP]:
                        raise InvalidParallelJob(parallel_job_type)

                    HID = self.pylist2bash(hash_types)

                    variables_definition_block = (
                        f"HID={HID}",
                    )

                    attack_cmd = f"srun --mpi={slurm.pmix} ${self.MAINNAME.upper()} --incremental"
                    attack_cmd += f" --format=$IDENTITY {hashes_file}"

                    header_attack = f"echo -e '\\n\\n[*] Running: {attack_cmd}'"

                    insert_cracked_hashes = ''
                    if db_status and workspace and db_credential_file:
                        insert_cracked_hashes = (
                            f"amadb -c {db_credential_file} -w {workspace}"
                            f" --cracker {John.MAINNAME} -j {hashes_file}"
                        )

                    cracking_block = (
                        "for IDENTITY in ${HID[@]}; do",
                        "\t" + header_attack,
                        "\t" + attack_cmd,
                        "\t" + insert_cracked_hashes,
                        "\t" + "all_cracked=false",
                        "\t" + "if $all_cracked; then break; fi",
                        "done",
                        )

                    parallel_work = (enviroment,
                                     variables_definition_block,
                                     cracking_block)

                    batch_script = slurm.gen_batch_script(parallel_work)
                    Bash.exec(f"sbatch {batch_script}")

                else:
                    #import pdb;pdb.set_trace()
                    for hash_type in hash_types:
                        all_cracked = John.are_all_hashes_cracked(hashes_file)
                        if not all_cracked:
                            attack_cmd = (
                                f"{self.main_exec} --incremental"
                                f" --format={hash_type}"
                                f" {hashes_file}"
                            )

                            print("\n")
                            print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                            Bash.exec(attack_cmd)

                        else:
                            print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                            break

                    if db_status and workspace and db_credential_file:
                        # rename insert_hashes_to_db function by insert2db
                        John.insert_hashes_to_db(hashes_file, workspace, db_credential_file, pretty=True)

            except Exception as error:
                print_failure(error)

        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    #debugged - date: Jun 5 2021
    def masks_attack(self, *,
                     hash_types: List[str] = None, hashes_file: Path, masks_file: Path,
                     slurm: Slurm, local: bool = False,
                     db_status:bool = False, workspace:str = None, db_credential_file: Path = None):
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
                if hash_types:
                    John.check_hash_type(hash_types)

                print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file with {ColorStr(masks_file).StyleBRIGHT} masks file")
                print_status(f"Possible hashes identities: {ColorStr(hash_types).StyleBRIGHT}")

                if (not local) and slurm and slurm.partition:
                    enviroment = (
                        f"{self.MAINNAME.upper()}={self.main_exec}",
                    )

                    if slurm.config:
                        self.check_slurm_partition(slurm.partition, slurm.config['partitions'])

                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in [Slurm.MPI, Slurm.OMP]:
                        raise InvalidParallelJob(parallel_job_type)

                    array_tasks = slurm.sbatch['array'].value
                    if array_tasks is None:
                        array_tasks = 1


                    base_path = masks_file.parent
                    name_masks_file = masks_file.name
                    suffix = masks_file.suffix
                    if array_tasks > 1:
                        self.array_masks(masks_file, array_tasks)
                        only_name_masks_file = name_masks_file[:-len(suffix)]

                        for a in range(array_tasks):
                            name_split_masks_file = only_name_masks_file + str(a) + suffix
                            split_masks_file = Path.joinpath(base_path, name_split_masks_file)
                            print_status(f"(array id {a}) Processing: masks file = {split_masks_file}")

                        MASKS_FILE = only_name_masks_file + "${SLURM_ARRAY_TASK_ID}" + suffix

                    else:
                        MASKS_FILE = masks_file.name

                    MASKS_FILE = Path.joinpath(base_path, MASKS_FILE)
                    HASHES_FILE = hashes_file
                    HID = self.pylist2bash(hash_types)
                    #ARRAY = slurm.sbatch['array'].value

                    variable_definition_block = (
                        f"HASHES_FILE={HASHES_FILE}",
                        f"MASKS_FILE={MASKS_FILE}",
                        f"HID={HID}",
                        #f"ARRAY="
                    )

                    attack_cmd = (
                        f"srun --mpi={slurm.pmix} ${self.MAINNAME.upper()}"
                        " --mask=$MASK"
                        " --format=$IDENTITY"
                        " $HASHES_FILE"
                    )

                    header_attack = f"echo -e \"\\n\\n[*] Running: {attack_cmd}\""

                    insert_cracked_hashes = ''
                    if db_status and workspace and db_credential_file:
                        insert_cracked_hashes = (
                            f"amadb -c {db_credential_file} -w {workspace}"
                            f" --cracker {John.MAINNAME} -j {hashes_file}"
                        )

                    cracking_block = (
                        "while read MASK",
                        "do",
                        "\tfor IDENTITY in ${HID[@]}; do",
                        "\t\t" + header_attack,
                        "\t\t" + attack_cmd,
                        "\t\t" + insert_cracked_hashes,
                        "\t\t" + "all_cracked=false",
                        "\t\t" + "if $all_cracked; then break; fi",
                        "\tdone",
                        "done < $MASKS_FILE"
                    )

                    parallel_work = (
                        enviroment,
                        variable_definition_block,
                        cracking_block
                    )

                    slurm_script_name = slurm.gen_batch_script(parallel_work)
                    import pdb; pdb.set_trace()
                    Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    all_cracked = False
                    for hash_type in hash_types:
                        with open(masks_file, 'r') as masks:
                            while mask := masks.readline().rstrip():
                                all_cracked = John.are_all_hashes_cracked(hashes_file)
                                if not all_cracked:
                                    attack_cmd = f"{self.main_exec} --mask={mask}"

                                    if hash_type:
                                        attack_cmd += f" --format={hash_type}"
                                    attack_cmd += f" {hashes_file}"

                                    print("\n")
                                    print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                                    Bash.exec(attack_cmd)

                                else:
                                    break

                        if all_cracked := John.are_all_hashes_cracked(hashes_file):
                            print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                            break

                    if db_status and workspace and db_credential_file:
                        John.insert_hashes_to_db(hashes_file, workspace, db_credential_file, pretty=True)

            except Exception as error:
                print_failure(error)

        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    # modify - date: Apr 1 2021 (debugged - date: Apr 2 2021)
    def single_attack(self, *,
                      hash_types: str, hashes_file: str,
                      slurm: Slurm, local: bool = False,
                      db_status:bool = False, workspace:str = None, db_credential_file: Path = None):
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
                John.check_hash_type(hash_types)

                #cmd2.Cmd.poutput(f"Attacking {hashType} hashes in {hashesFile} using single attack.")
                print_status(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file in single attack mode")
                print_status(f"Possible hashes identities: {ColorStr(hash_types).StyleBRIGHT}")

                if (not local) and slurm and slurm.partition:
                    enviroment = (
                        f"{self.MAINNAME.upper()}={self.main_exec}",
                    )

                    if slurm.config:
                        self.check_slurm_partition(slurm.partition, slurm.config['partitions'])

                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in [Slurm.MPI, Slurm.OMP]:
                        raise InvalidParallelJob(parallel_job_type)


                    #parallel_work = []
                    # for hash_type in hash_types:
                    #     attack_cmd = f"{self.main_exec} --single"
                    #     if parallel_job_type == "MPI":
                    #         attack_cmd = f"srun --mpi={slurm.pmix} "  + attack_cmd

                    #     elif parallel_job_type == "OMP":
                    #         attack_cmd = f"srun "  + attack_cmd

                    #     if hash_type:
                    #         attack_cmd += f" --format={hash_type}"

                    #     attack_cmd += f" {hashes_file}"
                    #     header_attack = f"echo -e '\\n\\n[*] Running: {attack_cmd}'"

                    #     if db_status and workspace and db_credential_file:
                    #         insert_cracked_hashes = (
                    #             f"amadb -c {db_credential_file} -w {workspace}"
                    #             f" --cracker {John.MAINNAME} -j {hashes_file}"
                    #         )
                    #         parallel_work.append((header_attack, attack_cmd, insert_cracked_hashes))
                    #     else:
                    #         parallel_work.append((header_attack, attack_cmd))

                    #     slurm_script_name = slurm.gen_batch_script(parallel_work)
                    #     Bash.exec(f"sbatch {slurm_script_name}")

                else:
                    #import pdb; pdb.set_trace()
                    for hash_type in hash_types:
                        attack_cmd = f"{self.main_exec} --single"
                        are_all_hashes_cracked = John.are_all_hashes_cracked(hashes_file)
                        if  not are_all_hashes_cracked: # some hash isn't cracked yet
                            if hash_type:
                                attack_cmd += f" --format={hash_type}"

                            attack_cmd += f" {hashes_file}"

                            print()
                            print_status(f"Running: {ColorStr(attack_cmd).StyleBRIGHT}")
                            Bash.exec(attack_cmd)
                        else:
                            print_successful(f"Hashes in {ColorStr(hashes_file).StyleBRIGHT} were cracked")
                            break

                    if db_status and workspace and db_credential_file:
                        John.insert_hashes_to_db(hashes_file, workspace, db_credential_file, pretty=True)

            except Exception as error:
                print_failure(error)
        else:
            print_failure(f"Cracker {ColorStr(self.main_name).StyleBRIGHT} is disable")


    def hybridAttack(self, *, hashType, hashesFile, wordlist, masksFile, slurm=None, inverse=False):
        """
        hybrid attack

        Combine wordlist + masks file (by default, when inverse=False) in other file and
        perform a wordlist attack with that file, if inverse=True combine masks file + wordlist
        """

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


