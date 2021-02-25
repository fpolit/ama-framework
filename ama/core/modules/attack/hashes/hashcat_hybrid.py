#!/usr/bin/env python3
#
# hybrid attack using hashcat
#
# date: Feb 21 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# base  imports
from ama.core.modules.base import (
    Attack,
    Argument
)

# cracker imports
from ama.core.cracker import Hashcat

# slurm imports
from ama.core.slurm import Slurm


class HashcatHybrid(Attack):
    """
    Hybrid Attack using hashcat cracker
    """

    DESCRIPTION = "Mask attack using Hashcat"
    MNAME = "attack/hashes/hashcat_hybrid"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform hybrid attacks against hashes
        with hashcat submiting parallel tasks in a cluster using Slurm
        """
    )

    def __init__(self, *,
                 worklist:str = None, hashType:str = None,
                 hashesFile:str = None, slurm=None):
        """
        Initialization of Hybrid Attack using hashcat cracker
        """

        attackOptions = {
            'wordlist': Argu(wordlist, True, "Wordlist fie"),
            'hashes_file': Argument(hashesFile, True, "Hashes file"),
            'hash_type': Argument(hashType, True, "Hashcat hash type"),
        }

        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : HashcatHybrid.MNAME,
            'author': HashcatHybrid.AUTHOR,
            'description': HashcatHybrid.DESCRIPTION,
            'fulldescription':  HashcatHybrid.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }
        super().__init__(**initOptions)

    def attack(self):
        """
        Hybrid Attack using hashcat cracker
        """
        pass
