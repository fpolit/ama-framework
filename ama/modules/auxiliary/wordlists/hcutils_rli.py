#!/usr/bin/env python3
#
# Hashcat utility - rli
#
# Status: DOES NOT REMOVE DUPLICATES WORDS (CHECK hcutils PACKAGE: rli.c, rli.h and pyrli.pyx)
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


from hcutils import pyrli


class HcutilsRli(Auxiliary):
    """
    Hashcat utilities - rli
    """
    DESCRIPTION = "Hashcat Utility - rli"
    MNAME = "auxiliary/wordlists/hcutils_rli"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        rli compares a single file against another file(s) and removes all duplicates
        """
    )

    REFERENCES = [
        "https://hashcat.net/wiki/doku.php?id=hashcat_utils"
    ]

    def __init__(self, pwordlist:str = None, rwordlists=None, output:str = None):

        auxiliary_options = {
            'PWORDLIST': Argument(pwordlist, True, "Wordlist to purge"),
            'RWORDLISTS': Argument(rwordlists, True, "Wordlists to compare(directory or list split by commas)"),
            'EXCLUDE': Argument(None, False, "Exclude any RWORDLIST (split by commas)"),
            'OUTPUT': Argument(output, True, "Output file"),
            'JOB_NAME': Argument('rli-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': HcutilsRli.MNAME,
            'authors': HcutilsRli.AUTHORS,
            'description': HcutilsRli.DESCRIPTION,
            'fulldescription': HcutilsRli.FULLDESCRIPTION,
            'references': HcutilsRli.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'exec_main_thread': False
        }

        super().__init__(**init_options)

    def run(self, quiet:bool = False):
        """
        rli - Hashcat utility
        """

        #import pdb; pdb.set_trace()
        try:

            pwordlist = self.options['PWORDLIST'].value

            if not os.path.isfile(pwordlist):
                raise Exception("No wordlist to purde was supplied")

            rwordlists_option = self.options['RWORDLISTS'].value
            exclude = set()
            if self.options['EXCLUDE'].value:
                exclude = set(self.options['EXCLUDE'].value.split(','))

            rwordlists = []
            if os.path.isdir(rwordlists_option):
                for wordlist_name in os.listdir(rwordlists_option):
                    wordlist_file = os.path.join(rwordlists_option, wordlist_name)
                    if os.path.isfile(wordlist_file) and wordlist_name not in exclude:
                        rwordlists.append(wordlist_file)

            else:
                for wordlist_file in rwordlists_option.split(','):
                    if os.path.isfile(wordlist_file) and wordlist_file not in exclude:
                        rwordlists.append(wordlist_file)

            if len(rwordlists) == 0:
                raise Exception("No wordlists to compare were supplied")

            print(f"[*] Wordlist to purge: {pwordlist}")
            print(f"[*] Wordlists to compare: {rwordlists}")

            output_file = self.options['OUTPUT'].value

            status = pyrli(pwordlist, output_file, rwordlists)

            if status != 0:
                print(f"[-] Some error ocurred while purging {pwordlist} with {rwordlists}")

            return output_file


        except Exception as error:
            print(error) # print_failure
