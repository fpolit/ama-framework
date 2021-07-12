#!/usr/bin/env python3
#
# Cupp - interactive mode
#
# date: Mar 3 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from fineprint.status import print_failure

# Cupp plugin
from ama.plugins.auxiliary.wordlists import Cupp

# Auxliary base class
from ama.modules.base import Auxiliary

from ama.utils import Argument


# debugged - date: Mar 4 2021
class CuppInteractive(Auxiliary):
    """
    Cupp - interactive mode
    """
    DESCRIPTION = "Cupp - Interactive mode"
    MNAME = "auxiliary/wordlists/cupp_interactive"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Interactive questions for user password profiling
        """
    )

    REFERENCES = [
        "https://www.hackingarticles.in/comprehensive-guide-on-cupp-a-wordlist-generating-tool/",
        "https://github.com/Mebus/cupp"
    ]

    def __init__(self):
        """
        Initialization of Cupp - interactive mode
        """

        auxiliary_options = {
            #'wordlist': Argument(wordlist, True, "Name of generated wordlist")
        }

        init_options = {
            'mname': CuppInteractive.MNAME,
            'author': CuppInteractive.AUTHOR,
            'description': CuppInteractive.DESCRIPTION,
            'fulldescription': CuppInteractive.FULLDESCRIPTION,
            'references': CuppInteractive.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self, quiet:bool = False):
        """
        Execution of Cupp interactive mode
        """

        #import pdb; pdb.set_trace()
        try:
            self.no_empty_required_options()
            cupp = Cupp()
            generated_wordlist = cupp.interactive(quiet = quiet)

            return generated_wordlist

        except Exception as error:
            print_failure(error)
