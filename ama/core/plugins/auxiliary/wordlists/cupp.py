#!/usr/bin/env python3
#
# cupp - auxiliary application (wordlists generator)
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os

from sbash import Bash
from fineprint.status import (
    print_failure,
    print_status,
    print_successful
)

import cupp

# from cupp import (
#     print_cow,
#     interactive,
#     download_wordlist,
#     alectodb_download,
#     improve_dictionary,
#     read_config
# )

import cupp


from ama.core.plugins.auxiliary import Auxiliary
from ama.core.files import Path


class Cupp(Auxiliary):
    """
    Common User Passwords Profiler
    """

    MAINNAME = "cupp"

    def __init__(self):
        self.CONFIG = cupp.read_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cupp.cfg"))
        super().__init__(["cupp"], version="v3.3.0", search_exec=False)


    # debugged - date: Mar 4 2021
    def interactive(self, *, quiet=False):
        """
        Cupp - interactive mode (Interactive questions for user password profiling)
        """
        #import pdb; pdb.set_trace()
        if self.enable:
            CONFIG = self.CONFIG
            if not quiet:
                cupp.print_cow()
            generated_wordlist = cupp.interactive()
            return generated_wordlist
        else:
            print_failure("Auxiliary application {self.main_name} is disable")
            return None

    # debugged - date: Mar 4 2021
    def improve_wordlist(self, *, wordlist: str, quiet=False):
        """
        Cupp - improve a wordlist
        """
        #import pdb; pdb.set_trace()
        if self.enable:
            CONFIG = self.CONFIG
            try:
                permission = [os.R_OK]
                Path.access(permission, wordlist)

                if not quiet:
                    cupp.print_cow()
                improved_wordlist = cupp.improve_dictionary(wordlist)

                return improved_wordlist

            except Exception as error:
                print_failure(error)

        else:
            print_failure("Auxiliary application {self.main_name} is disable")
            return None

    # debugged - date: Mar 4 2021
    def download_wordlists(self, *, quiet=False):
        """
        Cupp - download huge wordlists from repository
        """
        if self.enable:
            CONFIG = self.CONFIG
            if not quiet:
                cupp.print_cow()
            cupp.download_wordlist()
        else:
            print_failure("Auxiliary application {self.main_name} is disable")

    # debugged - date: Mar 4 2021
    def alectodb(self, *,quiet=False):
        """
        Cupp - Parse default usernames and passwords directly from Alecto DB. Project Alecto uses purified
        databases of Phenoelit and CIRT which were merged and enhanced
        """
        if self.enable:
            CONFIG = self.CONFIG
            if not quiet:
                cupp.print_cow()
            cupp.alectodb_download()
        else:
            print_failure("Auxiliary application {self.main_name} is disable")
