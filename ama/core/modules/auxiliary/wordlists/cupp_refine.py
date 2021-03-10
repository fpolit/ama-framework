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
from ama.core.modules.base import (
    Auxiliary,
    Argument
)


# debugged - date: Mar 4 2021
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

    FULLDESCRIPTION = (
        """
        Refine a supplied wordlist concatenating words or
        adding special chars or random numbers to the end of each word
        """
    )

    REFERENCES = [
        "https://www.hackingarticles.in/comprehensive-guide-on-cupp-a-wordlist-generating-tool/",
        "https://github.com/Mebus/cupp"
    ]

    def __init__(self, wordlist: str = None, quiet:bool = False):
        auxiliary_options = {
            'wordlist': Argument(wordlist, True, "Wordlist to refine"),
            'quiet': Argument(quiet, True, "Don't print cupp's fancy banner")
        }
        init_options = {
            'mname': CuppRefine.MNAME,
            'author': CuppRefine.AUTHOR,
            'description': CuppRefine.DESCRIPTION,
            'fulldescription': CuppRefine.FULLDESCRIPTION,
            'references': CuppRefine.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)


    def run(self):
        """
        Refine a wordlist
        """
        import pdb; pdb.set_trace()
        try:
            self.no_empty_required_options()
            cupp = Cupp()
            cupp.improve_wordlist(wordlist= self.options['wordlist'].value,
                                  quiet = self.options['quiet'].value)

        except Exception as error:
            print_failure(error)
