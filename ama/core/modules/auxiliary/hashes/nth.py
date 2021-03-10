#!/usr/bin/env python3
#
# hash identifier - nth
#
# date: Mar 4 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from fineprint.status import print_failure
#from typing import List

# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

# plugins imports
from ama.core.plugins.auxiliary.hashes import Nth as PluginNth

# validator imports
#from ama.core.validator import Args
#from ama.core.files import Path


class Nth(Auxiliary):
    """
    hash identifier - nth
    """
    DESCRIPTION = "Nth (name-that-hash) - Hash Identifier"
    MNAME = "auxiliary/hashes/nth"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]

    FULLDESCRIPTION = (
        """
        Identify different types of hashes used to encrypt data
        and return valid Hashcat or John hashes types
        """
    )

    REFERENCES = [
        "https://github.com/HashPals/Name-That-Hash"
    ]

    def __init__(self, *,
                 hashes: str = None,
                 hashcat: bool = True, john: bool = True,
                 base64: bool = False,
                 banner: bool = False, most_likely: bool = True):

        auxiliary_options = {
            'hashes': Argument(hashes, True, "Hashes to identify (hashes[split by commas] or hashes file)"),
            'most_likely': Argument(most_likely, True, "Show the most like hashes type"),
            'hashcat': Argument(hashcat, True, "Show corresponding Hashcat mode"),
            'john': Argument(john, True, "Show corresponding John hash format"),
            'base64': Argument(base64, True, "Decodes hashes in Base64 before identification"),
        }

        init_options = {
            'mname': Nth.MNAME,
            'author': Nth.AUTHOR,
            'description': Nth.DESCRIPTION,
            'fulldescription': Nth.FULLDESCRIPTION,
            'references': Nth.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self, quiet=False):
        """
        Identify an hash or hashes in a file using hashid
        """
        #import pdb; pdb.set_trace()
        try:

            self.no_empty_required_options()
            nth = PluginNth()

            if os.path.isfile(self.options['hashes'].value) and \
               os.access(self.options['hashes'].value, os.R_OK):
                hashes_file = open(self.options['hashes'].value, 'r')
                hashes = [query_hash.rstrip() for query_hash in hashes_file.readlines()]

            else: # HASHES option is a string (a simple hash)
                hashes = self.options['hashes'].value.split(',')

                hashes_identities = nth.identify_hashes(hashes,
                                                        hashcat = self.options['hashcat'].value,
                                                        john = self.options['john'].value,
                                                        base64 = self.options['base64'].value,
                                                        most_likely = self.options['most_likely'].value,
                                                        quiet = quiet)


            return hashes_identities

        except Exception as error:
            print_failure(error)
