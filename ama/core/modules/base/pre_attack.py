#!/usr/bin/env python3
#
# base class to build pre attack  modules
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import List
from .auxiliary import Auxiliary


class PreAttack(Auxiliary):
    """
    Base class to build pre attack modules
    """
    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldescription: str, references: List[str],
                 preattack_options: dict, slurm):

        init_options = {
            'mname': mname,
            'author': author,
            'description': description,
            'fulldescription': fulldescription,
            'references': references,
            'auxiliary_options': preattack_options,
            'slurm': slurm
        }

        super().__init__(**init_options)

    def run(self):
        """
        Default method to run pre attack module
        """
        pass

    def preattack_options_values(self):
        """
        Return the option name and value of auxiliary_options
        """
        preattack = {}
        for option, argument in self.auxiliary_options.items():
            preattack[option] = argument.value

        return preattack
