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
    CONFIG = cupp.read_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cupp.cfg"))
    def __init__(self):
        super().__init__(["cupp"], version="v3.3.0", search_exec=False)


    # debugged - date: Mar 4 2021
    def interactive(self, *, quiet=False, CONFIG=Cupp.CONFIG):
        """
        Cupp - interactive mode (Interactive questions for user password profiling)
        """
        if self.enable:
            if not quiet:
                cupp.print_cow()
            cupp.interactive()
        else:
            print_failure("Auxiliary application {self.main_name} is disable")

    # debugged - date: Mar 4 2021
    def improve_wordlist(self, *, wordlist: str, quiet=False, CONFIG=Cupp.CONFIG):
        """
        Cupp - improve a wordlist
        """
        #import pdb; pdb.set_trace()
        if self.enable:
            try:
                permission = [os.R_OK]
                Path.access(permission, wordlist)

                if not quiet:
                    cupp.print_cow()
                cupp.improve(wordlist)

            except Exception as error:
                print_failure(error)

        else:
            print_failure("Auxiliary application {self.main_name} is disable")
    # debugged - date: Mar 4 2021
    def download_wordlists(self, *, quiet=False, CONFIG=Cupp.CONFIG):
        """
        Cupp - download huge wordlists from repository
        """
        if self.enable:
            if not quiet:
                cupp.print_cow()
            cupp.download_wordlist()
        else:
            print_failure("Auxiliary application {self.main_name} is disable")

    # debugged - date: Mar 4 2021
    def alectodb(self, *,quiet=False, CONFIG=Cupp.CONFIG):
        """
        Cupp - Parse default usernames and passwords directly from Alecto DB. Project Alecto uses purified
        databases of Phenoelit and CIRT which were merged and enhanced
        """
        if self.enable:
            if not quiet:
                cupp.print_cow()
            cupp.alectodb_download()
        else:
            print_failure("Auxiliary application {self.main_name} is disable")
