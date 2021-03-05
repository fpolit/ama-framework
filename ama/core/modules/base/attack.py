#!/usr/bin/env python3
#
# base class to build attack modules
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from tabulate import tabulate

from typing import (
    List,
    Any
)

# base imports
from ama.core.modules.base import Module

# table formation imports
from cmd2.table_creator import (
    Column,
    SimpleTable
)

from fineprint.status import (
    print_failure
)


class Attack(Module):
    """
    Base class to build attack modules
    """
    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldescription: str, references: List[str],
                 attack_options: dict, slurm):

        init_options = {
            'mname': mname,
            'author': author,
            'description': description,
            'fulldescription': fulldescription,
            'references': references,
            'options': attack_options,
            'slurm': slurm
        }

        super().__init__(**init_options)

    def attack(self, *args, **kwargs):
        """
        Default method to run attack module
        """
        pass

    def isAttackOption(self, option):
        if option in self.options:
            return True
        return False
