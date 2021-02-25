#!/usr/bin/env python3
#
# combination attack using hashcat
#
# date: Feb 21 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import List

# base  imports
from ama.core.modules.base import (
    Attack,
    Argument
)

# cracker imports
from ama.core.cracker import Hashcat

# slurm imports
from ama.core.slurm import Slurm


class HashcatCombination(Attack):
    """
    Combination Attack using hashcat cracker
    """


    DESCRIPTION = "Combination attack using Hashcat"
    MNAME = "attack/hashes/hashcat_combination"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform combination attacks against hashes
        with hashcat submiting parallel tasks in a cluster using Slurm
        """
    )

    def __init__(self, *,
                 worklists: List[str] = None, hashType:int = None,
                 hashesFile: str = None, slurm=None):
        """
        Initialization of combination attack using Hashcat
        """

        attackOptions = {
            'wordlists': Argument(wordlists, True, "Wordlists to combine"),
            'hash_type': Argument(hashType, True, "Hashcat hash type"),
            'hashes_file': Argument(hashFile, True, "Hashes file")
        }


        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : HashcatCombination.MNAME,
            'author': HashcatCombination.AUTHOR,
            'description': HashcatCombination.DESCRIPTION,
            'fulldescription':  HashcatCombination.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }
        super().__init__(**initOptions)

    def attack(self):
        """
        Combination attack using Hashcat
        """
        pass
