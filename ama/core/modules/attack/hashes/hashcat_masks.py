#!/usr/bin/env python3
#
# masks attack using hashcat
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


class HashcatMasks(Attack):
    """
    Masks Attack using hashcat cracker
    """

    DESCRIPTION = "Mask attack using Hashcat"
    MNAME = "attack/hashes/hashcat_masks"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform masks attacks against hashes
        with hashcat submiting parallel tasks in a cluster using Slurm
        """
    )

    def __init__(self, *,
                 masksFile:str = None, hashType:str = None,
                 hashesFile:str = None, slurm=None):
        """
        Mask attack using Hashcat
        """

        attackOptions = {
            'hash_type': Argument(hashType, True, "John hash type"),
            'hashes_file': Argument(hashesFile, True, "Hashes file"),
            'masks_file': Argument(masksFile, True, "Masks file")
        }

        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : HashcatMasks.MNAME,
            'author': HashcatMasks.AUTHOR,
            'description': HashcatMasks.DESCRIPTION,
            'fulldescription':  HashcatMasks.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }
        super().__init__(**initOptions)

    def attack(self):
        """
        Masks Attack using hashcat cracker
        """
        pass
