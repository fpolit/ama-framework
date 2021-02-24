#!/usr/bin/env python3
#
# wordlist attack using john
#
# date: Feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# base  imports
from ama.core.modules.base import Attack

# cracker imports
from ama.core.cracker import John


class JohnWordlist(Attack):
    """
    Wordlist Attack using john cracker
    """

    description = "Wordlist attack using John The Ripper"
    mname = "attack/hashes/john_wordlist"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    fuldescription = (
        """
        Perform wordlists attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )

    def __init__(self, *, hashType=None, hashesFile=None, worklist=None, slurm=None):
        """
        Initialization of John  wordlist attack

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hashes file to attack
        wordlist (str): wordlist to attack
        slurm (Slurm): Instance of Slurm class
        """
        attackOptions = {
            'wordlist': wordlist,
            'hash_type': hashType,
            'hashes_file': hashesFile
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
        Wordlist attack using John the Ripper
        """
        jtr = John()
        jtr.wordlistAttack(hashType = self.hash_type,
                           hashesFile = self.hashes_file,
                           wordlist = self.wordlist,
                           slurm = self.slurm)
