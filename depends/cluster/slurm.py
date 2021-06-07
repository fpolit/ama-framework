#!/usr/bin/env python3
#
# automatization of slurm installation
#
# Status: DEBUGGED - date: Jun 2 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from sbash import Bash
from fineprint.status import print_status, print_successful
from fineprint.color import ColorStr

from pkg import Package


class Slurm(Package):
    def __init__(self, *, pkgver, source):
        depends = {
            "gcc": {"CentOS": "gcc.x86_64"},
            "pmix": {"CentOS": "pmix.x86_64"},
            "gtk2": {"CentOS": "gtk2-devel.x86_64"},
            "pam": {"CentOS": "pam-devel.x86_64"}
            }

        makedepends = {
            "make": {"CentOS": "make.x86_64"},
            "wget": {"CentOS": "wget.x86_64"}
        }

        super().__init__("slurm",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends)

    def build(self):
        print_status(f"Building {self.pkgname}-{self.pkgver}")
        print(ColorStr("It can take a while, so go for a coffee ...").StyleBRIGHT)

        Bash.exec("autoreconf", where=self.uncompressed_path)
        flags = [
            "--disable-developer",
            "--disable-debug",
            "--enable-optimizations",
            "--prefix=/usr",
            "--sbindir=/usr/bin",
            "--sysconfdir=/etc/slurm-llnl",
            "--localstatedir=/var",
            "--enable-pam",
            "--with-pmix=/usr",
            "--with-munge"
        ]
        #import pdb; pdb.set_trace()
        configure = "./configure " + " ".join(flags)
        Bash.exec(configure, where=self.uncompressed_path)
        Bash.exec("make", where=self.uncompressed_path)

    def install(self):
        print_status(f"Installing {self.pkgname}-{self.pkgver}")
        Bash.exec("sudo make install", where=self.uncompressed_path)

        print_status(f"Configuring {self.pkgname}-{self.pkgver} package")

        configrations = [
            'sudo install -D -m644 etc/slurm.conf.example    "/etc/slurm-llnl/slurm.conf.example"',
            'sudo install -D -m644 etc/slurmdbd.conf.example "/etc/slurm-llnl/slurmdbd.conf.example"',
            'sudo install -D -m644 LICENSE.OpenSSL           "/usr/share/licenses/slurm/LICENSE.OpenSSL"',
            'sudo install -D -m644 COPYING           "/usr/share/licenses/slurm/COPYING"',
            'sudo install -D -m755 etc/init.d.slurm      "/etc/rc.d/slurm"',
            'sudo install -D -m755 etc/init.d.slurmdbd   "/etc/rc.d/slurmdbd"',
            'sudo install -D -m644 etc/slurmctld.service "/usr/lib/systemd/system/slurmctld.service"',
            'sudo install -D -m644 etc/slurmd.service    "/usr/lib/systemd/system/slurmd.service"',
            'sudo install -D -m644 etc/slurmdbd.service  "/usr/lib/systemd/system/slurmdbd.service"',
            'sudo install -d -m755 "/var/log/slurm-llnl"',
            'sudo install -d -m755 "/var/lib/slurm-llnl"', 
            'sudo useradd -r -c "slurm daemon" -u 64030 -s /bin/nologin -d /var/log/slurm-llnl slurm',
            'sudo install -d -m700 "/var/spool/slurm/d"',
            'sudo install -d -m700 -o slurm -g slurm "/var/spool/slurm/ctld"'
        ]

        for cmd in configrations:
            Bash.exec(cmd, where=self.uncompressed_path)


def main():
    parser = Package.cmd_parser()
    args = parser.parse_args()
    slurm_pkg = Slurm(
        source="https://download.schedmd.com/slurm/slurm-20.11.7.tar.bz2",
        pkgver="20.11.7"
    )
    slurm_pkg.prepare(compilation_path = args.compilation,
                      avoid_download = args.no_download,
                      avoid_uncompress = args.no_uncompress)

    slurm_pkg.build()

    if args.check:
        slurm_pkg.check()

    slurm_pkg.install()
    print_successful(f"Package {slurm_pkg.pkgname}-{slurm_pkg.pkgver} was sucefully installed")


if __name__=="__main__":
    main()
