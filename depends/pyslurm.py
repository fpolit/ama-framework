#!/usr/bin/env python3
#
# automatization of pdsh installation
#
# Status: DEBUGGED - date: Jun 2 2021
#
# Warnings:
# Check output of bash process and quit execution if it fails
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import distro
import os
from sbash import Bash
from fineprint.status import print_status, print_successful, print_failure
from fineprint.color import ColorStr
from tabulate import tabulate


from pkg import Package, BuildablePackage


class PySlurm(Package):
    def __init__(self, *, pkgver, source, build_path, uncompressed_dir=None):
        depends = {}

        makedepends = {
            "make": {"Centos": "make.x86_64"},
            "wget": {"Centos": "wget.x86_64"}
        }

        super().__init__("pyslurm",
                         pkgver=pkgver,
                         source=source,
                         depends=depends,
                         makedepends=makedepends,
                         build_path=build_path,
                         uncompressed_dir=uncompressed_dir)

    def build(self):
        print_status(f"Building {self.pkgname}-{self.pkgver}")
        print(ColorStr("It can take a while, so go for a coffee ...").StyleBRIGHT)

        #import pdb; pdb.set_trace()
        Bash.exec("python3 setup.py build", where=self.uncompressed_path)

    def install(self):
        print_status(f"Installing {self.pkgname}-{self.pkgver}")
        #import pdb; pdb.set_trace()

        Bash.exec("python3 setup.py install", where=self.uncompressed_path)


if __name__ == "__main__":
    parser = Package.cmd_parser()
    args = parser.parse_args()

    build_path = os.path.abspath(os.path.expanduser(args.build_dir))

    bpkg = BuildablePackage(name='pyslurm', version='20.02.0',
                            source='https://github.com/PySlurm/pyslurm/archive/refs/tags/20-02-0.tar.gz',
                            pkg=PySlurm, build_path=build_path, uncompressed_dir='pyslurm-20-02-0')

    pretty_name_distro = distro.os_release_info()['pretty_name']
    print_status(f"Installing the following packages in {pretty_name_distro}")
    bpkg_table = [[bpkg.name, bpkg.version, bpkg.source]]
    print(tabulate(bpkg_table, headers=["Package", "Version", "Source"], tablefmt="pretty"))

    while True:
            short_answer = input("Proceed with installation? (y/n) ")
            short_answer = short_answer.lower()
            if short_answer in ['y', 'yes', 'n', 'no']:
                if short_answer in ['n', 'no']:
                    print_failure("Installation was canceled")
                    exit(1)
                else:
                    break


    PkgClass = bpkg.pkg
    pkg = PkgClass(pkgver = bpkg.version,
                   source = bpkg.source,
                   build_path = bpkg.build_path,
                   uncompressed_dir = bpkg.uncompressed_dir)

    installation_options = { # default installation options
        'no_confirm': True,
        'avoid_download': False,
        'avoid_uncompress': False,
        'avoid_check': True
    }

    if args.only_compile:
        installation_options['avoid_download'] = True
        installation_options['avoid_uncompress'] = True

    if args.avoid_download:
        installation_options['avoid_download'] = True

    if args.avoid_uncompress:
        installation_options['avoid_uncompress'] = True

    pkg.doall(**installation_options)
