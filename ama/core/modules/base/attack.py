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

# table formation imports
from cmd2.table_creator import (
    Column,
    SimpleTable
)



class Attack:
    """
    Base class to build attack modules
    """
    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldescription: str,
                 attackOptions: dict, slurm):

        self.mname = mname
        self.author = author
        self.description = description
        self.fulldesciption = fulldescription
        self.attackOpt = attackOptions
        self.slurm = slurm

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
   Name : {self.description}
 Module : {self.mname}
License : GPLv3

  Author:
            """
        for author in self.author:
            infoMsg += f"{author}\n"

        infoMsg += self.optionsMsg()

        # description module
        infoMsg += f"\n\nDescription:\n{self.fulldesciption}"

        return infoMsg


    def optionsMsg(self):
        """
        Show options available to set up
        """

        optionsMsg =(
            f"""
            Module: {self.mname}
            """
         )

        optionHeader = ["Name", "Current Setting", "Required", "Description"]
        # attack options
        formattedAttackOpt = [[name.upper(), *option.getAttributes()]
                              for name, option in self.attackOpt.items()]
        formattedAttackOpt = tabulate(formattedAttackOpt, headers=optionHeader)

        optionsMsg += f"\nModule Options:\n{formattedAttackOpt}"

        # slurm options
        slurmOptions = self.slurm.options()
        formattedSlurmOpt = [[name.upper(), *option.getAttributes()]
                             for name, option in slurmOptions.items()]
        formattedSlurmOpt = tabulate(formattedSlurmOpt, headers=optionHeader)

        optionsMsg += f"\n\nSlurm Options:\n{formattedSlurmOpt}"

        return optionsMsg


    def isVariable(self, variable):
        if variable in self.attackOpt or \
           variable in self.slurm.options():
            return True
        else:
            return False

    def isAttackVariable(self, variable):
        if variable in self.attackOpt:
            return True
        else:
            return False

    def isSlurmVariable(self, variable):
        if variable in self.slurm.options():
            return True
        else:
            return False
