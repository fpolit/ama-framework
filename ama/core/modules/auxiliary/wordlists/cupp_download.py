#!/usr/bin/env python3
#
# Cupp - Download wordlists
#
# date: Mar 3 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from fineprint.status import print_failure

# Cupp plugin
from ama.core.plugins.auxiliary import Cupp

# Auxliary base class
from ama.core.modules.base import Auxiliary

# debugged - date: Mar 4 2021
class CuppDownload(Auxiliary):
    """
    Cupp - Download wordlists
    """
    DESCRIPTION = "Cupp - Download huge wordlists"
    MNAME = "auxiliary/wordlists/cupp_download"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = """
    Download a wordlist from http://ftp.funet.fi/pub/unix/security/passwd/crack/dictionaries/
    """
    REFERENCES = [
        "https://www.hackingarticles.in/comprehensive-guide-on-cupp-a-wordlist-generating-tool/",
        "https://github.com/Mebus/cupp"
    ]

    def __init__(self):
        """
        Initialization of Cupp - Download wordlists
        """

        auxiliary_options = {
            'quiet': Argument(quiet, True, "Don't print cupp's fancy banner")
        }
        init_options = {
            'mname': CuppDownload.MNAME,
            'author': CuppDownload.AUTHOR,
            'description': CuppDownload.DESCRIPTION,
            'fulldescription': CuppDownload.FULLDESCRIPTION,
            'references': CuppDownload.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self):
        """
        Execution of Cupp interactive mode
        """
        try:
            self.no_empty_required_options()
            cupp = Cupp()
            cupp.download_wordlists(quiet = self.options['quiet'].value)

        except Exception as error:
            print_failure(error)
