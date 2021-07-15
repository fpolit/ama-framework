#!/usr/bin/env python3
#
# Hashcat utility - combipow
#
# Status:
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


from hcutils import pycombipow

# debugged - date: Mar 4 2021
class HcutilsCombipow(Auxiliary):
    """
    Hashcat utilities - combipow
    """
    DESCRIPTION = "Hashcat Utility - Combinator"
    MNAME = "auxiliary/wordlists/hcutils_combipow"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Produces all “unique combinations” from a short list of inputs
        """
    )

    REFERENCES = [
        "https://hashcat.net/wiki/doku.php?id=hashcat_utils"
    ]

    def __init__(self, wordlist=None, output=None, storage_dir:str = None):

        if storage_dir is None:
            storage_dir = os.getcwd()

        auxiliary_options = {
            'WORDLIST': Argument(wordlist, True, "Wordlist file"),
            'OUTPUT': Argument(output, True, "Output file"),
            'JOB_NAME': Argument('combinator-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': HcutilsCombipow.MNAME,
            'authors': HcutilsCombipow.AUTHORS,
            'description': HcutilsCombipow.DESCRIPTION,
            'fulldescription': HcutilsCombipow.FULLDESCRIPTION,
            'references': HcutilsCombipow.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'exec_main_thread': False
        }

        super().__init__(**init_options)

    def run(self, quiet:bool = False):
        """
        Combipow - Hashcat utility
        """

        #import pdb; pdb.set_trace()
        try:

            wordlist_file = self.options['WORDLIST'].value

            if not os.path.isfile(wordlist_file):
                raise Exception(f"File {wordlist_file} doesn't exist")

            output_file = self.options['OUTPUT'].value

            print(f"[*] Combining words of {wordlist_file} file")
            status = pycombipow(wordlist_file, output_file)

            if status != 0:
                raise Exception(f"Some error has ocurred while combining words of {wordlist_file}")

            return output_file


        except Exception as error:
            print(error) # print_failure
