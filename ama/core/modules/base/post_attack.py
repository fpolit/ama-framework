#!/usr/bin/env python3
#
# base class to build post attack  modules
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import List
from .auxiliary import Auxiliary


class PostAttack(Auxiliary):
    """
    Base class to build post attack modules
    """
    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldescription: str, references: List[str],
                 post_attack_options: dict, slurm):

        init_options = {
            'mname': mname,
            'author': author,
            'description': description,
            'fulldescription': fulldescription,
            'references': references,
            'auxiliary_options': post_attack_options,
            'slurm': slurm
        }

        super().__init__(**init_options)

    def run(self):
        """
        Default method to run post attack module
        """
        pass
