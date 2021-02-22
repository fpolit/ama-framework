#!/usr/bin/env python3
#
# base class to build auxiliary  modules
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import (
    List,
    Any
)

# table formation imports
from cmd2.table_creator import (
    Column,
    SimpleTable,
#    HorizontalAligment
)


class Auxiliary:
    """
    Base class to build auxiliary modules
    """
    def __init__(self, *,
                 name: str, mname: str, author: List[str],
                 description: str, slurm, auxiliaryOptions: dict):

        self.name = name
        self.mname = mname
        self.author = author
        self.description = description
        self.slurm = slurm
        self.options = {
            'name': name,
            'mtype': mtype,
            'subtype': msubtype,
            'author': author,
            'description': description,

            # attack options format: {"OPTION": [DEFAULT_VALUE, REQUIRED (booleam), DESCRIPTION (str)], ...}
            'auxiliary': auxiliaryOptions,

            # slurm options format: {"OPTION": [DEFAULT_VALUE, REQUIRED (booleam), DESCRIPTION (str)], ...}
            'slurm': slurm.slurmParameters
        }



    def run(self, *args, **kwargs):
        """
        Default method to perform an attack
        """
        pass

    def infoMsg(self):
        """
        Show  info and options about the attack
        """
        infoMsg = \
            f"""
                Name : {self.options['name']}
              Module : {self.mname}
             License : GPLv3

            Author:
              glozanoa <glozanoa@uni.pe>
            """

        infoMsg += self.optionsMsg()

        # description module
        infoMsg += f"\n\n Description:\n{self.description}"

        return infoMsg


    def optionsMsg(self):
        """
        Show options available to set up
        """

        optionsMsg = "Module options ({self.mtype}/{self.msubtype}/{self.mname}):"

        optionHeader = ["Name", "Current Setting", "Required", "Description"]
        # attack options
        attackOpt = self.options['attack']
        formattedAttackOpt = [[nameOpt, *infoOpt] for nameOpt, infoOpt in attackOpt.items()]
        formattedAttackOpt = tabulate(formattedAttackOpt)

        optionsMsg += f"\n\nOptions:\n{formattedattackopt}"

        # slurm options
        slurmOpt = self.options['slurm']
        formattedSlurmOpt = [[nameOpt, *infoOpt] for nameOpt, infoOpt in slurmOpt.items()]
        formattedSlurmOpt = tabulate(formattedSlurmOpt)

        optionsMsg += f"\n\nSlurm Options:\n{formattedslurmopt}"

        return optionsMsg
