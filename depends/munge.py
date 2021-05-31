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
        configure_cmd = "./configure" + " ".join(flags)
        Bash.exece(configure_cmd)
        Bash.exec("make")

