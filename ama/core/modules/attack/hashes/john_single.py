#!/usr/bin/env python3
#
# single attack using john
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

class JohnSingle(Attack):
    """
    Single Attack using john cracker
    """

    DESCRIPTION = "Single attack using John The Ripper"
    MNAME = "attack/hashes/john_single"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform single attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )
    def __init__(self, *, hashType=None, hashesFile=None, slurm=None):
        """
        Initialization of John single attack

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hashes file to attack
        slurm (Slurm): Instance of Slurm class
        """
        attackOptions = {
            'hash_type': Argument(hashType, True, "John hash type"),
            'hashes_file': Argument(hashesFile, True, "Hashes file")
        }

        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : JohnSingle.MNAME,
            'author': JohnSingle.AUTHOR,
            'description': JohnSingle.DESCRIPTION,
            'fulldescription':  JohnSingle.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }

        super().__init__(**initOptions)


    def attack(self):
        """
        Single attack using John the Ripper
        """
        jtr = John()
        jtr.singleAttack(hashType = self.attack['hash_type'].value,
                         hashesFile = self.attack['hashes_file'].value,
                         slurm = self.slurm)
