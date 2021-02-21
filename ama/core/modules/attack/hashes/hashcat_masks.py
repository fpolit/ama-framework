#!/usr/bin/env python3
#
# masks attack using hashcat
# NOTE: rewite module (copied from john_wordlist module)
#
# date: Feb 21 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# base  imports
from ama.core.modules.base import Attack

# cracker imports
from ama.core.cracker import Hashcat

# slurm imports
from ama.core.slurm import Slurm


class HashcatMasks(Attack):
    """
    Masks Attack using hashcat cracker
    """
    def __init__(self, worklist, hashType, hashFile, slurm):
        """
        REWRITE
        """
        name = "Wordlist attack using John The Ripper"
        mname = "attack/hashes/john_wordlist"
        author = [
            "glozanoa <glozanoa@uni.pe>"
        ]
        description = \
            """
            Perform wordlists attacks against hashes
            with john submiting parallel tasks in a cluster using Slurm
            """

        attackOptions = {
            'wordlist': wordlist,
            'hash_type': hashType,
            'hash_file': hashFile
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
