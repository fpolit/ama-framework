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


from ama.core.plugins.auxiliary import Auxiliary

# core.file imports
from ama.core.files import Path

class Cupp(Auxiliary):
    """
    Common User Passwords Profiler
    """

    MAINNAME = "cupp"
    def __init__(self):
        super().__init__(["cupp"], version="v3.3.0")

    # debugged - date: Mar 4 2021
    def interactive(self):
        """
        Cupp - interactive mode (Interactive questions for user password profiling)
        """
        if self.enable:
            Bash.exec(f"{self.main_exec} -i")
        else:
            print_failure("Auxiliary application {self.main_name} is disable")

    # debugged - date: Mar 4 2021
    def refine(self, wordlist: str):
        """
        Cupp - refine a wordlist
        """
        #import pdb; pdb.set_trace()
        if self.enable:
            try:
                permission = [os.R_OK]
                Path.access(permission, wordlist)
                Bash.exec(f"{self.main_exec} -w {wordlist}")

            except Exception as error:
                print_failure(error)

    # debugged - date: Mar 4 2021
    def download_wordlists(self):
        """
        Cupp - download huge wordlists from repository
        """
        if self.enable:
            Bash.exec(f"{self.main_exec} -l")
        else:
            print_failure("Auxiliary application {self.main_name} is disable")

    # debugged - date: Mar 4 2021
    def alecto(self):
        """
        Cupp - Parse default usernames and passwords directly from Alecto DB. Project Alecto uses purified
        databases of Phenoelit and CIRT which were merged and enhanced
        """
        if self.enable:
            Bash.exec(f"{self.main_exec} -a")
        else:
            print_failure("Auxiliary application {self.main_name} is disable")
