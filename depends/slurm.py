#!/usr/bin/env python3
#
# automatization of slurm installation
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from sbash import Bash

from pkg import Package


class Slurm(Package):
    def __init__(self, *, pkgver, source):
        depends = ["gcc", "pmix", "munge"]
        makedepends = ["make", "wget"]
        super().__init__("slurm",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends)

    def build(self):
        os.chdir(self.uncompressed_path)

        Bash.exec("autoreconf")
        flags = [
            "--disable-developer",
            "--disable-debug",
            "--enable-optimizations",
            "--prefix=/usr",
            "--sbindir=/usr/bin",
            "--sysconfdir=/etc/slurm-llnl",
            "--localstatedir=/var",
            "--enable-pam",
            "--with-pmix",
            "--with-munge"
        ]
        configure = "./configure" + " ".join(flags)
        Bash.exec(configure)
        Bash.exec("make")

    def install(self):
        os.chdir(self.uncompressed_path)
        Bash.exec("sudo make install")

        configrations = [
            'sudo install -D -m644 etc/slurm.conf.example    "/etc/slurm-llnl/slurm.conf.example"',
            'sudo install -D -m644 etc/slurmdbd.conf.example "/etc/slurm-llnl/slurmdbd.conf.example"',
            'sudo install -D -m644 LICENSE.OpenSSL           "/usr/share/licenses/slurm/LICENSE.OpenSSL"',
            'sudo install -D -m644 COPYING           "/usr/share/licenses/slurm/COPYING"',
            'sudo install -D -m755 etc/init.d.slurm      "/etc/rc.d/slurm"',
            'sudo install -D -m755 etc/init.d.slurmdbd   "/etc/rc.d/slurmdbd"',
            'sudo install -D -m644 etc/slurmctld.service "/usr/lib/systemd/system/slurmctld.service"',
            'sudo install -D -m644 etc/slurmd.service    "/usr/lib/systemd/system/slurmd.service"',
            'sudo install -D -m644 etc/slurmdbd.service  "/usr/lib/systemd/system/slurmdbd.service"'
            'sudo install -d -m755 "/var/log/slurm-llnl"'
            'sudo install -d -m755 "/var/lib/slurm-llnl"'
        ]

        for cmd in configrations:
            Bash.exec(cmd)


def main():
    parser = Package.cmd_parser()
    args = parser.parse_args()
    slurm_pkg = Slurm(
        source="https://download.schedmd.com/slurm/slurm-20.11.7.tar.bz2",
        pkgver="20.11.7"
    )
    slurm_pkg.prepare(uncompressed_dir = args.uncompres_dir,
                      compilation_path = args.compilation,
                      avoid_download = args.no_download)
    slurm_pkg.build()

    if args.check:
        slurm_pkg.check()

    slurm_pkg.install()


if __name__=="__main__":
    main()
