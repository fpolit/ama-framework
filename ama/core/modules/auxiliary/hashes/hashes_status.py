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
                 queryHash: str = None, queryHashesFile:str = None, slurm=None):
        """
        Initialization of auxiliary/hashes/hashes_status ama module
        """

        auxiliaryOptions = {
            'hashes_file': Argument(queryHashesFile, True, "Hashes file to check status")
        }


        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : HashesStatus.MNAME,
            'author': HashesStatus.AUTHOR,
            'description': HashesStatus.DESCRIPTION,
            'fulldescription':  HashesStatus.FULLDESCRIPTION,
            'auxiliaryOptions': auxiliaryOptions,
            'slurm': slurm
        }

        super().__init__(**initOptions)


    def run(self):
        """
        Execution of auxiliary/hashes/hashes_status ama module
        """
        #import pdb; pdb.set_trace()

        crackers = [John, Hashcat]
        hashesStatus = {'cracked': [], 'uncracked': []}

        try:
            permission = [os.R_OK]
            hashesFile = self.auxiliary['hashes_file'].value
            Path.access(permission, hashesFile)

            with open(hashesFile, 'r') as hashes:
                while queryHash := hashes.readline().rstrip():
                    #queryHash = queryHash[0]
                    cracked = False
                    for cracker in crackers:
                        if crackedHash := cracker.hashStatus(queryHash):
                            cracked = True
                            hashesStatus['cracked'].append(crackedHash.getAttributes())
                            break # break for loop

                    if not cracked:
                        hashesStatus['uncracked'].append([queryHash])

            # print status of hashes in hashesFile
            hashesStatusTables = (
                f"""
                Cracked Hashes

                {tabulate(hashesStatus['cracked'], headers = ['Hash', 'Type', 'Password', 'Cracker'])}
                """ ,

                f"""
                Uncracked Hashes

                {tabulate(hashesStatus['uncracked'], headers=['Hash'])}
                """
            )

            for table in hashesStatusTables:
                print(table)


        except Exception as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)
