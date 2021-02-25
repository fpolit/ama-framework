#!/usr/bin/env python3
#
# incremental attack using hashcat
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


class HashcatIncremental(Attack):
    """
    Incremental Attack using hashcat cracker
    """


    DESCRIPTION = "Incremental attack using Hashcat"
    MNAME = "attack/hashes/hashcat_incremental"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform incremental attacks against hashes
        with hashcat submiting parallel tasks in a cluster using Slurm
        """
    )

    def __init__(self, *,
                 hashType:int = None, hashFile:str = None, slurm=None):
        """
        Initialization of incremental attack using Hashcat
        """

        attackOptions = {
            'hash_type': Argument(hashType, True, "Hashcat hash type"),
            'hashes_file': Argument(hashesFile, True, "Hashes file"),
        }


        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : HashcatIncremental.MNAME,
            'author': HashcatIncremental.AUTHOR,
            'description': HashcatIncremental.DESCRIPTION,
            'fulldescription':  HashcatIncremental.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }
        super().__init__(**initOptions)

    def attack(self):
        """
        WRITE
        """
        pass
