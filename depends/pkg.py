#!/usr/bin/env python3
#
# General Package Class
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import argparse
import os
import sys
import zipfile
import tarfile

from fineprint.status import print_status, print_successful, print_failure
from sbash import Bash

from pkg_exceptions import UnsupportedCompression

class Package:

    """Buildable Package

    Attributes:
    pkgname (str): Package Name
    pkgver (str): Package Version
    source (str): Url to the source code of the package
    depends (list): dependences of packages in the standard repositories
    makedepends (list):  dependences of buildables packages.

    Methods:
    prepare: Download and uncompress the source code
    build: simple build for the package(use inheritance for more complex builds)
    check: simple check of the compilation status
    package: simple installation (use inheritance for more complex installations)
    """

    def __init__(self, pkgname, *, pkgver, source, depends=None, makedepends=None):
        self.pkgname=pkgname
        self.pkgver=pkgver
        self.source=source # link to the source code (compressed file)
        self.depends=depends
        self.makedepends=makedepends # these packages are needed by compilations
        self.uncompressed_path = None #path of uncompressed directory


    def depends_info(self):
        """
        Print information of dependencies and make dependencies
        """
        print_status("These packages are required to continue with the installation:")
        print_status("Dependencies:")
        for depend in self.depends:
            print(f"\t{depend}")

        print_status("Compilation dependencies (only used for compilation):")
        for depend in self.makedepends:
            print(f"\t{depend}")

        print()
        not_continue = True
        while not_continue:
            answer = input("Do you have installed all dependencies.(y/n)? ")
            answer = answer.lower()

            if answer in ["y", "yes"]:
                not_continue = False
            elif answer in ["n", "no"]:
                print_status(f"Install all the dependencies before install {self.pkgname}-{self.pkgver}")
                sys.exit(1)

    def prepare(self, *, uncompressed_dir:str =None, compilation_path=None, avoid_download=False):
        """
        Download and uncompress the source code
        """
        self.depends_info()

        if compilation_path is not None:
            self.compilation_path = os.path.abspath(compilation_path)
        else:
            self.compilation_path = os.getcwd()

        if compilation_path is not None:
            if not (os.path.exists(self.compilation_path) and os.path.isdir(self.compilation_path)):
                os.mkdir(self.compilation_path)
            os.chdir(self.compilation_path)

        if not avoid_download:
            Bash.exec(f"wget {self.source}")

        import pdb; pdb.set_trace()
        ## uncompress
        compressed_file = os.path.join(self.compilation_path, os.path.basename(self.source))

        if uncompressed_dir is not None:
            self.uncompressed_path = os.path.join(self.compilation_path, uncompressed_dir)
        else:
            self.uncompressed_path = os.path.join(self.compilation_path, f"{self.pkgname}-{self.pkgver}")
            print_status(f"Setting uncompresed_path to default value: {self.uncompressed_path}")
            print_status("\tProvide uncompresed_path argument if it's default value isn't rigth")
            print_status("\tAlso set avoid_download to True to avoid re-download the source code")

        if zipfile.is_zipfile(compressed_file): # source was compressed using zip
            with zipfile.ZipFile(compressed_file, 'r') as zip_compressed_file:
                zip_compressed_file.extractall()

        elif tarfile.is_tarfile(compressed_file): # source was compressed using tar
            with tarfile.open(compressed_file, 'r') as tar_compressed_file:
                tar_compressed_file.extractall()
        else:
            raise UnsupportedCompression(["zip", "tar"])

        print_successful(f"Package {self.pkgname}-{self.pkgver} was prepared")

    def build(self): # simple build(use inheritance for more complex builds)
        """
        Build the souce code
        """
        os.chdir(self.uncompressed_path)
        Bash.exec("./configure")
        Bash.exec("make")


    def check(self):
        """
        Check the status of the compiled source
        """
        os.chdir(self.uncompressed_path)
        Bash.exec("make check")


    def install(self): # simple installation(use inheritance for more complex installations)
        """
        Install the compiler source code
        """
        os.chdir(self.uncompressed_path)
        Bash.exec("sudo make install")


    def doall(self, avoid_check=False):
        """
        Install the buildable package(build, check, and install)
        """
        self.prepare()
        self.build()

        if not avoid_check:
            self.check()

        self.install()
        print_successful(f"Sucefully installation of {self.pkgname}-{self.pkgver}")

    @staticmethod
    def cmd_parser():
        pkg_parser = argparse.ArgumentParser(f"Automatization script")
        pkg_parser.add_argument("-u", "--uncompress_dir", type=str,
                                help="Name of uncompress directory")
        pkg_parser.add_argument("-c", "--compilation", type=str,
                                help="Build directory path ")
        pkg_parser.add_argument("-d", "--no_download", action='store_true',
                                help="Avoid download package")
        pkg_parser.add_argument("--check", action='store_true',
                                help="Perform check of compilation")

        return pkg_parser


    def __repr__(self):
        return f"Package(name={self.pkgname}, version={self.pkgver})"
