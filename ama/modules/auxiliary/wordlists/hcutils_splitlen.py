#!/usr/bin/env python3
#
# Hashcat utility - splitlen
#
# Status:
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from pathlib import Path
import os

from fineprint.status import print_failure

# Auxliary base class
from ama.modules.base import Auxiliary
from ama.utils import Argument
from ama.utils.files import only_name


from hcutils import pysplitlen

class HcutilsSplitlen(Auxiliary):
    """
    Hashcat utilities - splilen
    """
    DESCRIPTION = "Hashcat Utility - splitlen"
    MNAME = "auxiliary/wordlists/hcutils_splitlen"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Split a wordlist by the length of their words
        """
    )

    REFERENCES = [
        "https://hashcat.net/wiki/doku.php?id=hashcat_utils"
    ]

    def __init__(self, wordlist=None, outdir=None):

        auxiliary_options = {
            'WORDLIST': Argument(wordlist, True, "Wordlist file"),
            'OUTDIR': Argument(outdir, True, "Output directory"),
            'JOB_NAME': Argument('splitlen-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': HcutilsSplitlen.MNAME,
            'authors': HcutilsSplitlen.AUTHORS,
            'description': HcutilsSplitlen.DESCRIPTION,
            'fulldescription': HcutilsSplitlen.FULLDESCRIPTION,
            'references': HcutilsSplitlen.REFERENCES,
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

            wordlist = self.options['WORDLIST'].value


            if not os.path.isfile(wordlist):
                raise Exception(f"File {wordlist} don't exist")

            # check if each wordlist exists

            outdir = self.options['OUTDIR'].value

            print(f"[*] Split {wordlist} wordlist by length and save them in {outdir} directory")
            status = pysplitlen(outdir, wordlist)

            if status != 0:
                raise Exception(f"Some error was ocurred while spliting {wordlist} wordlist")


        except Exception as error:
            print(error) # print_failure
