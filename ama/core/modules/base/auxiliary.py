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


class Auxiliary:
    """
    Base class to build cracker modules
    """
    def __init__(self, +,
                 name: str, mtype: str, msubtype: str, author: List[str],
                 description: str, importPath: str, slurm, *args, *kwargs):

        self.name = name
        self.mtype = mtype
        self.msubtype = msubtype
        self.author = author
        self.description = description
        self.importPath = importPath
        self.slurm = slurm


    def attack(self, *args, **kwargs):
        """
        Attack performed by cracker
        """
        pass
