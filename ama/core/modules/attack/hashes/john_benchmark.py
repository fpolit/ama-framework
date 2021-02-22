#!/usr/bin/env python3
#
# john benchmark
#
# date: Feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# base  imports
from ama.core.modules.base import Attack

# cracker imports
from ama.core.cracker import John


class JohnBenchmark(Attack):
    """
    Wordlist Attack using john cracker
    """

    description = "John the Ripper benchmark"
    mname = "attack/hashes/john_benchmark"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    fuldescription = (
        """
        Perform John benchmark submitting parallel task in a cluster using Slurm
        """
        )
    def __init__(self):
        """
        Initialization of John benchmark class
        """
        attackOptions = {}

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
        jtr.benchmark(slurm = self.slurm)
