#!/usr/bin/env python3
#
# hash identifier - nth
#
# State: TESTED - date: Jul 13 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import argparse
from cmd2 import Cmd2ArgumentParser
import os


from ama.modules.base import Auxiliary
from ama.plugins.auxiliary.hashes import Nth as PluginNth

from ama.utils import Argument
from ama.utils.fineprint import print_failure
from ama.utils.validator import Args


class Nth(Auxiliary):
    """
    hash identifier - nth
    """
    DESCRIPTION = "Nth (name-that-hash) - Hash Identifier"
    MNAME = "auxiliary/hashes/nth"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
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
            'HASHES': Argument(hashes, True, "Hashes to identify (hashes[split by commas] or hashes file)"),
            'MOST_LIKELY': Argument(most_likely, True, "Show the most like hashes type"),
            'HASHCAT': Argument(hashcat, True, "Show corresponding Hashcat mode"),
            'JOHN': Argument(john, True, "Show corresponding John hash format"),
            'BASE64': Argument(base64, True, "Decodes hashes in Base64 before identification"),
            'JOB_NAME': Argument('nth-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': Nth.MNAME,
            'authors': Nth.AUTHORS,
            'description': Nth.DESCRIPTION,
            'fulldescription': Nth.FULLDESCRIPTION,
            'references': Nth.REFERENCES,
            'auxiliary_options': auxiliary_options
        }

        super().__init__(**init_options)

    def run(self, quiet=False):
        """
        Identify an hash or hashes in a file using hashid
        """
        #import pdb; pdb.set_trace()
        try:

            #self.no_empty_required_options()
            nth = PluginNth()

            if os.path.isfile(self.options['HASHES'].value) and \
               os.access(self.options['HASHES'].value, os.R_OK):
                hashes_file = open(self.options['HASHES'].value, 'r')
                hashes = [query_hash.rstrip() for query_hash in hashes_file.readlines()]
                hashes_file.close()

            else: # HASHES option is a string (a simple hash)
                hashes = self.options['HASHES'].value.split(',')

            hashes_identity = nth.hashes_identify(hashes,
                                                  hashcat = self.options['HASHCAT'].value,
                                                  john = self.options['JOHN'].value,
                                                  base64 = self.options['BASE64'].value,
                                                  most_likely = self.options['MOST_LIKELY'].value,
                                                  quiet = quiet)


            return hashes_identity

        except Exception as error:
            print_failure(error)
