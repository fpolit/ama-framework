#!/usr/bin/env python3
#
# nth - auxiliary application (hash identificator)
#
#
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

class NTH(Auxiliary):
    """
    Identify the different types of hashes
    """

    MAINNAME = "nth"
    def __init__(self):
        super().__init__(["nth"], version="v3.1.4")

    def identify_hash(self,
                      query_hash: str, *,
                      hashcat: bool = True, john: bool = True,
                      base64: bool = False,
                      most_likely: bool = True):
        """
        Identify the type of the supplied hash
        """

        #import pdb; pdb.set_trace()

        if self.enable:
            nth_cmd = f"{self.main_exec} --no-banner"

            if most_likely:
                nth_cmd += " -a"

            if not hashcat:
                nth_cmd += f" --no-hashcat"

            if not john:
                nth_cmd += f" --no-john"

            if base64:
                nth_cmd += f" --base64"

            nth_cmd += f" --text {query_hash}"

            print_status(f"Identifying {query_hash} hash")
            Bash.exec(nth_cmd)

        else:
            print_failure("Auxliary plugin {self.main_name} is disable")


    def identify_hashes(self,
                        hashes_file: str, *,
                        hashcat: bool = True, john: bool = True,
                        base64: bool = False,
                        most_likely: bool = True):
        """
        Identify the type of the supplied hashes
        """

        #import pdb; pdb.set_trace()

        try:
            if self.enable:
                permission = [os.R_OK]
                Path.access(permission, hashes_file)

                nth_cmd = f"{self.main_exec} --no-banner"

                if most_likely:
                    nth_cmd += " -a"

                if not hashcat:
                    nth_cmd += f" --no-hashcat"

                if not john:
                    nth_cmd += f" --no-john"

                if base64:
                    nth_cmd += f" --base64"

                nth_cmd += f" --file {hashes_file}"

                print_status(f"Identifying hashes in {hashes_file} file")
                Bash.exec(nth_cmd)

            else:
                print_failure("Auxliary plugin {self.main_name} is disable")

        except Exception as error:
            print_failure(error)
