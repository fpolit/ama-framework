#!/usr/bin/env python3
#
# hash identifier - hashID
#
# date: Feb 23 2021
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
from ama.core.plugins.auxiliary.hashes import HashID as PLuginHashID

# validator imports
from ama.core.validator import Args
from ama.core.files import Path


class HashID(Auxiliary):
    """
    hash identifier - hashID
    """
    DESCRIPTION = "HashID - hash identifier"
    MNAME = "auxiliary/hashes/hashid"
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
        "https://github.com/psypanda/hashID"
    ]

    def __init__(self, *,
                 hashes: str = None, output: str = None,
                 extended: bool = True, hashcat: bool = True, john: bool = True):

        auxiliary_options = {
            'hashes': Argument(hashes, True, "Hashes to identify (hash or hashes file)"),
            'output': Argument(output, False, "Output File"),
            'extended': Argument(extended, True, "List all possible hash algorithms including salted passwords"),
            'hashcat': Argument(hashcat, True, "Show corresponding Hashcat mode in output"),
            'john': Argument(john, True, "Show corresponding John hash format in output")
        }

        init_options = {
            'mname': HashID.MNAME,
            'author': HashID.AUTHOR,
            'description': HashID.DESCRIPTION,
            'fulldescription': HashID.FULLDESCRIPTION,
            'references': HashID.REFERENCES,
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


            if os.path.isfile(self.options['hashes'].value) and \
               os.access(self.options['hashes'].value, os.R_OK):
                hashes_file = open(self.options['hashes'].value, 'r')
                hashes = [query_hash.rstrip() for query_hash in hashes_file.readlines()]
                hashes_file.close()

            else:
                hashes = self.options['hashes'].value.split(',')

            phid = PLuginHashID()
            phid.identify_hashes(hashes,
                                 hashcat = self.options['hashcat'].value,
                                 john = self.options['john'].value,
                                 extended = self.options['extended'].value,
                                 output = self.options['output'].value)

        except Exception as error:
            print_failure(error)
