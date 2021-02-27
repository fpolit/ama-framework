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

# slurm import
from ama.core.slurm import Slurm

class JohnBenchmark(Attack):
    """
    john the ripper benchmark
    """

    DESCRIPTION = "John the Ripper benchmark"
    MNAME = "attack/hashes/john_benchmark"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform John benchmark submitting parallel task in a cluster using Slurm
        """
        )
    def __init__(self, slurm=None):
        """
        Initialization of John benchmark class
        """
        attackOptions = {}

        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : JohnBenchmark.MNAME,
            'author': JohnBenchmark.AUTHOR,
            'description': JohnBenchmark.DESCRIPTION,
            'fulldescription':  JohnBenchmark.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }

        super().__init__(**initOptions)


    def attack(self):
        """
        John the Ripper benchmark
        """
        jtr = John()
        jtr.benchmark(slurm = self.slurm)
