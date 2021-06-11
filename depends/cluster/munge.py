#!/usr/bin/env python3
#
# automatization of munge installation
#
# Status: DEBUGGED - date May 31 2021
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


class Munge(Package):
    def __init__(self, *, pkgver, source):
        depends = {
            "gcc": {"Centos": "gcc.x86_64"},
            "OpenSSL": {"Centos": "openssl-devel.x86_64"},
            "libevent": {"Centos": "libevent-devel.x86_64"},
            "zlib": {"Centos": "zlib-devel.x86_64"}
        }

        makedepends = {
            "make": {"Centos": "make.x86_64"},
            "wget": {"Centos": "wget.x86_64"}
        }

        super().__init__("munge",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends)

    def build(self):
        print_status(f"Building {self.pkgname}-{self.pkgver}")
        print(ColorStr("It can take a while, so go for a coffee ...").StyleBRIGHT)

        Bash.exec("./bootstrap", where=self.uncompressed_path)
        flags = [
            "--prefix=/usr",
            "--sysconfdir=/etc",
            "--localstatedir=/var",
            "--libdir=/usr/lib64"
        ]

        configure = "./configure " + " ".join(flags)
        Bash.exec(configure, where=self.uncompressed_path)
        Bash.exec("make", where=self.uncompressed_path)

    def install(self):
        print_status(f"Installing {self.pkgname}-{self.pkgver}")
        #import pdb; pdb.set_trace()

        Bash.exec("sudo make install", where=self.uncompressed_path)

        print_status(f"Configuring {self.pkgname}-{self.pkgver} package")
        configure = [
            "sudo useradd -s /bin/bash -d /var/log/munge munge",
            "sudo chown munge:munge -R /var/log/munge/",

            "sudo chown munge:munge /etc/munge/",
            "sudo chmod 700 /etc/munge/",

            "sudo chown munge:munge /var/lib/munge/",
            "sudo chmod 711 /var/lib/munge/",

            "sudo chmod 700 /var/log/munge"
        ]

        for cmd in configure:
            Bash.exec(cmd)




def main():
    parser = Package.cmd_parser()
    args = parser.parse_args()
    munge_pkg = Munge(
        source="https://github.com/dun/munge/archive/refs/tags/munge-0.5.14.tar.gz",
        pkgver="0.5.14"
    )
    munge_pkg.prepare(compilation_path = args.compilation,
                      avoid_download = args.no_download,
                      avoid_uncompress = args.no_uncompress)
    #import pdb; pdb.set_trace()
    munge_pkg.build()

    if args.check:
        munge_pkg.check()

    munge_pkg.install()

    print_successful(f"Package {munge_pkg.pkgname}-{munge_pkg.pkgver} was sucefully installed")
    print_status("Now create munge key in /etc/munge using mungekey.Then initialize munge service")


if __name__=="__main__":
    main()