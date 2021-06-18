#!/usr/bin/env  python3
#
# This script was written to automate installation of ama dependencies.
# Dependencies:
#       John with MPI support (it depends of openmpi, which depends of pmix)
#       Slurm with Pmix support (it depends of munge and pmix)
#
# Status:
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
    OpenMPI,
    John,
    install_requirements
)

BuildablePackage = namedtuple('BuildablePackage', ['name', 'version', 'source', 'pkg', 'build_path', 'uncompressed_dir'])

tested_linux_distros = ['ubuntu', 'kali', 'arch', 'centos']

def install_args():
    parser = argparse.ArgumentParser(description="Install ama's dependencies")

    parser.add_argument('-b','--build-dir', dest='build_dir', required=True,
                        help="Directory where packages will be downloaded, uncompressed and compiled")

    # python_parser = parser.add_argument_group("Python enviroment")
    # python_parser.add_argument('--pyenv', default = None,
    #                            help="Python enviroment to install python requirements")
    # python_parser.add_argument('--create-pyenv', action="store_true", dest='create_pyenv',
    #                            help="Create a python enviroment if supplied enviroment doesn't exist")
    # python_parser.add_argument('--pyenv-prompt', dest='pyenv_prompt', default='ama',
    #                            help="Python enviroment name")

    prefix_parser = parser.add_argument_group("Location to install dependencies")
    prefix_parser.add_argument("--openmpi-prefix", dest="openmpi_prefix", default="/usr/local/openmpi",
                               help="Location to install OpenMPI")
    prefix_parser.add_argument("--john-prefix", dest="john_prefix", required=True,
                               help="Location to install John")

    depends_parser = parser.add_argument_group("Optional dependencies")
    depends_parser.add_argument("--enable-slurm", dest='enable_slurm', action='store_true',
                                help="Install Slurm to perform distributed attacks")

    return parser.parse_args()


def check_distro():
    """
    Check if the OS is Linux and validate if the distributions is one which ama was tested
    """

    os_name = platform.system()
    if os_name != "Linux":
        raise Exception(f"Sorry but actually ama isn't supported by {os_name} OS")

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

        packages = [
            BuildablePackage(name='munge', version='0.5.14',
                             source='https://github.com/dun/munge/archive/refs/tags/munge-0.5.14.tar.gz',
                             pkg=Munge, build_path=build_path, uncompressed_dir='munge-munge-0.5.14'),
            BuildablePackage(name='pmix', version='3.2.3',
                             source='https://github.com/openpmix/openpmix/releases/download/v3.2.3/pmix-3.2.3.tar.gz',
                             pkg=Pmix, build_path=build_path, uncompressed_dir='pmix-3.2.3'),
        ]

        if args.enable_slurm:
            packages.append(BuildablePackage(name='slurm', version='20.11.7',
                                             source='https://download.schedmd.com/slurm/slurm-20.11.7.tar.bz2',
                                             pkg=Slurm, build_path=build_path, uncompressed_dir='slurm-20.11.7'))

        packages += [
            BuildablePackage(name='openmpi', version='4.1.1',
                             source='https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.1.tar.gz',
                             pkg=OpenMPI, build_path=build_path, uncompressed_dir='openmpi-4.1.1'),
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

        install_requirements(distro_id)
        #import pdb; pdb.set_trace()

        for bpkg in packages:
            if distro_id == "arch":
                if bpkg.name == "john":
                    print_status(f"Install john using {ColorStr('john-git')} AUR package")
                    print_failure(f"{ColorStr('john-git')} AUR package is compiler using default {ColorStr('openmpi')} package (without slurm and pmix support)")
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

            pkg.doall(no_confirm=True)


    except Exception as error:
        print_failure(error)


if __name__ == "__main__":
    install()
