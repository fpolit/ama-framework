#!/usr/bin/env python3
#
# sth (search-that-name) - cracker/hashes plugin
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os

from sbash import Bash
from fineprint.status import (
    print_failure,
    print_status
)


from .cracker import PasswordCracker

# core.file imports
from ama.core.files import Path

# validator
from ama.core.validator import Args

class STH(PasswordCracker):
    """
    automate the search of hashes on the most popular hash cracking websites
    """

    MAINNAME = "sth"
    def __init__(self):
        super().__init__(["sth"], version="v0.2.2")

    def search_hash(self,
                      query_hash: str, *,
                      timeout: int, greppable: bool = False):
        """
        search an hash in all the availables online cracking APIs
        """

        #import pdb; pdb.set_trace()

        if self.enable:
            sth_cmd = f"{self.main_exec} --no-banner --accessible"

            if isinstance(timeout, int) and timeout > 0:
                sth_cmd += f"--timeout {timeout}"

            sth_cmd += f" --text {query_hash}"

            print_status(f"Searching {query_hash} hash in availables online cracking APIs")
            Bash.exec(sth_cmd)

        else:
            print_failure("Auxliary plugin {self.main_name} is disable")


    def search_hashes(self,
                      hashes_file: str, *,
                      timeout: int, greppable: bool = False):
        """
        search each hash in hashes_file in all the availables online cracking APIs
        """

        #import pdb; pdb.set_trace()

        try:
            if self.enable:
                permission = [os.R_OK]
                Path.access(permission, hashes_file)

                sth_cmd = f"{self.main_exec} --no-banner --accessible"

                if isinstance(timeout, int) and timeout > 0:
                    sth_cmd += f"--timeout {timeout}"

                sth_cmd += f" --file {hashes_file}"

                print_status(f"Searching hashes in {hashes_file} file in availables online cracking APIs")
                Bash.exec(sth_cmd)

            else:
                print_failure("Auxliary plugin {self.main_name} is disable")

        except Exception as error:
            print_failure(error)
