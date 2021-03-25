#!/usr/bin/env python3
#
# check status (broken or not) of hash or hashes in a file
#
# date: Feb 25 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from tabulate import tabulate
from typing import Any

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
from ama.core.plugins.cracker import (
    Hashcat,
    John,
    get_availables_crackers
)

# validator imports
from ama.core.files import Path

# slurm import
from ama.core.slurm import Slurm

class HashesStatus(Auxiliary):
    """
    Check status (broken or not) of hashes in a file
    """


    DESCRIPTION = "Check hashes status"
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

    REFERENCES = None

    def __init__(self, *,
                 hashes_file:str = None, uncracked_hashes: str = None,
                 slurm=None):
        """
        Initialization of auxiliary/hashes/hashes_status ama module
        """

        auxiliary_options = {
            'hashes_file': Argument(hashes_file, True, "Hashes file to check status"),
            'uncracked_hashes': Argument(uncracked_hashes, False, "File name to save uncracked hashes")
        }

        init_options = {
            'mname' : HashesStatus.MNAME,
            'author': HashesStatus.AUTHOR,
            'description': HashesStatus.DESCRIPTION,
            'fulldescription':  HashesStatus.FULLDESCRIPTION,
            'references': HashesStatus.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': slurm
        }

        super().__init__(**init_options)


    # debugged - date: Mar 1 2021
    def run(self, quiet:bool = False, attack_output: Any = None):
        """
        Execution of auxiliary/hashes/hashes_status ama module
        """
        #import pdb; pdb.set_trace()

        crackers = get_availables_crackers()
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
                            hashes_status['cracked'].append(cracked_hash.get_loot())
                            break # break for loop

                    if not cracked:
                        hashes_status['uncracked'].append([query_hash])

            if uncracked_hashes := self.options.get('uncracked_hashes', Argument.get_empty()).value:
                with open(uncracked_hashes, 'w') as uncracked_hashes_file:
                    for uhash in hashes_status['uncracked']:
                        uncracked_hashes_file.write(f"{uhash[0]}\n") #hashes_status['uncracked'] struct is [[UNCRACKED_HASH], [OTHER_UNCRACKED_HASH], ...]

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

        except Exception as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)
