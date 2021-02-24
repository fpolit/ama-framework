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


class JohnSingle(Attack):
    """
    Single Attack using john cracker
    """

    description = "Single attack using John The Ripper"
    mname = "attack/hashes/john_single"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    fuldescription = (
        """
        Perform single attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )
    def __init__(self, *, hashType=None, hashesFile=None, masksFile=None, wordlist=None, slurm=None, inverse=False):
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
            'inverse': Argument(inverse, False, "False: wordlits + masks <> True: masks + wordlist")
        }

        initOptions = {'mname' : nname,
                       'author': author,
                       'description': description,
                       'fulldescription':  fulldescription,
                       'atackOptions': attackOptions,
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
