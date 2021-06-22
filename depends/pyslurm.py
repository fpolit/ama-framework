#!/usr/bin/env python3
#
# automatization of pdsh installation
#
# Status: DEBUGGED - date: Jun 2 2021
#
# Warnings:
# Check output of bash process and quit execution if it fails
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from sbash import Bash
from fineprint.status import print_status, print_successful
from fineprint.color import ColorStr

from .pkg import Package


class PySlurm(Package):
    def __init__(self, *, pkgver, source):
        depends = {}

        makedepends = {
            "make": {"Centos": "make.x86_64"},
            "wget": {"Centos": "wget.x86_64"}
        }

        super().__init__("pyslurm",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends)

    def build(self):
        print_status(f"Building {self.pkgname}-{self.pkgver}")
        print(ColorStr("It can take a while, so go for a coffee ...").StyleBRIGHT)

        #import pdb; pdb.set_trace()
        Bash.exec("python3 setup.py build", where=self.uncompressed_path)

    def install(self):
        print_status(f"Installing {self.pkgname}-{self.pkgver} in {self.prefix}")
        #import pdb; pdb.set_trace()

        Bash.exec("python3 setup.py install", where=self.uncompressed_path)
