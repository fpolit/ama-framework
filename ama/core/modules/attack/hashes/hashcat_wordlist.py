#!/usr/bin/env python3
#
# wordlist attack using hashcat
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

class HashcatWordlist(Attack):
    """
    Wordlist Attack using hashcat cracker
    """

    DESCRIPTION = "Wordlist attack using Hashcat"
    MNAME = "attack/hashes/hashcat_wordlist"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform wordlist attacks against hashes
        with hashcat submiting parallel tasks in a cluster using Slurm
        """
    )

    def __init__(self, *,
                 worklist:str = None, hashType: str = None,
                 hashesFile: str = None, slurm = None):
        """
        Initialization of wordlist attack using hashcat
        """

        attackOptions = {
            'wordlist': Argument(wordlist, True, "Wordlist file"),
            'hash_type': Argument(hashType, True, "Hashcat hash type"),
            'hashes_file': Argument(hashesFile, True, "Hashes file")
        }


        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : HashcatWordlist.MNAME,
            'author': HashcatWordlist.AUTHOR,
            'description': HashcatWordlist.DESCRIPTION,
            'fulldescription':  HashcatWordlist.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }
        super().__init__(**initOptions)

    def attack(self):
        """
        Wordlist attack using Hashcat
        """
        pass
