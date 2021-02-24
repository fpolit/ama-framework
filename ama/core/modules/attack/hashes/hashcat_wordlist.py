#!/usr/bin/env python3
#
# wordlist attack using hashcat
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
from ama.core.cracker import Hashcat

class HashcatWordlist(Attack):
    """
    Wordlist Attack using hashcat cracker
    """

    name = "Wordlist attack using Hashcat"
    mname = "attack/hashes/hashcat_wordlist"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    description = (
        """
        Perform wordlists attacks against hashes
        with hashcat submiting parallel tasks in a cluster using Slurm
        """
    )

    def __init__(self,
                 worklist:str = None, hashType: str = None, hashesFile: str = None, slurm):
        """
        Initialization of wordlist attack using hashcat
        """

        attackOptions = {
            'wordlist': Argument(wordlist, True, "Wordlist file"),
            'hash_type': Argument(hashType, True, "Hashcat hash type"),
            'hashes_file': Argument(hashesFile, True, "Hashes file")
        }

        initOptions = {
            'name': name,
            'mname' : nname,
            'author': author,
            'description': description,
            'atackOptions': attackOptions,
            'slurm': slurm
        }

        super().__init__(**initOptions)

    def attack(self):
        """
        Wordlist attack using Hashcat
        """
        hc = Hashcat()
        hc.wo
