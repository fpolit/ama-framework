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
    SimpleTable
)


class Attack:
    """
    Base class to build attack modules
    """
    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldesciption: str,
                 attackOptions: dict, slurm):

        self.mname = mname
        mtype, msubtype, attackName = mname.split("/")
        self.mtype = mtype
        self.msubtype = msubtype
        self.name = attackName
        self.author = author
        self.description = description
        self.fulldesciption = fulldesciption
        self.attack = attackOptions
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
              glozanoa <glozanoa@uni.pe>
            """

        infoMsg += self.optionsMsg()

        # description module
        infoMsg += f"\n\n Description:\n{self.fulldescription}"

        return infoMsg


    def optionsMsg(self):
        """
        Show options available to set up
        """

        optionsMsg = f"Module options (self.mname):"

        optionHeader = ["Name", "Current Setting", "Required", "Description"]
        # attack options
        formattedAttackOpt = [[nameOpt.upper(), *infoOpt] for nameOpt, infoOpt in self.attack.items()]
        formattedAttackOpt = tabulate(formattedAttackOpt)

        optionsMsg += f"\n\nAttack Options:\n{formattedattackopt}"

        # slurm options
        formattedSlurmOpt = [[nameOpt.upper(), *infoOpt] for nameOpt, infoOpt in self.slurm.items()]
        formattedSlurmOpt = tabulate(formattedSlurmOpt)

        optionsMsg += f"\n\nSlurm Options:\n{formattedslurmopt}"

        return optionsMsg
