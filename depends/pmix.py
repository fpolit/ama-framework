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
        configure_cmd = "./configure" + " ".join(flags)
        Bash.exece(configure_cmd)
        Bash.exec("make")

