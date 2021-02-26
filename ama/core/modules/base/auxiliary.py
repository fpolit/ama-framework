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
            """

        for author in self.author:
            infoMsg += f"{author}\n"

        infoMsg += self.optionsMsg()

        # description module
        infoMsg += f"\n\n Description:\n{self.fulldescription}"

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

        # auxiliary options
        formattedOpt = [[name.upper(), *option.getAttributes()]
                              for name, option in self.auxiliary.items()]
        formattedOpt = tabulate(formattedOpt, headers=optionHeader)

        optionsMsg += f"\n\nOptions:\n{formattedOpt}"

        # slurm options
        slurmOptions = self.slurm.options()
        formattedSlurmOpt = [[name.upper(), *option.getAttributes()]
                             for name, option in slurmOptions.items()]
        formattedSlurmOpt = tabulate(formattedSlurmOpt, headers=optionHeader)

        optionsMsg += f"\n\nSlurm Options:\n{formattedSlurmOpt}"

        return optionsMsg



    def isVariable(self, variable):
        if variable in self.auxiliary or \
           variable in self.slurm.options():
            return True
        else:
            return False

    def isAuxiliaryVariable(self, variable):
        if variable in self.auxiliary:
            return True
        else:
            return False

    def isSlurmVariable(self, variable):
        if variable in self.slurm.options():
            return True
        else:
            return False
