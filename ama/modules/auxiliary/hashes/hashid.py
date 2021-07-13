#!/usr/bin/env python3
#
# hash identifier - hashID
#
# State: TESTED - date: Jul 13 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from pathlib import Path
import os
import cmd2
from typing import List

from ama.modules.base import Auxiliary
from ama.plugins.auxiliary.hashes import HashID as PLuginHashID

from ama.utils import Argument
from ama.utils.fineprint import print_failure
from ama.utils.validator import Args


class HashID(Auxiliary):
    """
    hash identifier - hashID
    """
    DESCRIPTION = "HashID - hash identifier"
    MNAME = "auxiliary/hashes/hashid"
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
        "https://github.com/psypanda/hashID"
    ]

    def __init__(self, *,
                 hashes: str = None, output: str = None,
                 extended: bool = True, hashcat: bool = True, john: bool = True):

        auxiliary_options = {
            'HASHES': Argument(hashes, True, "Hashes to identify (hash or hashes file)"),
            'OUTPUT': Argument(output, False, "Output File"),
            'EXTENDED': Argument(extended, True, "List all possible hash algorithms including salted passwords"),
            'HASHCAT': Argument(hashcat, True, "Show corresponding Hashcat mode in output"),
            'JOHN': Argument(john, True, "Show corresponding John hash format in output"),
            'JOB_NAME': Argument('hashid-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': HashID.MNAME,
            'authors': HashID.AUTHORS,
            'description': HashID.DESCRIPTION,
            'fulldescription': HashID.FULLDESCRIPTION,
            'references': HashID.REFERENCES,
            'auxiliary_options': auxiliary_options
        }

        super().__init__(**init_options)

    def run(self, quiet: bool = False):
        """
        Identify an hash or hashes in a file using hashid
        """
        try:
            #import pdb; pdb.set_trace()

            #self.no_empty_required_options()


            if os.path.isfile(self.options['HASHES'].value) and \
               os.access(self.options['HASHES'].value, os.R_OK):
                hashes_file = open(self.options['HASHES'].value, 'r')
                hashes = [query_hash.rstrip() for query_hash in hashes_file.readlines()]
                hashes_file.close()

            else:
                hashes = self.options['HASHES'].value.split(',')

            phid = PLuginHashID()
            identities = phid.identify_hashes(hashes,
                                              hashcat = self.options['HASHCAT'].value,
                                              john = self.options['JOHN'].value,
                                              extended = self.options['EXTENDED'].value,
                                              output = self.options['OUTPUT'].value,
                                              quiet= quiet)

            return identities

        except Exception as error:
            print_failure(error)
