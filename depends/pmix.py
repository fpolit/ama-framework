#!/usr/bin/env python3
#
# automatization of pmix installation
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from sbash import Bash

from pkg import Package


class Pmix(Package):
    def __init__(self, *, pkgver, source):
        depends = ["gcc"]
        makedepends = ["make", "wget"]
        super().__init__("pmix",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends)

    def build(self):
        os.chdir(self.uncompressed_path)

        flags = [
            "--prefix=/usr",
            "--disable-pmi-backward-compatibility",
            "--with-libevent",
            "--with-zlib",
            "--with-munge"
        ]
        configure = "./configure" + " ".join(flags)
        Bash.exece(configure)
        Bash.exec("make")



def main():
    parser = Package.cmd_parser()
    args = parser.parse_args()
    pmix_pkg = Pmix(
        source="https://github.com/openpmix/openpmix/releases/download/v3.2.3/pmix-3.2.3.tar.gz",
        pkgver="3.2.3"
    )
    pmix_pkg.prepare(uncompressed_dir = args.uncompres_dir,
                     compilation_path = args.compilation,
                     avoid_download = args.no_download)
    pmix_pkg.build()

    if args.check:
        pmix_pkg.check()

    pmix_pkg.install()


if __name__=="__main__":
    main()
