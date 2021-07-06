#!/usr/bin/env python3
#
# Bopscrk - interactive mode
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
class BopscrkInteractive(Auxiliary):
    """
    Bopscrk - interactive mode
    """
    DESCRIPTION = "Bopscrk - Interactive mode"
    MNAME = "auxiliary/wordlists/bopscrk_interactive"
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
        "https://github.com/r3nt0n/bopscrk",
        "https://www.hackingarticles.in/wordlists-for-pentester/"
    ]

    def __init__(self):
        """
        Initialization of Bopscrk - interactive mode
        """

        auxiliary_options = {
            'output': Argument(Bopscrk.DEFAULT_OUTPUT_FILE, True, "Output File", value_type=str)
        }

        init_options = {
            'mname': BopscrkInteractive.MNAME,
            'author': BopscrkInteractive.AUTHOR,
            'description': BopscrkInteractive.DESCRIPTION,
            'fulldescription': BopscrkInteractive.FULLDESCRIPTION,
            'references': BopscrkInteractive.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self, quiet:bool = False):
        """
        Execution of Bopscrk interactive mode
        """

        #import pdb; pdb.set_trace()
        try:
            self.no_empty_required_options()
            bopscrk = Bopscrk()
            generated_wordlist = bopscrk.interactive(
                quiet = quiet,
                ouput = self.options['ouput'].value
            )

            return generated_wordlist

        except Exception as error:
            print_failure(error)
