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
    def __init__(self, *, pkgver, source):
        depends = {
            "MPI": {}
        }

        makedepends = {
            "make": {"Centos": "make.x86_64"},
            "wget": {"Centos": "wget.x86_64"}
        }

        super().__init__("john",
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
            "--with-systemwide",
            "--with-mpi"
        ]

        configure = "./configure " + " ".join(flags)
        Bash.exec(configure, where=self.uncompressed_path)
        Bash.exec("make", where=self.uncompressed_path)

    
    def install(self):
        """
        Install the compiler source code
        """
        print_status(f"Installing {self.pkgname}-{self.pkgver}")
        #import pdb; pdb.set_trace()

        Bash.exec("sudo make install", where=self.uncompressed_path)

        # Configurations
        Bash.exec("sudo mkdir -p /usr/share/john")
        Bash.exec("sudo cp john.conf korelogic.conf hybrid.conf dumb16.conf dumb32.conf repeats32.conf repeats16.conf dynamic.conf dynamic_flat_sse_formats.conf regex_alphabets.conf password.lst ascii.chr lm_ascii.chr /usr/share/john/", where=os.path.join(self.uncompressed_path, "run"))
        Bash.exec("sudo cp -r rules /usr/share/john/", where=os.path.join(self.uncompressed_path, "run"))


def main():
    parser = Package.cmd_parser()
    parser.add_argument("--prefix", default=os.getcwd(),
                        help="Location to install john")
    args = parser.parse_args()
    john_pkg = John(
        source="https://github.com/openwall/john/archive/1.9.0-Jumbo-1.tar.gz",
        pkgver="1.9.0-jumbo"
    )
    john_pkg.prepare(compilation_path = args.compilation,
                     avoid_download = args.no_download,
                     avoid_uncompress = args.no_uncompress)
    #import pdb; pdb.set_trace()
    john_pkg.build(args.prefix)

    if args.check:
        john_pkg.check()

    john_pkg.install()

    print_successful(f"Package {john_pkg.pkgname}-{john_pkg.pkgver} was sucefully installed in {john_pkg.prefix}")
    print_status("Now add john to you PATH")


if __name__=="__main__":
    main()
