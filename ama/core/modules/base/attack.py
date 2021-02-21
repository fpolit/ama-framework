#!/usr/bin/env python3
#
# base class to build attack modules
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


class Attack:
    """
    Base class to build cracker modules
    """
    def __init__(self, *,
                 name: str, mname: str, author: List[str],
                 description: str, slurm, attackOptions: dict):

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
            'attack': attackOption,

            # slurm options format: {"OPTION": [DEFAULT_VALUE, REQUIRED (booleam), DESCRIPTION (str)], ...}
            'slurm': slurm.slurmParameters
        }



    def attack(self, *args, **kwargs):
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


    def optionsMsg(self):
        """
        Show options available to set up
        """

        optionsMsg = "Module options ({self.mtype}/{self.msubtype}/{self.mname}):"

        optionHeader = ["Name", "Current Setting", "Required", "Description"]
        # attack options
        attackOpt = self.options['attack']
        formattedAttackOpt = [[nameOpt, *infoOpt] for nameOpt, infoOpt in attack.items()]
        formattedAttackOpt = tabulate(formattedAttackOpt)

        optionsMsg += f"\n\nAttack Options:\n{formattedattackopt}"

        # slurm options
        slurmOpt = self.options['slurm']
        formattedSlurmOpt = [[nameOpt, *infoOpt] for nameOpt, infoOpt in slurm.items()]
        formattedSlurmOpt = tabulate(formattedSlurmOpt)

        optionsMsg += f"\n\nSlurm Options:\n{formattedslurmopt}"

        return optionsMsg
