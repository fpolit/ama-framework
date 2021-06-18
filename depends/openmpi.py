#!/usr/bin/env python3
#
# automatization of openmpi installation with pmix ans slurm support
#
# Status: DEBUGGED - date: Jun 3 2021
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


class OpenMPI(Package):
    def __init__(self, *, pkgver, source, build_path, uncompressed_dir=None):
        depends = {
            "gcc": {"Centos": "gcc.x86_64"},
            "pmix": {"CentOS": "https://github.com/fpolit/ama-framework/blob/master/depends/cluster/pmix.py"}
        }

        makedepends = {
            "make": {"Centos": "make.x86_64"},
            "wget": {"Centos": "wget.x86_64"}
        }
        self.prefix = "/usr/local/openmpi" # default prefix
        super().__init__("openmpi",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends,
                         build_path = build_path,
                         uncompressed_dir= uncompressed_dir)

    def set_prefix(self, prefix):
        self.prefix = os.path.abspath(os.path.expanduser(prefix))

    def build(self):
        print_status(f"Building {self.pkgname}-{self.pkgver}")
        print(ColorStr("It can take a while, so go for a coffee ...").StyleBRIGHT)

        flags = [
            f"--prefix={prefix}",
            "--with-pmix=/usr",
            "--with-pmi",
            "--with-slurm"
        ]

        configure = "./configure " + " ".join(flags)
        Bash.exec(configure, where=self.uncompressed_path)
        Bash.exec("make", where=self.uncompressed_path)

    def install(self):
        super().install()
        print_successful(f"Package {openmpi_pkg.pkgname}-{openmpi_pkg.pkgver} was sucefully installed in {openmpi_pkg.prefix}")
        print_status("Now add openmpi to you PATH")

        openmpi2path = f"""
        * Open ~/.bashrc and add the following

        ### exporting openmpi to the PATH
        export OPENMPI_HOME={openmpi_pkg.prefix}
        export PATH=$PATH:$OPENMPI_HOME/bin
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$OPENMPI_HOME/lib
        """

        print(openmpi2path)
