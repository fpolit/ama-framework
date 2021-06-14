#!/usr/bin/env python3
#
# PasswordCracker - main class to generate password crackers (john, hashcat, ...)
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from typing import List, Any
from fineprint.status import print_failure
from .crackerException import InvalidPartition
from ama.core.files import (
    Path,
    line_counter
)

from math import ceil

from .password_cracker import PasswordCracker


class HashCracker(PasswordCracker):
    """
        Hash Cracker - Base class for Hash Crackers
    """
    # Supported crackers
    HASH_CRACKERS = ["john", "hashcat"]

    def __init__(self, name, *, version=None, main_exec=None):
        super().__init__(name,
                         version = version,
                         main_exec = main_exec)

    def pylist2bash(self, pylist:list):
        bash_array = '('
        for id_list, value in enumerate(pylist):
            if id_list == (len(pylist) - 1):
                bash_array += f"'{value}')"
            else:
                bash_array += f"'{value}' "
        return bash_array

    def check_slurm_partition(self, partition:str, slurm_partitions):
        #import pdb; pdb.set_trace()
        if slurm_partitions is not None:
            valid_partition = False
            for slurm_partition in slurm_partitions:
                if partition == slurm_partition:
                    valid_partition = True
                    break
            if not valid_partition:
                raise InvalidPartition(partition, slurm_partitions.keys())
        else:
            print_failure("Slurm partition hasn't validate (slurm.conf=None)")

    # debugged - date Apr 13 2021
    def array_masks(self, masks_file:Path, ARRAY:int):
        """
        distribute masks_file into ARRAY masks file
        e.g. if weak.hcmasks has 215 masks and ARRAY=4, then array_masks split weak.hcmasks in
        weak0.hcmasks, weak1.hcmasks, weak2.hcmasks and weak3.hcmasks
        where weak0-2.hcmasks have 215/4 ~ 53 masks and weak3.hcmasks (the rest of masks)
        """

        #import pdb; pdb.set_trace()

        base_path = masks_file.parent
        name_masks_file = masks_file.name
        suffix = masks_file.suffix
        only_name_masks_file = name_masks_file[:-len(suffix)]

        nmasks = line_counter(masks_file)
        with open(masks_file, 'r') as masks:
            for a in range(ARRAY):
                INIT = ceil(nmasks/ARRAY)*a
                if a == (ARRAY - 1):
                    END = nmasks
                else:
                    END = ceil(nmasks/ARRAY)*(a+1)


                name_split_masks_file = only_name_masks_file + str(a) + suffix
                split_masks_file = Path.joinpath(base_path, name_split_masks_file)
                with open(split_masks_file, 'w') as split_masks:
                    k = INIT
                    mask = masks.readline()
                    while mask and k < END:
                        split_masks.write(mask)
                        k += 1
                        if k < END:
                            mask = masks.readline()

    def check_hash_type(hash_types: List[Any]):
        """
        Check if there is a valid hash type in hash_types list

        Args:
            hash_type (List[str]): hash types

        Raises:
            NoValidHashType: Error if there isn't a valid hash type in hash_types
        """

        any_valid_hash_type = False
        for hash_type in hash_types:
            if hash_type in self.HASHES:
                any_valid_hash_type = True
                break

        if not any_valid_hash_type:
            raise NoValidHashType(self, hash_types)

    def search_hash_type(pattern, *, sensitive=False):
        """
        Search valid hashes types given a pattern
        """
        pass

    def pattern_in_potfile(pattern, potfile:Path):
        """
        Search a supplied pattern in a porfile

        Return:
        [] if there isn't a line that match the pattern or a list of matched groups (re module)
        """
        #import pdb;pdb.set_trace()
        try:
            permission = [os.R_OK]
            Path.access(permission, potfile)

            matches = []
            with open(potfile, 'r') as potfile:
                while line := potfile.readline().rstrip():
                    if match := pattern.fullmatch(line):
                        matches.append(match)

            return matches

        except Exception as error:
            print_failure(error)

    def all_cracked(hashes_file: Path):
        """
        Check if all hashes are cracked
        return True if all hashes were cracked otherwise return False
        """
        #import pdb;pdb.set_trace()
        all_cracked = True
        with open(hashes_file, 'r') as hashes:
            while query_hash := hashes.readline().rstrip():
                status = self.hash_status(query_hash)
                if status is None: # query_hash isn't cracked yet
                    all_cracked
                    break

        return all_cracked

    # NO DEBUGGED
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
