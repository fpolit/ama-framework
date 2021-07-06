#!/usr/bin/env python3
#
# base class to build auxiliary  modules
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


class Auxiliary(Module):
    """
    Base class to build auxiliary modules
    """
    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldescription: str, references: List[str],
                 auxiliary_options: dict, slurm):

        init_options = {
            'mname': mname,
            'author': author,
            'description': description,
            'fulldescription': fulldescription,
            'references': references,
            'options': auxiliary_options,
            'slurm': slurm
        }

        super().__init__(**init_options)

    def run(self, *args, **kwargs):
        """
        Default method to run auxiliary module
        """
        pass

    def isAuxiliaryOption(self, option):
        if option in self.options:
            return True
        return False
