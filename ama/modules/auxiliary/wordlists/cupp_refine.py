#!/usr/bin/env python3
#
# Cupp - refine a wordlist
#
# date: Mar 32 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from fineprint.status import print_failure

# Cupp plugin
from ama.plugins.auxiliary.wordlists import Cupp

# Auxliary base class
from ama.modules.base import Auxiliary

from ama.utils import Argument

# debugged - date: Mar 4 2021
class CuppRefine(Auxiliary):
    """
    Cupp - refine a wordlist
    """

    DESCRIPTION = "Cupp - refine a wordlist"
    MNAME = "auxiliary/wordlists/cupp_refine"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
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
            'WORDLIST': Argument(wordlist, True, "Wordlist to refine"),
            #'quiet': Argument(quiet, True, "Don't print cupp's fancy banner")
        }
        init_options = {
            'mname': CuppRefine.MNAME,
            'author': CuppRefine.AUTHOR,
            'description': CuppRefine.DESCRIPTION,
            'fulldescription': CuppRefine.FULLDESCRIPTION,
            'references': CuppRefine.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'exec_main_thread': True
        }

        super().__init__(**init_options)


    def run(self, quiet: bool = False):
        """
        Refine a wordlist
        """
        #import pdb; pdb.set_trace()
        try:
            #self.no_empty_required_options()
            cupp = Cupp()
            improved_wordlist = cupp.improve_wordlist(wordlist= self.options['WORDLIST'].value,
                                                      quiet = quiet)

            return improved_wordlist

        except Exception as error:
            print(error) # print_failure
