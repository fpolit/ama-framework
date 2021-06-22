#!/usr/bin/env  python3
#
# This script was written to automate installation of ama dependencies.
# Dependencies:
#       John with MPI support (it depends of openmpi, which depends of pmix)
#       Slurm with Pmix support (it depends of munge and pmix)
#
# Status: DEBUGGED - date: Jun 18 2021
#    Tested OS: Centos 8
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import argparse
from collections import namedtuple
import distro
from fineprint.status import print_failure, print_status, print_successful
from fineprint.color import ColorStr
import platform
from tabulate import tabulate
import os

# script of depends/cluster
from depends import (
    Munge,
    Pmix,
    Slurm,
    PySlurm,
    OpenMPI,
    John,
    install_requirements
)

BuildablePackage = namedtuple('BuildablePackage', ['name', 'version', 'source',
                                                   'pkg', 'build_path', 'uncompressed_dir'])
pkgs_names = ['munge', 'pmix', 'slurm', 'pyslurm', 'openmpi', 'john']
tested_linux_distros = ['ubuntu', 'kali', 'arch', 'centos']

def install_args():
    parser = argparse.ArgumentParser(description="Script to automate installation of dependencies")

    parser.add_argument('-b','--build-dir', dest='build_dir', required=True,
                        help="Directory where packages will be downloaded, uncompressed and compiled")

    prefix_parser = parser.add_argument_group("Location to install dependencies")
    prefix_parser.add_argument("--openmpi-prefix", dest="openmpi_prefix", default="/usr/local/openmpi", metavar='/usr/local/openmpi',
                               help="Location to install OpenMPI")
    prefix_parser.add_argument("--john-prefix", dest="john_prefix", default='~/tools', metavar='~/tools',
                               help="Location to install John")


    installation_parser = parser.add_argument_group("Customized Installation")
    installation_parser.add_argument("--no-ospkgs", dest='no_ospkgs', action='store_true',
                                help="Do not install OS dependecy packages")
    installation_parser.add_argument("--only-compile", dest='only_compile', nargs='*',
                                     choices=pkgs_names,
                                     default=[],
                                     help="Do not donwload and uncompress, simply compile packages")
    installation_parser.add_argument("--avoid-download", dest='avoid_download', nargs='*',
                                     choices=pkgs_names,
                                     default=[],
                                     help="Do not download package")
    installation_parser.add_argument("--avoid-uncompress", dest='avoid_uncompress', nargs='*',
                                     choices=pkgs_names,
                                     default=[],
                                     help="Do not uncompress package")
    installation_parser.add_argument("--disable", nargs='*',
                                     choices=pkgs_names,
                                     default=[],
                                     help="Do not install selected packages (USE WITH CAUTION)")



    depends_parser = parser.add_argument_group("Optional Features")
    depends_parser.add_argument("--enable-slurm", dest='enable_slurm', action='store_true',
                                help="Install Slurm to perform distributed attacks")

    return parser.parse_args()


def check_distro():
    """
    Check if the OS is Linux and validate if the distributions is one which ama was tested
    """

    os_name = platform.system()
    if os_name != "Linux":
        raise Exception(f"Sorry but currently ama isn't supported by {os_name} OS")

    distro_id = distro.id()
    if distro_id not in tested_linux_distros:
        print_failure(f"Ama-Framework wasn't tested in {distro_id} GNU/Linux distributions.")
        print_status("Supported GNU/Linux distros: {' '.join(tested_linux_distros)}")
        while True:
            short_answer = input("Do you want to continue(y/n)? ")
            short_answer = short_answer.lower()
            if short_answer in ['y', 'yes', 'n', 'no']:
                if short_answer in ['n', 'no']:
                    raise Exception("Installation was canceled")
                else:
                    break

    return distro_id

