#!/usr/bin/env python3
#
# General Package Class
#
# Maintainer: glozanoa <glozanoa@uni.pe>

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
        self.compilation_path = os.path.join(os.getcwd(), self.pkgname)
        self.uncompressed_path = None #path of uncompressed directory


    def depends_info(self):
        print_status("These packages are required to continue with the installation:")
        print_status("Dependencies:")
        for depend in self.depends:
            print(f"\t{depend}")

        print_status("Compilation dependencies (only used for compilation):")
        for depend in self.makedepends:
            print(f"\t{depend}")

        not_continue = True
        while not_continue:
            answer = input("Do you have installed all dependencies.(y/n)? ")
            answer = answer.lower()

            if answer in ["y", "yes"]:
                not_continue = False
            elif answer in ["n", "no"]:
                print_status(f"Install all the dependencies before install {self.pkgname}-{self.pkgver}")
                sys.exit(1)

    def prepare(self, uncompressed_dir:str =None):
        """
        Download and uncompress the source code
        """
        self.depends_info()
        os.mkdir(self.compilation_path)
        os.chdir(self.compilation_path)
        Bash.exec(f"wget {self.source}")

        ## uncompress
        compressed_file = os.path.basename(self.source)

        if zipfile.is_zipfile(compressed_file): # source was compressed using zip
            with zipfile.ZipFile(compressed_file, 'r') as zip_compressed_file:
                zip_compressed_file.extractall()

        elif tarfile.is_tarfile(compressed_file): # source was compressed using tar
            with tarfile.TarFile(compressed_file, 'r') as tar_compressed_file:
                tar_compressed_file.extractall()
        else:
            raise UnsupportedCompression(["zip", "tar"])

    def build(self): # simple build(use inheritance for more complex builds)
        """
        Build the souce code
        """
        #os.chdir(self.compilation_path)
        Bash.exec("./configure")
        Bash.exec("make")


    def check(self):
        """
        Check the status of the compiled source
        """
        Bash.exec("make check")


    def install(self): # simple installation(use inheritance for more complex installations)
        Bash.exec("sudo make install")


    def doall(self):
        """
        Install the buildable package(build, check, and install)
        """
        self.prepare()
        self.build()
        self.check()
        self.install()
        print_successful(f"Sucefully installation of {self.pkgname}")


    def __repr__(self):
        return f"Package(name={self.pkgname}, version={self.pkgver})"
