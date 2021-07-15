#!/usr/bin/env python3
#
# Hashcat utility - mli2
#
# Status: TESTED - date Jul 15 2021
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from itertools import combinations
from pathlib import Path
import os

from fineprint.status import print_failure

# Auxliary base class
from ama.modules.base import Auxiliary
from ama.utils import Argument
from ama.utils.files import only_name


from hcutils import pymli2

# debugged - date: Mar 4 2021
class HcutilsMli2(Auxiliary):
    """
    Hashcat utilities - mli2
    """
    DESCRIPTION = "Hashcat Utility - mli2"
    MNAME = "auxiliary/wordlists/hcutils_mli2"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Merge 2 sorted wordlists
        """
    )

    REFERENCES = [
        "https://hashcat.net/wiki/doku.php?id=hashcat_utils"
    ]

    def __init__(self, wordlists=None, output=None):

        auxiliary_options = {
            'WORDLISTS': Argument(wordlists, True, "Wordlist files (split by commas)"),
            'OUTPUT': Argument(output, True, "Output file"),
            'JOB_NAME': Argument('mli2-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': HcutilsMli2.MNAME,
            'authors': HcutilsMli2.AUTHORS,
            'description': HcutilsMli2.DESCRIPTION,
            'fulldescription': HcutilsMli2.FULLDESCRIPTION,
            'references': HcutilsMli2.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'exec_main_thread': False
        }

        super().__init__(**init_options)

    def run(self, quiet:bool = False):
        """
        mli2 - Hashcat utility
        """

        #import pdb; pdb.set_trace()
        try:

            wordlist_files = self.options['WORDLISTS'].value.split(',')


            if len(wordlist_files) != 2:
                raise Exception(f"Only supplied 2 wordlists ({len(wordlist_files)} was supplied)")

            # check if each wordlist exists

            output_file = self.options['OUTPUT'].value

            wl1, wl2 = wordlist_files
            print(f"[*] Merging {wl1} and {wl2} into {output_file} file")
            status = pymli2(wl1, wl2, output_file)

            if status != 0:
                raise Exception(f"Some error was ocurred while merging {wl1} and {wl2} wordlists")

            return output_file


        except Exception as error:
            print(error) # print_failure
