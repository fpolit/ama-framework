#!/usr/bin/env python3
#
# Cupp - alecto
#
# date: Mar 3 2021
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
class CuppAlecto(Auxiliary):
    """
    Cupp - Alecto
    """
    DESCRIPTION = "Cupp - Alecto Database"
    MNAME = "auxiliary/wordlists/cupp_alecto"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = """
    Cupp - Parse default usernames and passwords directly from Alecto DB. Project Alecto uses purified
    databases of Phenoelit and CIRT which were merged and enhanced
    """
    REFERENCES = [
        "https://www.hackingarticles.in/comprehensive-guide-on-cupp-a-wordlist-generating-tool/",
        "https://github.com/Mebus/cupp"
    ]

    def __init__(self, *, quiet=False):
        """
        Initialization of Cupp - Alecto
        """

        auxiliary_options = {
            'quiet': Argument(quiet, True, "Don't print cupp's fancy banner")
        }
        init_options = {
            'mname': CuppAlecto.MNAME,
            'author': CuppAlecto.AUTHOR,
            'description': CuppAlecto.DESCRIPTION,
            'fulldescription': CuppAlecto.FULLDESCRIPTION,
            'references': CuppAlecto.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self):
        """
        Execution of Cupp - alecto
        """
        try:
            self.no_empty_required_options()
            cupp = Cupp()
            cupp.alectodb(quiet = self.options['quiet'].value)

        except Exception as error:
            print_failure(error)
