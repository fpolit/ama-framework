#!/usr/bin/env python3
#
# automatization of openmpi installation with pmix ans slurm support
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


class Openmpi(Package):
    def __init__(self, *, pkgver, source):
        depends = {
            "gcc": {"Centos": "gcc.x86_64"},
            "pmix": {"CentOS": "pmix.x86_64"}
        }

        makedepends = {
            "make": {"Centos": "make.x86_64"},
            "wget": {"Centos": "wget.x86_64"}
        }

        super().__init__("openmpi",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends)

    def build(self, prefix):
        self.prefix = prefix
        print_status(f"Building {self.pkgname}-{self.pkgver}")
        print(ColorStr("It can take a while, so go for a coffee ...").StyleBRIGHT)

        flags = [
            f"--prefix={prefix}",
            "--with-pmix=/usr/lib64/pmix",
            "--with-slurm"
        ]

        configure = "./configure " + " ".join(flags)
        Bash.exec(configure, where=self.uncompressed_path)
        Bash.exec("make", where=self.uncompressed_path)


def main():
    parser = Package.cmd_parser()
    parser.add_argument("--prefix", default="/usr/local/openmpi",
                        help="Location to install openmpi")
    args = parser.parse_args()
    openmpi_pkg = Openmpi(
        source="https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.1.tar.gz",
        pkgver="4.1.1"
    )
    openmpi_pkg.prepare(compilation_path = args.compilation,
                        avoid_download = args.no_download,
                        avoid_uncompress = args.no_uncompress)
    #import pdb; pdb.set_trace()
    openmpi_pkg.build(args.prefix)

    if args.check:
        openmpi_pkg.check()

    openmpi_pkg.install()

    print_successful(f"Package {openmpi_pkg.pkgname}-{openmpi_pkg.pkgver} was sucefully installed in {openmpi.prefix}")
    print_status("Now add openmpi to you PATH")


if __name__=="__main__":
    main()
