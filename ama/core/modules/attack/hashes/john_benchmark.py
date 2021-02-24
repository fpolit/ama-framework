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
    john the ripper benchmark
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
        John the Ripper benchmark
        """
        jtr = John()
        jtr.benchmark(slurm = self.slurm)
