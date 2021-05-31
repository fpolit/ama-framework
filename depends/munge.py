#!/usr/bin/env python3
#
# automatization of munge installation
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from sbash import Bash

from pkg import Package


class Munge(Package):
    def __init__(self, *, pkgver, source):
        depends = ["gcc"]
        makedepends = ["make", "wget"]
        super().__init__("munge",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends)

    def build(self):
        os.chdir(self.uncompressed_path)

        Bash.exec("./bootstrap")
        flags = [
            "--prefix=/usr",
            "--sysconfdir=/etc",
            "--localstatedir=/var"
        ]
        configure = "./configure" + " ".join(flags)
        Bash.exece(configure)
        Bash.exec("make")




def main():
    parser = Package.cmd_parser()
    args = parser.parse_args()
    munge_pkg = Munge(
        source="https://github.com/dun/munge/archive/refs/tags/munge-0.5.14.tar.gz",
        pkgver="0.5.14"
    )
    munge_pkg.prepare(uncompressed_dir = args.uncompres_dir,
                      compilation_path = args.compilation,
                      avoid_download = args.no_download)
    munge_pkg.build()

    if args.check:
        munge_pkg.check()

    munge_pkg.install()


if __name__=="__main__":
    main()
