#!/usr/bin/env python3
#
# masks attack using john
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


class JohnMasks(Attack):
    """
    Mask Attack using john cracker
    """

    DESCRIPTION = "Masks attack using John The Ripper"
    MNAME = "attack/hashes/john_masks"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform mask attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )

    def __init__(self, *, hashType=None, hashesFile=None, masksFile=None, slurm=None):
        """
        Initialization of John masks attack

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hashes file to attack
        slurm (Slurm): Instance of Slurm class
        """
        attackOptions = {
            'hash_type': Argument(hashType, True, "John hash type"),
            'hashes_file': Argument(hashesFile, True, "Hashes file"),
            'masks_file': Argument(masksFile, True, "Masks file")
        }

        if slurm is None:
            slurm = Slurm()

        initOptions = {
            'mname' : JohnMasks.MNAME,
            'author': JohnMasks.AUTHOR,
            'description': JohnMasks.DESCRIPTION,
            'fulldescription':  JohnMasks.FULLDESCRIPTION,
            'attackOptions': attackOptions,
            'slurm': slurm
        }

        super().__init__(**initOptions)


    def attack(self):
        """
        masks attack using John the Ripper
        """
        jtr = John()
        jtr.masksAttack(hashType = self.attackOpt['hash_type'].value,
                        hashesFile = self.attackOpt['hashes_file'].value,
                        masksFile= self.attackOpt['masks_file'].value,
                        slurm = self.slurm)
