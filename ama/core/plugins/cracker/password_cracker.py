#!/usr/bin/env python3
#
# PasswordCracker - main class to generate password crackers (john, hashcat, ...)
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from fineprint.status import print_failure
from ..plugin import Plugin
from .crackerException import InvalidPartition
from ama.core.files import (
    Path,
    line_counter
)

from math import ceil


class PasswordCracker(Plugin):
    """
        Password Cracker (hash and credential cracker) - Main Password Cracker class
    """
    # Supported crackers
    HASH_CRACKERS = ["john", "hashcat"]
    CREDENTIAL_CRACKERS = ["hydra"]

    def __init__(self, name, *, version=None, main_exec=None):
        super().__init__(name,
                         version = version,
                         main_exec = main_exec)

    @staticmethod
    def hash_status(query_hash: str, potfile: str = None):
        """
        Check the status (broken or not) of query hash or hashes file
        """
        pass # implement for each child class of PasswordCracker

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



