#!/usr/bin/env python3
#
# sth (search-that-name) - attack/hashes module
#
# date: Mar 5 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from fineprint.status import print_failure
import cmd2
from typing import List

# module.base imports
from ama.core.modules.base import (
    Attack,
    Argument,
    Auxiliary
)

# plugins imports
from ama.core.plugins.cracker import STH as CrackerSTH

# validator imports
from ama.core.validator import Args
from ama.core.files import Path


class STH(Attack):
    """
    automate the search of hashes on the most popular hash cracking websites
    """
    DESCRIPTION = "sth - search hashes on online cracking APIs"
    MNAME = "attack/hashes/sth"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]

    FULLDESCRIPTION = (
        """
        Automate the search of hashes on the most popular hash cracking websites
        """
    )

    REFERENCES = [
        "https://github.com/HashPals/Search-That-Hash"
    ]

    PRE_ATTACKS = {}
    POST_ATTACKS = {}


    def __init__(self, *,
                 hashes: str = None,
                 timeout: int = None, greppable: bool = False,
                 pre_attack: Auxiliary = None, post_attack: Auxiliary = None):

        attack_options = {
            'hashes': Argument(hashes, True, "Hashes to identify (hash or hashes file)"),
            'timeout': Argument(timeout, False, "Timeout in seconds"),
            'greppable': Argument(greppable, False, "Show output in JSON form ")
        }

        init_options = {
            'mname': STH.MNAME,
            'author': STH.AUTHOR,
            'description': STH.DESCRIPTION,
            'fulldescription': STH.FULLDESCRIPTION,
            'references': STH.REFERENCES,
            'pre_attack': pre_attack,
            'attack_options': attack_options,
            'post_attack': post_attack,
            'slurm': None
        }

        super().__init__(**init_options)

    def attack(self, *args, **kwargs):
        """
        Identify an hash or hashes in a file using hashid
        """
        try:
            #import pdb; pdb.set_trace()

            self.no_empty_required_options()
            sth = CrackerSTH()

            if os.path.isfile(self.options['hashes'].value):
                search = sth.search_hashes

            else: # HASHES option is a string (a simple hash)
                search = sth.search_hash

            search(self.options['hashes'].value,
                   timeout = self.options['timeout'].value,
                   greppable = self.options['greppable'].value)

        except Exception as error:
            print_failure(error)
