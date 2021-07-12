#!/usr/bin/env python3
#
# nth - auxiliary application (hash identificator)
#
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import List
from sbash import Bash
from pathlib import Path

# name_that_hash imports
import name_that_hash as nth
from name_that_hash.runner import (
    api_return_hashes_as_dict
)


from ama.plugins.auxiliary import Auxiliary
from ama.utils.fineprint import (
    print_failure,
    print_status,
    print_successful
)
from ama.utils.validator import Args


class Nth(Auxiliary):
    """
    Identify different types of hashes
    """

    MAINNAME = "nth"
    def __init__(self):
        super().__init__(["name_that_hash", "nth"], version="v3.1.4", search_exec=False)

    def hashes_identify(self, hashes: List[str], *,
                        hashcat: bool = True, john: bool = True,
                        base64: bool = False,
                        most_likely: bool = True, quiet=False):
        """
        Identify the type of the supplied hash
        """

        #import pdb; pdb.set_trace()
        if self.enable:

            args = {
                'base64': base64,
                'accessible': most_likely,
                'no_john': not john,
                'no_hashcat': not hashcat,
                'debug': False
            }

            if quiet:
                hashes_identities = api_return_hashes_as_dict(hashes, args)

            else:
                output, hashes_identities = Nth.hashes_identity_nth_api(hashes, args)
                #import pdb; pdb.set_trace()
                pretty_printer = nth.prettifier.Prettifier(args)
                pretty_printer.pretty_print(output)

            return hashes_identities

        else:
            print_failure(f"Auxliary plugin {self.main_name} is disable")



    @staticmethod
    def hashes_identity_nth_api(chash: [str], args: dict = {}):
        """
        Using name-that-hash as an API? Call this function!

        Given a list of hashes of strings
        return a list of dictionaries with the supplied hashes as key and the posible identities as values
        return format: [{QUERY_HASH : [{POSIBLE_HASH_IDENTITY}, ...]}, ...]
        """
        # nth = the object which names the hash types

        #import pdb; pdb.set_trace()
        nth_obj = nth.hash_namer.Name_That_Hash(nth.hashes.prototypes)
        hashChecker = nth.check_hashes.HashChecker(args, nth_obj)

        for i in chash:
            hashChecker.single_hash(i)

        hashes_identities = [hashTypeObj.hash_obj for hashTypeObj in hashChecker.output]

        return hashChecker.output, hashes_identities
