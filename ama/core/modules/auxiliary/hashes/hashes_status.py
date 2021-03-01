#!/usr/bin/env python3
#
# check status (broken or not) of hash or hashes in a file
#
# date: Feb 25 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from tabulate import tabulate


#fineprint imports
from fineprint.status import (
    print_failure
)
# cmd2 imports
import cmd2

# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

# cracker import
from ama.core.cracker import (
    Hashcat,
    John
)

# validator imports
from ama.core.files import Path

# slurm import
from ama.core.slurm import Slurm

class HashesStatus(Auxiliary):
    """
    Check status (broken or not) of hashes in a file
    """


    DESCRIPTION = "Check status of hashes"
    MNAME = "auxiliary/hashes/hashes_status"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Check status (broken or not) of hashes in a file
        searching them in John and Hashcat potfiles
        """
    )

    def __init__(self, *,
                 query_hashes_file:str = None, slurm=None):
        """
        Initialization of auxiliary/hashes/hashes_status ama module
        """

        auxiliary_options = {
            'hashes_file': Argument(query_hashes_file, True, "Hashes file to check status")
        }

        init_options = {
            'mname' : HashesStatus.MNAME,
            'author': HashesStatus.AUTHOR,
            'description': HashesStatus.DESCRIPTION,
            'fulldescription':  HashesStatus.FULLDESCRIPTION,
            'auxiliary_options': auxiliary_options,
            'slurm': slurm
        }

        super().__init__(**init_options)


    def run(self):
        """
        Execution of auxiliary/hashes/hashes_status ama module
        """
        #import pdb; pdb.set_trace()

        crackers = [John, Hashcat]
        hashes_status = {'cracked': [], 'uncracked': []}

        try:
            permission = [os.R_OK]
            hashes_file = self.options['hashes_file'].value
            Path.access(permission, hashes_file)

            with open(hashes_file, 'r') as hashes:
                while query_hash := hashes.readline().rstrip():
                    #query_hash = queryHash[0]
                    cracked = False
                    for cracker in crackers:
                        if cracked_hash := cracker.hash_status(query_hash):
                            cracked = True
                            hashes_status['cracked'].append(cracked_hash.getAttributes())
                            break # break for loop

                    if not cracked:
                        hashes_status['uncracked'].append([query_hash])

            # print status of hashes in hashesFile
            status_hashes_table = (
                f"""
    Cracked Hashes:

{tabulate(hashes_status["cracked"],headers = ["Hash", "Type", "Password", "Cracker"])}

    Uncracked Hashes:
                
{tabulate(hashes_status["uncracked"],headers = ["Hash"])}
                """
            )

            print(status_hashes_table)
            # print("\tCracked Hashes:")
            # print(tabulate(hashes_status["cracked"],
            #                headers = ["Hash", "Type", "Password", "Cracker"]))

            # print("\tUncracked Hashes:")
            # print(tabulate(hashes_status["uncracked"],
            #                headers = ["Hash"]))

        except Exception as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)
