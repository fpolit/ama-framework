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

from pkg import Package


class Pdsh(Package):
    def __init__(self, *, pkgver, source):
        depends = {
            "ssh": {"Centos": "libssh.x86_64"},
        }

        makedepends = {
            "make": {"Centos": "make.x86_64"},
            "wget": {"Centos": "wget.x86_64"}
        }

        super().__init__("pdsh",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends)

    def build(self):
        print_status(f"Building {self.pkgname}-{self.pkgver}")
        print(ColorStr("It can take a while, so go for a coffee ...").StyleBRIGHT)

        #import pdb; pdb.set_trace()
        Bash.exec("./bootstrap", where=self.uncompressed_path)
        self.prefix = "/usr/local/pdsh"
        flags = [
            f"--prefix={self.prefix}",
            "--with-ssh"
        ]

        configure = "./configure " + " ".join(flags)
        Bash.exec(configure, where=self.uncompressed_path)
        Bash.exec("make", where=self.uncompressed_path)

    def install(self):
        print_status(f"Installing {self.pkgname}-{self.pkgver} in {self.prefix}")
        #import pdb; pdb.set_trace()

        Bash.exec("sudo make install", where=self.uncompressed_path)

        pdsh2path = f"""
        Now add pdsh to your PATH

        * Open ~/.bashrc and add the following

        # Adding PDSH to the PATH
        export PDSH_RCMD_TYPE=ssh
        export PDSH_HOME=/usr/local/pdsh
        export PATH=$PATH:$PDSH_HOME/bin
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PDSH_HOME/lib
        """
        print(pdsh2path)
