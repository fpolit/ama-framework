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



class JohnMasks(Attack):
    """
    Mask Attack using john cracker
    """

    description = "Masks attack using John The Ripper"
    mname = "attack/hashes/john_masks"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    fuldescription = (
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
        masks attack using John the Ripper
        """
        jtr = John()
        jtr.masksAttack(hashType = self.attack['hash_type'].value,
                        hashesFile = self.attack['hashes_file'].value,
                        masksFile= self.attack['masks_file'].value,
                        slurm = self.slurm)
