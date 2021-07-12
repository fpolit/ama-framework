#!/usr/bin/env python3
#
# hashid - auxiliary application (hash identificator)
#
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import List
import os
import sys
import re
from sbash import Bash
from pathlib import Path

# hashid package imports
from hashid import (
    HashID as _HashID,
    writeResult
)

from ama.plugins.auxiliary import Auxiliary
from ama.utils.fineprint import (
    print_failure,
    print_status,
    print_successful
)
from ama.utils.validator import Args



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
            query_hash_pattern = re.compile(r"(\w*|\w*|.*):?(\w*|\w*|.*)") #parser to analize: NAME:HASH hashes
            for qhash in query_hashes:
                parser_hash = query_hash_pattern.fullmatch(qhash)
                if parser_hash.group(2):
                    qhash = parser_hash.group(2)
                else:
                    qhash = parser_hash.group(1)

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
