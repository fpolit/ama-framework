#!/usr/bin/env python3
#
# hybrid attack using john
#
# date: Feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# base  imports
from ama.core.modules.base import Attack

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
            'hash_type': hashType,
            'hashes_file': hashesFile,
            'masks_file': masksFile,
            'wordlist': wordlist,
            'inverse': inverse
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
        jtr.hybridAttack(hashType = self.hash_type,
                         hashesFile = self.hashes_file,
                         wordlist = self.wordlist,
                         masksFile = self.masks_file,
                         slurm = self.slurm,
                         inverse = self.inverse)
