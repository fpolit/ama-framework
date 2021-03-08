#!/usr/bin/env python3
#
# hash identifier - nth
#
# date: Mar 4 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from fineprint.status import print_failure
import cmd2
from typing import List

# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

# plugins imports
from ama.core.plugins.auxiliary.hashes import NTH as PluginNTH

# validator imports
from ama.core.validator import Args
from ama.core.files import Path


class NTH(Auxiliary):
    """
    hash identifier - nth
    """
    DESCRIPTION = "NTH (name-that-hash) - hash identifier"
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
            'hashes': Argument(hashes, True, "Hashes to identify (hash or hashes file)"),
            'most_likely': Argument(most_likely, True, "Show the most like hashes type"),
            'hashcat': Argument(hashcat, True, "Show corresponding Hashcat mode"),
            'john': Argument(john, True, "Show corresponding John hash format"),
            'base64': Argument(base64, True, "Decodes hashes in Base64 before identification"),
        }

        init_options = {
            'mname': NTH.MNAME,
            'author': NTH.AUTHOR,
            'description': NTH.DESCRIPTION,
            'fulldescription': NTH.FULLDESCRIPTION,
            'references': NTH.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self):
        """
        Identify an hash or hashes in a file using hashid
        """
        try:
            #import pdb; pdb.set_trace()

            self.no_empty_required_options()
            nth = PluginNTH()

            if os.path.isfile(self.options['hashes'].value):
                identify = nth.identify_hashes

            else: # HASHES option is a string (a simple hash)
                identify = nth.identify_hash

            identify(self.options['hashes'].value,
                     hashcat = self.options['hashcat'].value,
                     john = self.options['john'].value,
                     base64 = self.options['base64'].value,
                     most_likely = self.options['most_likely'].value)

        except Exception as error:
            print_failure(error)
