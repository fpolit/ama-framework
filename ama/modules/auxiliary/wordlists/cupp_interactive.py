#!/usr/bin/env python3
#
# Cupp - interactive mode
#
# State: TESTED - date: Jul 13 2021
#
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
    AUTHORS = [
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

        auxiliary_options = {}

        init_options = {
            'mname': CuppInteractive.MNAME,
            'authors': CuppInteractive.AUTHORS,
            'description': CuppInteractive.DESCRIPTION,
            'fulldescription': CuppInteractive.FULLDESCRIPTION,
            'references': CuppInteractive.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'exec_main_thread': True
        }

        super().__init__(**init_options)

    def run(self, quiet:bool = False):
        """
        Execution of Cupp interactive mode
        """

        #import pdb; pdb.set_trace()
        try:
            #self.no_empty_required_options()
            cupp = Cupp()
            generated_wordlist = cupp.interactive(quiet = quiet)

            return generated_wordlist

        except Exception as error:
            print(error) # print_failure