def install():
    try:
        distro_id = check_distro()
        args = install_args()

        build_path = os.path.abspath(os.path.expanduser(args.build_dir))

        packages = []
        if "munge" not in args.disable:
            packages += [
                BuildablePackage(name='munge', version='0.5.14',
                                 source='https://github.com/dun/munge/archive/refs/tags/munge-0.5.14.tar.gz',
                                 pkg=Munge, build_path=build_path, uncompressed_dir='munge-munge-0.5.14')
            ]

        if "pmix" not in args.disable:
            packages += [
                BuildablePackage(name='pmix', version='3.2.3',
                                 source='https://github.com/openpmix/openpmix/releases/download/v3.2.3/pmix-3.2.3.tar.gz',
                                 pkg=Pmix, build_path=build_path, uncompressed_dir='pmix-3.2.3')
            ]

        if args.enable_slurm and not ("slurm" in args.disable):
            packages += [
                BuildablePackage(name='slurm', version='20.02.7',
                                 source='https://download.schedmd.com/slurm/slurm-20.02.7.tar.bz2',
                                 pkg=Slurm, build_path=build_path, uncompressed_dir='slurm-20.02.7'),
                BuildablePackage(name='pyslurm', version='20.02.0',
                                 source='https://github.com/PySlurm/pyslurm/archive/refs/tags/20-02-0.tar.gz',
                                 pkg=PySlurm, build_path=build_path, uncompressed_dir='pyslurm-20-02-0')
            ]

        if "openmpi" not in args.disable:
            packages += [
                BuildablePackage(name='openmpi', version='4.1.1',
                                 source='https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.1.tar.gz',
                                 pkg=OpenMPI, build_path=build_path, uncompressed_dir='openmpi-4.1.1')
            ]
        if "john" not in args.disable:
            packages += [
                BuildablePackage(name='john', version='1.9.0-Jumbo-1',
                                 source='https://github.com/openwall/john/archive/1.9.0-Jumbo-1.tar.gz',
                                 pkg=John, build_path=args.john_prefix, uncompressed_dir='john-1.9.0-Jumbo-1')
        ]

        pretty_name_distro = distro.os_release_info()['pretty_name']
        print_status(f"Installing the following packages in {pretty_name_distro}")
        bpkg_table = [[bpkg.name, bpkg.version, bpkg.source] for bpkg in packages]
        print(tabulate(bpkg_table, headers=["Package", "Version", "Source"], tablefmt="pretty"))

        while True:
            short_answer = input("Proceed with installation? (y/n) ")
            short_answer = short_answer.lower()
            if short_answer in ['y', 'yes', 'n', 'no']:
                if short_answer in ['n', 'no']:
                    raise Exception("Installation was canceled")
                else:
                    break

        if not args.no_ospkgs:
            install_requirements(distro_id)
        #import pdb; pdb.set_trace()

        for bpkg in packages:
            if distro_id == "arch":
                if bpkg.name == "john":
                    print_status(f"Install john using {ColorStr('john-git')} AUR package")
                    print_failure(f"{ColorStr('john-git')} AUR package is compiled using default {ColorStr('openmpi')} package (it hasn't slurm and pmix support)")
                    continue

                # elif bpkg.name == "slurm":
                #     print_status(f"Install slurm using {ColorStr('slurm-llnl')} AUR package")
                #     continue

            print_status(f"Installing {bpkg.name}-{bpkg.version}")
            PkgClass = bpkg.pkg
            pkg = PkgClass(pkgver = bpkg.version,
                           source = bpkg.source,
                           build_path = bpkg.build_path,
                           uncompressed_dir = bpkg.uncompressed_dir)

            if bpkg.name in ["openmpi", "john"]:
                if bpkg.name == "john":
                    prefix = args.john_prefix
                elif bpkg.name == "openmpi":
                    prefix = args.openmpi_prefix

                pkg.set_prefix(prefix)

            installation_options = { # default installation options
                'no_confirm': True,
                'avoid_download': False,
                'avoid_uncompress': False,
                'avoid_check': True
            }

            if pkg.pkgname in args.only_compile:
                installation_options['avoid_download'] = True
                installation_options['avoid_uncompress'] = True

            if pkg.pkgname in args.avoid_download:
                installation_options['avoid_download'] = True

            if pkg.pkgname in args.avoid_uncompress:
                installation_options['avoid_uncompress'] = True

            print_status("Installation options:")
            for option, value in installation_options.items():
                print(f"\t{option}: {value}")

            #import pdb; pdb.set_trace()

            pkg.doall(**installation_options)


    except Exception as error:
        print_failure(error)


if __name__ == "__main__":
    install()
