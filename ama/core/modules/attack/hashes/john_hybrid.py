#!/usr/bin/env python3
#
# hybrid attack using john
#
# date: Feb 22 2021
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

class JohnHybrid(Attack):
    """
    Hybrid Attack using john cracker
    """

    DESCRIPTION = "Hybrid attack using John The Ripper"
    MNAME = "attack/hashes/john_hybrid"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform hybrid attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )

    def __init__(self, *,
                 hashType=None, hashesFile=None, masksFile=None,
                 wordlist=None, slurm=None, inverse=False):
        """
        Initialization of John hybrid attack

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hashes file
        masksFile (str): Masks file
        wordlist (str): Wordlist
        slurm (Slurm): Instance of Slurm class
        """
        attackOptions = {
            'hash_type': Argument(hashType, True, "John hash type"),
            'hashes_file': Argument(hashesFile, True, "Hashes file"),
            'masks_file': Argument(masksFile, True, "Masks file"),
            'wordlist': Argument(wordlist, True, "Wordlist file"),
            'inverse': Argument(inverse, True, "False: wordlits + masks <> True: masks + wordlist")
        }

        if slurm is None:
            slurm = Slurm()

        initOptions = {'mname' : JohnHybrid.MNAME,
                       'author': JohnHybrid.AUTHOR,
                       'description': JohnHybrid.DESCRIPTION,
                       'fulldescription':  JohnHybrid.FULLDESCRIPTION,
                       'attackOptions': attackOptions,
                       'slurm': slurm
                       }

        super().__init__(**initOptions)


    def attack(self):
        """
        hybrid attack using John the Ripper
        """
        jtr = John()
        jtr.hybridAttack(hashType = self.attack['hash_type'].value,
                         hashesFile = self.attack['hashes_file'].value,
                         wordlist = self.attack['wordlist'].value,
                         masksFile = self.attack['masks_file'].value,
                         inverse = self.attack['inverse'].value,
                         slurm = self.slurm)
