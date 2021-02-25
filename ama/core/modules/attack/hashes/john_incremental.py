#!/usr/bin/env python3
#
# incremental attack using john
# NOTE: rewite module (copied from john_wordlist module)
#
# date: Feb 21 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# base  imports
from ama.core.modules.base import (
    Attack,
    Argument
)

# cracker imports
from ama.core.cracker import John

# slurm import
from ama.core.slurm import Slurm

class JohnIncremental(Attack):
    """
    Wordlist Attack using john cracker
    """

    DESCRIPTION = "Incremental attack using John The Ripper"
    MNAME = "attack/hashes/john_incremental"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform incremental attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )

    def __init__(self, *, hashType=None, hashesFile=None, slurm=None):
        """
        Initialization of John incremental attack

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hash file to attack
        slurm (Slurm): Instance of Slurm class
        """
        attackOptions = {
            'hash_type': Argument(hashType, True, "John hash type"),
            'hashes_file': Argument(hashesFile, True, "Hashes file")
        }

        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : JohnIncremental.MNAME,
            'author': JohnIncremental.AUTHOR,
            'description': JohnIncremental.DESCRIPTION,
            'fulldescription':  JohnIncremental.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }

        super().__init__(**initOptions)


    def attack(self):
        """
        Incremental attack using John the Ripper
        """
        jtr = John()
        jtr.incremtalAttack(hashType = self.attack['hash_type'].value,
                            hashesFile = self.attack['hashes_file'].value,
                            slurm = self.slurm)
