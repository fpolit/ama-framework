#!/usr/bin/env python3
#
# hashid - auxiliary application (hash identificator)
#
# NOTE (date: Mar 4 2021) - Try to remove this bug
# /usr/local/hack/dev/fpolit/ama/env/lib/python3.9/site-packages/varname/utils.py:353: UserWarning: Cannot evaluate node Attribute(value=Name(id='Args', ctx=Load()), attr='some_not_none', ctx=Load()) using 'pure_eval'. Using 'eval' to get the function that calls 'argname'. Try calling it using a variable reference to the function, or passing the function to 'argname' explicitly.
#   warnings.warn(
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

# validator
from ama.core.validator import Args

class HashID(Auxiliary):
    """
    Identify the different types of hashes
    """

    MAINNAME = "hashid"
    def __init__(self):
        super().__init__(["hashid"], version="v3.1.4")


    def identify_hash(self, query_hash: str = None, *,
                      hashcat: bool = True, john: bool = True, extended: bool = True,
                      output: str = None):
        """
        Identify the type of the supplied hashe
        """
        #import pdb; pdb.set_trace()

        if self.enable:
            #Args.some_not_none(query_hash, hashes_file)

            if query_hash: #identify the supplied hash
                hashid_cmd = f"{self.main_exec}"

                if hashcat:
                    hashid_cmd += f" -m"

                if john:
                    hashid_cmd += f" -j"

                if extended:
                    hashid_cmd += f" -e"

                if output:
                    hashid_cmd += f" -o {output}"

                hashid_cmd += f" {query_hash}"

                print_status(f"Identifying {query_hash} hash")
                Bash.exec(hashid_cmd)

                if output:
                    print_successful(f"Possible valid hashes types saved in {output}")
                else:
                    print()

        else:
            print_failure("Auxliary plugin {self.main_name} is disable")



    def identify_hashes(self, hashes_file: str = None,  *,
                        hashcat: bool = True, john: bool = True, extended: bool = True,
                        output: str = None):
        """
        Identify the type of the hashes in a file
        """

        #import pdb; pdb.set_trace()

        if self.enable:
            hashid_cmd = f"{self.main_exec}"

            if hashcat:
                hashid_cmd += f" -m"

            if john:
                hashid_cmd += f" -j"

            if extended:
                hashid_cmd += f" -e"

            if output:
                hashid_cmd += f" -o {output}"

            hashid_cmd += f" {hashes_file}"

            print_status(f"Identifying hashes in {hashes_file} file")
            Bash.exec(hashid_cmd)

            if output:
                print_successful(f"Possible valid hashes types saved in {output}")
            else:
                print()

        else:
            print_failure("Auxliary plugin {self.main_name} is disable")
