#!/usr/bin/env python3
#
# automatization of john installation with MPI support
#
# Status:
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


class John(Package):
    def __init__(self, *, pkgver, source, build_path, uncompressed_dir=None):
        depends = {
            "MPI": {"Linux": "https://github.com/fpolit/ama-framework/blob/master/depends/cluster/openmpi.py"},
            "OpenSSL": {"Centos": "openssl-devel.x86_64"}
        }

        makedepends = {
            "make": {"Centos": "make.x86_64"},
            "wget": {"Centos": "wget.x86_64"}
        }

        super().__init__("john",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends,
                         build_path=build_path,
                         uncompressed_dir=uncompressed_dir)

    def set_prefix(self, prefix):
        self.build_path = os.path.abspath(os.path.expanduser(prefix))
        self.uncompressed_path = os.path.join(prefix, self.uncompressed_dir)

    def build(self):
        print_status(f"Building {self.pkgname}-{self.pkgver}")
        print(ColorStr("It can take a while, so go for a coffee ...").StyleBRIGHT)

        flags = [
            "--with-systemwide",
            "--enable-mpi"
        ]

        configure = "./configure " + " ".join(flags)
        Bash.exec(configure, where=os.path.join(self.uncompressed_path, "src"))
        Bash.exec("make", where=os.path.join(self.uncompressed_path, "src"))

    def install(self):
        """
        Install the compiler source code
        """
        print_status(f"Installing {self.pkgname}-{self.pkgver}")
        #import pdb; pdb.set_trace()

        Bash.exec("sudo make install", where=os.path.join(self.uncompressed_path, "src"))

        # Configurations
        Bash.exec("sudo mkdir -p /usr/share/john")
        Bash.exec("sudo cp john.conf korelogic.conf hybrid.conf dumb16.conf dumb32.conf repeats32.conf repeats16.conf dynamic.conf dynamic_flat_sse_formats.conf regex_alphabets.conf password.lst ascii.chr lm_ascii.chr /usr/share/john/", where=os.path.join(self.uncompressed_path, "run"))
        Bash.exec("sudo cp -r rules /usr/share/john/", where=os.path.join(self.uncompressed_path, "run"))


        print_status("Adding john to you PATH")
        john2path = f"""
### exporting john to the PATH
export JOHN_HOME={self.uncompressed_path}
export PATH=$PATH:$JOHN_HOME/run
        """

        with open(os.path.expanduser("~/.bashrc"), 'a') as bashrc:
            bashrc.write(john2path)

        # exporting John to the PATH
        john_bin = os.path.join(self.uncompressed_path, "run")
        os.environ['PATH'] += f":{john_bin}"
