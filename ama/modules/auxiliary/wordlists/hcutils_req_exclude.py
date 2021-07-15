#!/usr/bin/env python3
#
# Hashcat utility - req-exclude
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


from hcutils import pyreq_exclude


class HcutilsReqExclude(Auxiliary):
    """
    Hashcat utilities - req-exclude
    """
    DESCRIPTION = "Hashcat Utility - req-exclude"
    MNAME = "auxiliary/wordlists/hcutils_req_exclude"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Excludes words that match specific criteria

        Name 	Item 	Chars
        LOWER 	1 	abcdefghijklmnoprstuvwxyz
        UPPER 	2 	ABCDEFGHIJKLMNOPRSTUVWXYZ
        DIGIT 	4 	0123465789
        SYMBOL 	8 	0x20 to 0x7e NOT IN lower, upper, digit
        OTHER 	16 	All others, not matching the above
        """
    )

    REFERENCES = [
        "https://hashcat.net/wiki/doku.php?id=hashcat_utils"
    ]

    def __init__(self, wordlists=None, exc_mask:int = None, exclude:str = None, storage_dir:str = None):


        if storage_dir is None:
            storage_dir = os.getcwd()

        auxiliary_options = {
            'WORDLISTS': Argument(wordlists, True, "Wordlist files (directory or list split by commas)"),
            'EXC_MASK': Argument(None, True, "Criteria to exclude words", value_type=int),
            'EXCLUDE': Argument(None, False, "Wordlists to exclude (split by commas)"),
            'STORAGE_DIR': Argument(storage_dir, True, "Directory to store purged wordlists"),
            'JOB_NAME': Argument('req-exclude-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': HcutilsReqExclude.MNAME,
            'authors': HcutilsReqExclude.AUTHORS,
            'description': HcutilsReqExclude.DESCRIPTION,
            'fulldescription': HcutilsReqExclude.FULLDESCRIPTION,
            'references': HcutilsReqExclude.REFERENCES,
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

            wordlists_option = self.options['WORDLISTS'].value
            exclude = set()
            if self.options['EXCLUDE'].value:
                exclude = set(self.options['EXCLUDE'].value.split(','))

            wordlists = []
            if os.path.isdir(wordlists_option):
                for wordlist_name in os.listdir(wordlists_option):
                    wordlist_file = os.path.join(wordlists_option, wordlist_name)
                    if os.path.isfile(wordlist_file) and wordlist_name not in exclude:
                        wordlists.append(wordlist_file)

            else:
                for wordlist_file in wordlists_options.split(','):
                    if os.path.isfile(wordlist_file) and wordlist_file not in exclude:
                        wordlists.append(wordlist_file)

            if len(wordlists) == 0:
                raise Exception("No wordlists were supplied")

            print(f"[*] Wordlists to purge: {wordlists}")

            storage_dir = self.options['STORAGE_DIR'].value

            if not os.path.exists(storage_dir):
                os.mkdir(storage_dir)

            criteria = self.options['EXC_MASK'].value
            print(f"[*] Criteria to exclude words: {criteria}")

            status = [0]*len(wordlists)
            output_files = []

            for k, wordlist in enumerate(wordlists):
                wl_name = only_name(wordlist)

                output_name = wl_name + "_purged.txt"
                output_path = os.path.join(storage_dir, output_name)
                output_files.append(output_path)

                print(f"[*] Purge {wordlist} and save to {output_path}")

                status[k] = pyreq_exclude(wordlist, output_path, criteria)

            # check if any error was ocurred
            for state, wl in zip(status, wordlists):
                if state != 0:
                    print(f"[-] Some error ocurred while purging {wordlist}")

            return output_files


        except Exception as error:
            print(error) # print_failure
