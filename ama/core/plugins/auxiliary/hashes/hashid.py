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

from typing import List
import os
import sys

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

# hashid package imports
from hashid import (
    HashID as _HashID,
    writeResult
)

class HashID(Auxiliary):
    """
    Identify the different types of hashes
    """

    MAINNAME = "hashid"
    def __init__(self):
        super().__init__(["hashid"], version="v3.1.4", search_exec=False)


    def identify_hashes(self, query_hashes: List[str] = None, *,
                        hashcat: bool = True, john: bool = True, extended: bool = True,
                        output: str = None, quiet: bool = False):
        """
        Identify the type of the supplied hashes

        return {hash: [POSIBLE_IDENTITIES, ...], ...}
        """
        #import pdb; pdb.set_trace()

        try:

            identities = {} # {hash: [POSIBLE_IDENTITIES, ...], ...}
            hid = _HashID()
            for qhash in query_hashes:
                if qhash not in identities:
                    identities[qhash] = []
                    identified_modes = hid.identifyHash(qhash)
                    for hash_info in identified_modes:
                        if not hash_info.extended or extended:
                            identities[qhash].append(hash_info)



            if not quiet:
                if output is None:
                    output = sys.stdout
                else:
                    output = open(output, 'w')

                for qhash, modes in identities.items():
                    output.write(f"\nAnalizing hash: {qhash}\n")
                    writeResult(modes, output,
                                hashcatMode=hashcat, johnFormat=john,
                                extended=extended)

            return identities

        except Exception as error:
            print_failure(error)

        finally:
            if output is not None and \
               output != sys.stdout and \
                not isinstance(output, str):
                print_successful(f"Possible hashes identities saved in: {output.name}")
                output.close()
