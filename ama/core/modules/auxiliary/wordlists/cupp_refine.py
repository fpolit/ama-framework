#!/usr/bin/env python3
#
# Cupp - refine a wordlist
#
# date: Mar 32 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from fineprint.status import print_failure

# Cupp plugin
from ama.core.plugins.auxiliary import Cupp

# Auxliary base class
from ama.core.modules.base import Auxiliary
from ama.core.modules.base import Argument


class CuppRefine(Auxiliary):
    """
    Cupp - refine a wordlist
    """

    DESCRIPTION = "Cupp - refine a wordlist"
    MNAME = "auxiliary/wordlists/cupp_refine"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = """
    Refine a supplied wordlist concatenating words or
    adding special chars or random numbers to the end of each word
    """
    REFERENCES = [
        "https://www.hackingarticles.in/comprehensive-guide-on-cupp-a-wordlist-generating-tool/",
        "https://github.com/Mebus/cupp"
    ]

    def __init__(self, wordlist: str = None, slurm=None):
        auxiliary_options = {
            'wordlist': Argument(wordlist, True, "Wordlist to refine")
        }
        init_options = {
            'mname': CuppRefine.MNAME,
            'author': CuppRefine.AUTHOR,
            'description': CuppRefine.DESCRIPTION,
            'fulldescription': CuppRefine.FULLDESCRIPTION,
            'options': auxiliary_options,
            'slurm': slurm
        }

        super().__init__(**init_options)


    def run(self):
        """
        Refine a wordlist
        """

        try:
            self.no_empty_required_options()
            cupp = Cupp()
            cupp.refine(
                self.options['wordlist'].value
            )

        except Exception as error:
            print_failure(error)
