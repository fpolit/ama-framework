#!/usr/bin/env python3
#
# check status (broken or not) of hash or hashes in a file
#
# debugged - date Apr 3 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from tabulate import tabulate
from typing import Any

#fineprint imports
from fineprint.status import (
    print_failure,
    print_status
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
    John,
    Hashcat
)
from ama.core.plugins.cracker.availables import (
    get_availables_hashes_crackers
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
        Check status (broken or not) of hashes
        searching them in hash cracker's potfiles.
        If no cracker is supplied, then search hashes in potfile of
        all availables hash crackers supported by ama
        """
    )

    REFERENCES = None

    def __init__(self, *,
                 hashes_file:str = None, uncracked_hashes: str = None,
                 slurm=None, cracker = None, potfile:Path = None):
        """
        Initialization of auxiliary/hashes/hashes_status ama module
        """

        auxiliary_options = {
            'hashes_file': Argument(hashes_file, True, "Hashes file to check status"),
            'uncracked_hashes': Argument(uncracked_hashes, False, "File to save uncracked hashes"),
            'cracker': Argument(cracker, False, f"Hash cracker (<{John.MAINNAME}|{Hashcat.MAINNAME}>)"),
            'potfile': Argument(potfile, False, "Potfile of hash cracker"),
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

        global_hashes_status = {'cracked': [], 'uncracked': []}

        try:
            cracker_name = self.options['cracker'].value
            if cracker_name is not None:
                if cracker_name not in [John.MAINNAME, Hashcat.MAINNAME]:
                    raise Exception("Selected invalid cracker: {cracker_name}")
                elif cracker_name == John.MAINNAME:
                    crackers = [John]
                else: #cracker_name == Hashcat.MAINNAME
                    crackers = [Hashcat]
            else:
                crackers = get_availables_hashes_crackers()


            hashes_file = self.options['hashes_file'].value
            potfile = self.options['potfile'].value


            for cracker in crackers:
                hashes_status = cracker.hashes_file_status(hashes_file, potfile)

                for cracked_hash in hashes_status['cracked']:
                    if cracked_hash not in global_hashes_status['cracked']:
                        global_hashes_status['cracked'].append(cracked_hash)

                for uncracked_hash in hashes_status['uncracked']:
                    if uncracked_hash not in global_hashes_status['uncracked']:
                        global_hashes_status['uncracked'].append(uncracked_hash)

            if uncracked_hashes := self.options.get('uncracked_hashes', Argument.get_empty()).value:
                with open(uncracked_hashes, 'w') as uncracked_hashes_file:
                    #hashes_status['uncracked'] struct is [[UNCRACKED_HASH], [OTHER_UNCRACKED_HASH], ...]
                    for [uhash] in global_hashes_status['uncracked']:
                        uncracked_hashes_file.write(f"{uhash}\n")

                print_status(f"Uncracked hashes have written to {uncracked_hashes} file")


            # print status of hashes in hashesFile
            if not quiet:
                status_hashes_table = (
                    f"""
        Cracked Hashes:

{tabulate(global_hashes_status["cracked"],headers = ["Hash", "Type", "Password", "Cracker"])}

        Uncracked Hashes:

{tabulate(global_hashes_status["uncracked"],headers = ["Hash"])}
                """
                )

                print(status_hashes_table)

            return hashes_status

        except Exception as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)
