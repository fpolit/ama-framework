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
    SimpleTable
)


class Auxiliary:
    """
    Base class to build auxiliary modules
    """
    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldescription: str,
                 auxiliaryOptions: dict, slurm):

        self.mname = mname
        mtype, msubtype, auxiliaryName = mname.split("/")
        self.mtype = mtype
        self.msubtype = msubtype
        self.name = auxiliaryName
        self.author = author
        self.description = description
        self.fulldescription = fulldescription
        self.auxiliary = auxiliaryOptions
        self.slurm = slurm


    def run(self, *args, **kwargs):
        """
        Default method to run the auxiliary module
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

        optionsMsg = f"Module options ({self.mname}):"

        optionHeader = ["Name", "Current Setting", "Required", "Description"]

        # auxiliary options
        formattedAttackOpt = [[nameOpt.upper(), *infoOpt] for nameOpt, infoOpt in self.auxiliary.items()]
        formattedAttackOpt = tabulate(formattedAttackOpt)

        optionsMsg += f"\n\nOptions:\n{formattedattackopt}"

        # slurm options
        formattedSlurmOpt = [[nameOpt.upper(), *infoOpt] for nameOpt, infoOpt in self.slurm.items()]
        formattedSlurmOpt = tabulate(formattedSlurmOpt)

        optionsMsg += f"\n\nSlurm Options:\n{formattedslurmOpt}"

        return optionsMsg
