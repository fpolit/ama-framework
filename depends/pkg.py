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
from fineprint.color import ColorStr
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
        for name, pkg_linux in self.depends.items():
            print(f"\t{name}:")
            for os, pkg in pkg_linux.items():
                print(f"\t\t{os}: {pkg}")

        print_status("Compilation dependencies (only used for compilation):")
        for name, pkg_linux in self.makedepends.items():
            print(f"\t{name}:")
            for os, pkg in pkg_linux.items():
                print(f"\t\t{os}: {pkg}")

        print()
        not_continue = True
        while not_continue:
            answer = input("Do you have installed all dependencies(y/n)? ")
            answer = answer.lower()

            if answer in ["y", "yes"]:
                not_continue = False
            elif answer in ["n", "no"]:
                print_status(f"Install all the dependencies before install {self.pkgname}-{self.pkgver}")
                sys.exit(1)

    def prepare(self, *, compilation_path=None, avoid_download=False, avoid_uncompress=False):
        """
        Download and uncompress the source code
        """
        #import pdb; pdb.set_trace()
        self.depends_info()

        if compilation_path is not None:
            self.compilation_path = os.path.abspath(compilation_path)
            if not (os.path.exists(compilation_path) and os.path.isdir(compilation_path)):
                os.mkdir(compilation_path)
        else:
            self.compilation_path = os.getcwd()

        if not avoid_download:
            print_status(f"Downloading {os.path.basename(self.source)}")
            Bash.exec(f"wget {self.source}", where=self.compilation_path)

        ## uncompress
        compressed_file = os.path.join(self.compilation_path, os.path.basename(self.source))

        if not avoid_uncompress:
            print_status(f"Uncompressing {compressed_file}")
            if zipfile.is_zipfile(compressed_file): # source was compressed using zip
                with zipfile.ZipFile(compressed_file, 'r') as zip_compressed_file:
                    zip_compressed_file.extractall(self.compilation_path)

            elif tarfile.is_tarfile(compressed_file): # source was compressed using tar
                with tarfile.open(compressed_file, 'r') as tar_compressed_file:
                    tar_compressed_file.extractall(self.compilation_path)
            else:
                raise UnsupportedCompression(["zip", "tar"])

        self.uncompressed_path = os.path.join(self.compilation_path, f"{self.pkgname}-{self.pkgver}")
        print_status(f"Setting {ColorStr('uncompressed_path').StyleBRIGHT} to: {self.uncompressed_path}")

        advice = f"""
        Look for the uncompressed directory in {self.compilation_path} directory
        and check if its name match with {ColorStr('uncompressed_path').StyleBRIGHT} variable value,
        otherwise reset its value
        """
        print_status(advice)

        ansnwer = None
        while True:
            answer = input("Do you want to reset uncompressed_path value(y/n)? ")
            answer = answer.lower()

            if answer in ["y", "yes", "n", "no"]:
                break

        if answer in ["y", "yes"]:
            self.uncompressed_path = input("Reset value: ")

        print_successful(f"Package {self.pkgname}-{self.pkgver} was prepared")

    def build(self): # simple build(use inheritance for more complex builds)
        """
        Build the souce code
        """
        print_status(f"Building {self.pkgname}-{self.pkgver}")
        print(ColorStr("It can take a while, so go for a cafe ...").StyleBRIGHT)
        #import pdb; pdb.set_trace()

        Bash.exec("./configure", where=self.uncompressed_path)
        Bash.exec("make", where=self.uncompressed_path)


    def check(self):
        """
        Check the status of the compiled source
        """
        #import pdb; pdb.set_trace()

        Bash.exec("make check", where=self.uncompressed_path)


    def install(self): # simple installation(use inheritance for more complex installations)
        """
        Install the compiler source code
        """
        print_status(f"Installing {self.pkgname}-{self.pkgver}")
        #import pdb; pdb.set_trace()

        Bash.exec("sudo make install", where=self.uncompressed_path)


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
        pkg_parser = argparse.ArgumentParser()
        pkg_parser.add_argument("-c", "--compilation", type=str,
                                help="Build directory path ")
        pkg_parser.add_argument("--no-download", action='store_true', dest="no_download",
                                help="Avoid download package")
        pkg_parser.add_argument("--no-uncompress", action='store_true', dest="no_uncompress",
                                help="Avoid uncompress package")
        pkg_parser.add_argument("--check", action='store_true',
                                help="Perform check of compilation")

        return pkg_parser


    def __repr__(self):
        return f"Package(name={self.pkgname}, version={self.pkgver})"
