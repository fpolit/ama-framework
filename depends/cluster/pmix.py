#!/usr/bin/env python3
#
# automatization of pmix installation
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


class Pmix(Package):
    def __init__(self, *, pkgver, source):
        depends = {
            "gcc": {"Centos": "gcc.x86_64"},
            "libevent": {"Centos": "libevent-devel.x86_64"},
            "zlib": {"CentOS": "zlib-devel.x86_64 "},
            "munge": {"Linux": "https://github.com/fpolit/ama-framework/blob/master/depends/cluster/munge.py"},
        }

        makedepends = {
            "make": {"Centos": "make.x86_64"},
            "wget": {"Centos": "wget.x86_64"}
        }

        super().__init__("pmix",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends)

    def build(self):
        print_status(f"Building {self.pkgname}-{self.pkgver}")
        print(ColorStr("It can take a while, so go for a coffee ...").StyleBRIGHT)

        Bash.exec("./autogen.pl", where=self.uncompressed_path)
        flags = [
            "--prefix=/usr",
            "--with-libevent",
            "--with-zlib",
            "--with-munge"
        ]

        configure = "./configure " + " ".join(flags)
        Bash.exec(configure, where=self.uncompressed_path)
        Bash.exec("make", where=self.uncompressed_path)
 

def main():
    parser = Package.cmd_parser()
    args = parser.parse_args()
    pmix_pkg = Pmix(
        source="https://github.com/openpmix/openpmix/releases/download/v3.2.3/pmix-3.2.3.tar.gz",
        pkgver="3.2.3"
    )
    pmix_pkg.prepare(compilation_path = args.compilation,
                      avoid_download = args.no_download,
                      avoid_uncompress = args.no_uncompress)
    #import pdb; pdb.set_trace()
    pmix_pkg.build()

    if args.check:
        pmix_pkg.check()

    pmix_pkg.install()

    print_successful(f"Package {pmix_pkg.pkgname}-{pmix_pkg.pkgver} was sucefully installed")


if __name__=="__main__":
    main()
