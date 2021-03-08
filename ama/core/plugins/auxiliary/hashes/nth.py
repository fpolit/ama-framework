#!/usr/bin/env python3
#
# nth - auxiliary application (hash identificator)
#
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os

from sbash import Bash
from fineprint.status import (
    print_failure,
    print_status,
    print_successful
)


from ama.core.plugins.auxiliary import Auxiliary

# core.file imports
from ama.core.files import Path

# name_that_hash imports
import name_that_hash as nth

class NTH(Auxiliary):
    """
    Identify different types of hashes
    """

    MAINNAME = "nth"
    def __init__(self):
        super().__init__(["nth"], version="v3.1.4", search_exec=False)

    def identify_hash(self,
                      query_hash: str, *,
                      hashcat: bool = True, john: bool = True,
                      base64: bool = False,
                      most_likely: bool = True):
        """
        Identify the type of the supplied hash
        """

        #import pdb; pdb.set_trace()

        nth.identify_hash(query_hash = query_hash,
                          base64 = base64,
                          accessible = most_likely,
                          john = john,
                          hashcat = hashcat,
                          show_banner=False)

    def identify_hashes(self,
                        hashes_file: str, *,
                        hashcat: bool = True, john: bool = True,
                        base64: bool = False,
                        most_likely: bool = True):
        """
        Identify the type of the supplied hashes
        """

        #import pdb; pdb.set_trace()

        if self.enable:

            try:
                permission = [os.R_OK]
                Path.access(permission, hashes_file)

                nth.identify_hashes(hashes_file = hashes_file,
                                    base64 = base64,
                                    accessible = most_likely,
                                    john = john,
                                    hashcat = hashcat,
                                    show_banner=False)



            except Exception as error:
                print_failure(error)

        else:
            print_failure("Auxliary plugin {self.main_name} is disable")
