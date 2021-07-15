#!/usr/bin/env python3
#
# Hashcat utility - combinator
#
# Status: TESTED - date: Jul 14 2021
#
# NOTE: pycombinator open mode ('a') OVERWRITE data in output file (instead of append new lines)
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from itertools import combinations
from pathlib import Path
from multiprocessing import Pool
import os

from fineprint.status import print_failure

# Auxliary base class
from ama.modules.base import Auxiliary
from ama.utils import Argument
from ama.utils.files import only_name


from hcutils import pycombinator

# debugged - date: Mar 4 2021
class HcutilsCombinator(Auxiliary):
    """
    Hashcat utilities - combinator
    """
    DESCRIPTION = "Hashcat Utility - Combinator"
    MNAME = "auxiliary/wordlists/hcutils_combinator"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Combine a list of wordlists 2 by 2
        """
    )

    REFERENCES = [
        "https://hashcat.net/wiki/doku.php?id=hashcat_utils"
    ]

    def __init__(self, wordlists=None, storage_dir:str = None, processes:int = 2):

        if storage_dir is None:
            storage_dir = os.getcwd()

        auxiliary_options = {
            'WORDLISTS': Argument(wordlists, True, "Wordlists to combine (directory or list split by commas)"),
            'EXCLUDE': Argument(None, True, "Wordlists to exclude (split by commas)"),
            'INVERSE': Argument(inverse, True, "Include inverse combination"),
            'STORAGE_DIR': Argument(storage_dir, True, "Directory to store generate combinations"),
            'PROCESSES': Argument(processes, True, "Number of process to perform combinations"),
            'JOB_NAME': Argument('combinator-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': HcutilsCombinator.MNAME,
            'authors': HcutilsCombinator.AUTHORS,
            'description': HcutilsCombinator.DESCRIPTION,
            'fulldescription': HcutilsCombinator.FULLDESCRIPTION,
            'references': HcutilsCombinator.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'exec_main_thread': False
        }

        super().__init__(**init_options)

    def run(self, quiet:bool = False):
        """
        Combinator - Hashcat utility
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

            print(f"[*] Wordlists to combine: {wordlists}")

            if len(wordlists) < 2:
                raise Exception("No enough wordlists to combine")


            storage_dir = self.options['STORAGE_DIR'].value

            if not os.path.exists(storage_dir):
                os.mkdir(storage_dir)


            inverse = self.options['INVERSE'].value

            output_files = []
            wl_combinations = []
            for wl1, wl2 in combinations(wordlists, 2):
                wl1_name = only_name(wl1)
                wl2_name = only_name(wl2)

                output_name = wl1_name + '_' + wl2_name + ".txt"
                output = os.path.join(storage_dir, output_name)
                output_files.append(output)

                wl_combinations.append([wl1, wl2, output, inverse])

            status = []
            with Pool(processes=self.options['PROCESSES'].value) as pool:
                status = pool.map(combine2wls, wl_combinations)

            # check return status
            for status, combination in zip(status, wl_combinations):
                if status != 0:
                    wl1, wl2, *_ = combination
                    print(f"[-] Some error ocurred while combining {wl1} and {wl2}")

            return output_files


        except Exception as error:
            print(error) # print_failure


def combine2wls(wl1, wl2, output, inverse):
    print(f"[*] Combining {wl1} and {wl2} into {output}")
    status = pycombinator(wl1, wl2, output)

    inv_status = 0
    if inverse:
        print("[*] Combining {wl1} and {wl2} into {output}")
        inv_status = pycombinator(wl1, wl2, output)

    return status or inv_status
