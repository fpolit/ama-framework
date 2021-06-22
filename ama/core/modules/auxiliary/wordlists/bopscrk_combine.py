#!/usr/bin/env python3
#
# Bopscrk - Combine words (no interactive mode)
#
# Status:
# Maintainer: glozanoa <glozanoa@uni.pe>

from fineprint.status import print_failure

# Cupp plugin
from ama.core.plugins.auxiliary.wordlists import Bopscrk

# Auxliary base class
from ama.core.modules.base import (
    Auxiliary,
    Argument
)


# debugged - date: Mar 4 2021
class BopscrkCombine(Auxiliary):
    """
    Bopscrk - Combine words
    """
    DESCRIPTION = "Bopscrk - Combine words"
    MNAME = "auxiliary/wordlists/bopscrk_combine"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Combine words
        """
    )

    REFERENCES = [
        "https://github.com/r3nt0n/bopscrk",
        "https://www.hackingarticles.in/wordlists-for-pentester/"
    ]

    def __init__(self):
        """
        Initialization of Bopscrk - interactive mode
        """

        auxiliary_options = {
            'words': Argument(None, True, "words to combine comma-separated (will be combined with all words)"),
            'min_length': Argument(Bopscrk.DEFAULT_MIN, False, "Min length for the words to generate", value_type=int),
            'max_length': Argument(Bopscrk.DEFAULT_MAX, False, "Max length for the words to generate", value_type=int),
            'case': Argument(False, False, "Enable case transformations", value_type=bool),
            'leet': Argument(False, False, "Enable leet transformations", value_type=bool),
            'nwords': Argument(Bopscrk.DEFAULT_N_WORDS, False, "Max amount of words to combine each time", value_type=int),
            'artists': Argument(False, False, "Artists to search song lyrics (comma-separated)"),
            'exclude': Argument(None, False, "Exclude all the words included in other wordlists"),
            'output': Argument(Bopscrk.DEFAULT_OUTPUT_FILE, True, "Output file to save the wordlist")
        }

        init_options = {
            'mname': BopscrkCombine.MNAME,
            'author': BopscrkCombine.AUTHOR,
            'description': BopscrkCombine.DESCRIPTION,
            'fulldescription': BopscrkCombine.FULLDESCRIPTION,
            'references': BopscrkCombine.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self, quiet:bool = False):
        """
        Execution of Bopscrk combine mode
        """

        #import pdb; pdb.set_trace()
        try:
            self.no_empty_required_options()

            bopscrk = Bopscrk()

            generated_wordlist = bopscrk.combine(
                quiet = quiet,
                ouput = self.options['ouput'].value
            )

            return generated_wordlist

        except Exception as error:
            print_failure(error)
