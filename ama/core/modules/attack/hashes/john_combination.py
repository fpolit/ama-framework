#!/usr/bin/env python3
#
# combination attack using john
#
# date: Feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import List, Any

# base  imports
from ama.core.modules.base import (
    Attack,
    Argument
)


# cracker imports
from ama.core.plugins.cracker import John
# cracker imports
#from ama.core.cracker import John

# slurm import
from ama.core.slurm import Slurm


class JohnCombination(Attack):
    """
    Combination Attack using john cracker
    """

    DESCRIPTION = "Combination attack using John The Ripper"
    MNAME = "attack/hashes/john_combination"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform combination attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )

    def __init__(self, *,
                 hashType:str = None, hashesFile:str = None,
                 wordlists: List[str] = None, slurm=None):
        """
        Initialization of John combination attack

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hashes file to attack
        slurm (Slurm): Instance of Slurm class
        """
        attackOptions = {
            'hash_type': Argument(hashType, True, "Hashcat hash type"),
            'hashes_file': Argument(hashesFile, True, "Hashes file"),
            'wordlists': Argument(wordlists, True, "Hashes file"),
        }

        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : JohnCombination.MNAME,
            'author': JohnCombination.AUTHOR,
            'description': JohnCombination.DESCRIPTION,
            'fulldescription':  JohnCombination.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }

        super().__init__(**initOptions)


    def attack(self, local:bool = False, pre_attack_output: Any = None):
        """
        Combination attack using John the Ripper
        """
        jtr = John()
        jtr.combinationAttack(hashType = self.attackOpt['hash_type'],
                              hashesFile = self.attackOpt['hashes_file'],
                              wordlists = self.attackOpt['wordlists'],
                              slurm = self.slurm)
