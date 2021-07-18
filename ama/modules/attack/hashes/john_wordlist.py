#!/usr/bin/env python3
#
# wordlist attack using john
#
# Status: DEBUGGED - date: Jun 8 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>


import  argparse

from cmd2 import (
    Cmd,
    with_argparser,
    Cmd2ArgumentParser
)


import os
from typing import Any
import psutil

#from ama.core.files import Path

# base  imports
from ama.modules.base import Attack, Auxiliary
from ama.utils import Argument

# cracker imports
from ama.plugins.cracker import John

# slurm import
#from ama.slurm import Slurm

#fineprint status
from fineprint.status import (
    print_failure,
    print_status
)

from fineprint.color import ColorStr

# pre attack import
## auxiliary/hashes
# from ama.modules.auxiliary.hashes import (
#     HashID,
#     Nth
# )
# ## auxiliary/wordlist
# from ama.modules.auxiliary.wordlists import (
#     CuppInteractive
# )

# # post attack import
# ## auxiliary/hashes
# from ama.modules.auxiliary.hashes import (
#     HashesStatus
# )

class JohnWordlist(Attack):
    """
    Wordlist Attack using john cracker
    """

    DESCRIPTION = "Wordlist attack using John The Ripper"
    MNAME = "attack/hashes/john_wordlist"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform wordlists attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
    )

    REFERENCES = [
        "https://www.hackingarticles.in/beginner-guide-john-the-ripper-part-1/",
        "https://www.hackingarticles.in/beginners-guide-for-john-the-ripper-part-2/",
        "https://github.com/openwall/john"
    ]

    CRACKER = John.MAINNAME

    def __init__(self, *,
                 hash_type: str = None, hashes_file: str = None,
                 wordlists: str = None,
                 pre_attack: Auxiliary = None, post_attack: Auxiliary = None):
        """
        Initialization of John  wordlist attack

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hashes file to attack
        wordlist (str): wordlist to attack
        slurm (Slurm): Instance of Slurm class

        pre_attack (Auxiliary): Instance of a pre attack (auxiliary module)
        post_attack (Auxiliary): Instance of a post attack (auxiliary module)
        """

        attack_options = {
            'WORDLISTS': Argument(wordlists, True, "Wordlists to combine (directory or list split by commas)"),
            'EXCLUDE': Argument(None, False, "Wordlists to exclude (split by commas)"),
            'HASH_TYPE': Argument(hash_type, True, "John hash types (split by commas)", value_type=str),
            'HASHES_FILE': Argument(hashes_file, True, "hashes file", value_type=str),
            "CORES": Argument(1, False, "Number of cores to lunch MPI job (-1: MAXIMUM CORES)", value_type=int),
            "THREADS": Argument(-1, False, "Number of threads to lunch OMP job (-1: MAXIMUM THREADS)", value_type=int),
            'JOB_NAME': Argument('jtr-wordlist-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname' : JohnWordlist.MNAME,
            'authors': JohnWordlist.AUTHORS,
            'description': JohnWordlist.DESCRIPTION,
            'fulldescription':  JohnWordlist.FULLDESCRIPTION,
            'references': JohnWordlist.REFERENCES,
            'attack_options': attack_options,
            'pre_attack': pre_attack,
            'post_attack': post_attack
        }

        super().__init__(**init_options)


    def attack(self, quiet:bool = False, pre_attack_output: Any = None):
        """
        Wordlist attack using John the Ripper

        Args:
           local (bool): if local is True run attack localy otherwise
                         submiting parallel tasks in a cluster using slurm
        """

        #import pdb; pdb.set_trace()
        try:
            #self.no_empty_required_options(local)

            jtr = John()

            hash_type = self.options['HASH_TYPE'].value


            wordlists_option = self.options['WORDLISTS'].value
            exclude = set()
            if self.options['EXCLUDE'].value:
                exclude = set(self.options['EXCLUDE'].value.split(','))

            wordlists = []
            if os.path.isdir(wordlists_option):
                for wordlist_name in os.listdir(wordlists_option):
                    wordlist_file = os.path.join(wordlists_option, wordlist_name)
                    if os.path.isfile(wordlist_file) and wordlist_name not in exclude:
                        wordlists.append(wordlist_file)

            else:
                for wordlist_file in wordlists_options.split(','):
                    if os.path.isfile(wordlist_file) and wordlist_file not in exclude:
                        wordlists.append(wordlist_file)

            jtr.wordlist_attack(htype = hash_type,
                                hashes_file = self.options['HASHES_FILE'].value,
                                wordlists = wordlists,
                                cores = self.options['CORES'].value,
                                threads = self.options['THREADS'].value)

        except Exception as error:
            print_failure(error)
