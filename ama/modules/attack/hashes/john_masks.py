#!/usr/bin/env python3
#
# masks attack using john
#
# date: Feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import Any
from pathlib import Path

from fineprint.status import (
    print_failure,
    print_status
)

from fineprint.color import ColorStr



from ama.modules.base import (
    Attack,
    Auxiliary
)

from ama.plugins.cracker import John
from ama.utils import Argument
#from ama.slurm import Slurm


# # pre attack modules
# ## auxiliary/hashes
# from ama.modules.auxiliary.hashes import (
#     HashID,
#     Nth
# )

# ## auxiliary/wordlist
# from ama.modules.auxiliary.wordlists import (
#     CuppInteractive
# )

# ## auxiliary/analysis
# from ama.modules.auxiliary.analysis import (
#     PackMaskgen,
#     PackWholegen,
#     PackPolicygen
# )

# # post attack import
# from ama.core.modules.auxiliary.hashes import HashesStatus

class JohnMasks(Attack):
    """
    Mask Attack using john cracker
    """

    DESCRIPTION = "Masks attack using John The Ripper"
    MNAME = "attack/hashes/john_masks"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform mask attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )

    REFERENCES = None

    # # {PRE_ATTACK_MNAME: PRE_ATTACK_CLASS, ...}
    # PRE_ATTACKS = {
    #     # auxiliary/hashes
    #     f"{Nth.MNAME}": Nth,
    #     f"{HashID.MNAME}": HashID,

    #     # auxiliary/analysis
    #     f"{PackMaskgen.MNAME}": PackMaskgen,
    #     f"{PackWholegen.MNAME}": PackWholegen,
    #     f"{PackPolicygen.MNAME}": PackPolicygen,

    #     # auxiliary/wordlist
    #     f"{CuppInteractive.MNAME}": CuppInteractive,
    # }

    # # {POST_ATTACK_MNAME: POST_ATTACK_CLASS, ...}
    # POST_ATTACKS = {
    #     # auxiliary/hashes
    #     f"{HashesStatus.MNAME}": HashesStatus,
    # }


    def __init__(self, *,
                 hash_type:str = None, hashes_file:str = None,
                 masks_file: str = None,
                 pre_attack:Auxiliary = None, post_attack:Auxiliary = None):
        """
        Initialization of John masks attack

        Args:
        hash_type (str): Jonh's hash type
        hashes_file (str): Hashes file to attack
        masks_file (str): Masks file
        masks_attack (str): Generated masks attack script
        slurm (Slurm): Instance of Slurm class
        """

        attack_options = {
            'MASKS_FILE': Argument(masks_file, True, "Masks file", value_type=str),
            'HASH_TYPE': Argument(hash_type, True, "John hash types(split by commas)", value_type=str),
            'HASHES_FILE': Argument(hashes_file, True, "Hashes file", value_type=str),
            "CORES": Argument(1, False, "Number of cores to lunch MPI job (-1: MAXIMUM CORES)", value_type=int),
            "THREADS": Argument(-1, False, "Number of threads to lunch OMP job (-1: MAXIMUM THREADS)", value_type=int),
            'JOB_NAME': Argument('jtr-masks-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname' : JohnMasks.MNAME,
            'authors': JohnMasks.AUTHORS,
            'description': JohnMasks.DESCRIPTION,
            'fulldescription':  JohnMasks.FULLDESCRIPTION,
            'references': JohnMasks.REFERENCES,
            'attack_options': attack_options,
            'pre_attack': pre_attack,
            'post_attack': post_attack
        }

        super().__init__(**init_options)

    def attack(self,  quiet:bool = False, pre_attack_output: Any = None):
        """
        Masks attack using John the Ripper
        Args:
          local (bool): try to perform the attack locally
        """
        #import pdb; pdb.set_trace()
        try:

            jtr = John()

            htype  = self.options['HASH_TYPE'].value
            hashes_file = Path(self.options['HASHES_FILE'].value)
            masks_file = Path(self.options['MASKS_FILE'].value)


            print(f"Attacking hashes in {ColorStr(hashes_file).StyleBRIGHT} file with {ColorStr(masks_file).StyleBRIGHT} masks file")

            jtr.masks_attack(htype = htype,
                             hashes_file = hashes_file,
                             masks_file= masks_file)

        except Exception as error:
            print_failure(error)


    # def setv(self, option, value, *, pre_attack: bool = False, post_attack: bool = False):
    #     import pdb; pdb.set_trace()
    #     super().setv(option, value, pre_attack = pre_attack, post_attack = post_attack)

    #     option = option.lower()
    #     attack ->  atack
    #     if option == "array":
    #         super().setv('output', 'slurm-%A_%a.out', pre_attack=False, post_attack=False)
