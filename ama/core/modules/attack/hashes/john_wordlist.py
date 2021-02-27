#!/usr/bin/env python3
#
# wordlist attack using john
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

class JohnWordlist(Attack):
    """
    Wordlist Attack using john cracker
    """

    DESCRIPTION = "Wordlist attack using John The Ripper"
    MNAME = "attack/hashes/john_wordlist"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform wordlists attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )

    def __init__(self, *,
                 hashType: str = None, hashesFile: str = None,
                 wordlist: str = None, slurm=None):
        """
        Initialization of John  wordlist attack

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hashes file to attack
        wordlist (str): wordlist to attack
        slurm (Slurm): Instance of Slurm class
        """
        attackOptions = {
            'wordlist': Argument(wordlist, True, "wordlist file"),
            'hash_type': Argument(hashType, True, "John hash type"),
            'hashes_file': Argument(hashesFile, True, "hashes file")
        }

        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : JohnWordlist.MNAME,
            'author': JohnWordlist.AUTHOR,
            'description': JohnWordlist.DESCRIPTION,
            'fulldescription':  JohnWordlist.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }

        super().__init__(**initOptions)


    def attack(self):
        """
        Wordlist attack using John the Ripper
        """
        jtr = John()
        jtr.wordlistAttack(hashType = self.attackOpt['hash_type'].value,
                           hashesFile = self.attackOpt['hashes_file'].value,
                           wordlist = self.attackOpt['wordlist'].value,
                           slurm = self.slurm)
