#!/usr/bin/env python3
#
# combination attack using hashcat
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

# slurm imports
from ama.core.slurm import Slurm


class HashcatCombination(Attack):
    """
    Combination Attack using hashcat cracker
    """

    name = "Wordlist attack using John The Ripper"
    mname = "attack/hashes/john_wordlist"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    description = (
        """
        Perform wordlists attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
    )

    def __init__(self, worklists, hashType, hashFile, slurm):
        """
        REWRITE
        """

        attackOptions = {
            'wordlists': Argument(wordlists, True, "Wordlists to combine"),
            'hash_type': Argument(hashType, True, "John hash type"),
            'hash_file': Argument(hashFile, True, "Hash file")
        }

        initOptions = {'name': name,
                       'mname' : nname,
                       'author': author,
                       'description': description,
                       'slurm': slurm,
                       'atackOptions': attackOptions
                       }

        super().__init__(**initOptions)

    def attack(self):
        """
        WRITE
        """
        pass
