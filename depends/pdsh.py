#!/usr/bin/env python3
#
# automatization of pdsh installation
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
        print(ColorStr("It can take a while, so go for a cafe ...").StyleBRIGHT)

        Bash.exec("./bootstrap", where=self.uncompressed_path)
        flags = [
            "--prefix=/usr/local/pdsh",
            "--with-ssh"
        ]

        configure = "./configure " + " ".join(flags)
        Bash.exec(configure, where=self.uncompressed_path)
        Bash.exec("make", where=self.uncompressed_path)

    def install(self):
        print_status(f"Installing {self.pkgname}-{self.pkgver}")
        #import pdb; pdb.set_trace()

        Bash.exec("sudo make install", where=self.uncompressed_path) 


def main():
    parser = Package.cmd_parser()
    args = parser.parse_args()
    pdsh_pkg = Pdsh(
        source="https://github.com/chaos/pdsh/releases/download/pdsh-2.32/pdsh-2.32.tar.gz",
        pkgver="2.32"
    )
    pdsh_pkg.prepare(compilation_path = args.compilation,
                      avoid_download = args.no_download,
                      avoid_uncompress = args.no_uncompress)
    #import pdb; pdb.set_trace()
    pdsh_pkg.build()

    if args.check:
        pdsh_pkg.check()

    pdsh_pkg.install()

    print_successful(f"Package {munge_pkg.pkgname}-{munge_pkg.pkgver} was sucefully installed")
    print_status("Now add pdsh to your PATH")


if __name__=="__main__":
    main()
