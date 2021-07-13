#!/usr/bin/env python3
#
# Strong Password generator - random-password-generator
#
# State: TESTED - date: Jul 13 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from password_generator import PasswordGenerator as RandomPasswordGenerator
import string


from ama.modules.base import Auxiliary

from ama.utils import Argument
from ama.utils.color import ColorStr
from ama.utils.fineprint import (
    print_failure,
    print_status,
    print_successful
)


class ShufflePassword(Auxiliary):
    """
    Password Generator (Shuffle Password)
    """
    DESCRIPTION = "Shuffle Passwords Generator"
    MNAME = "auxiliary/passwords/shuffle_password"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]

    FULLDESCRIPTION = (
        """

        """
    )

    REFERENCES = [
        "https://github.com/suryasr007/random-password-generator"
    ]

    def __init__(self, *, min_length:int = 8):

        auxiliary_options = {
            'LENGTH': Argument(min_length, True, "Minimum password length", value_type=int),
            'CHARSET': Argument(None, True, "Characters to shuffle"),
            'JOB_NAME': Argument('shuffle-passwd-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': ShufflePassword.MNAME,
            'authors': ShufflePassword.AUTHORS,
            'description': ShufflePassword.DESCRIPTION,
            'fulldescription': ShufflePassword.FULLDESCRIPTION,
            'references': ShufflePassword.REFERENCES,
            'auxiliary_options': auxiliary_options
        }

        super().__init__(**init_options)

    def run(self, quiet=False):
        """
        Strong password generator (Shuffle Passwords) - auxiliary module
        """
        #import pdb; pdb.set_trace()
        try:
            #self.no_empty_required_options()

            password = RandomPasswordGenerator()

            charset = self.options['CHARSET'].value
            length = self.options['LENGTH'].value
            passwd = password.shuffle_password(charset, length)

            print_successful(f"Generated password: {ColorStr(passwd).StyleBRIGHT}")

            return passwd


        except Exception as error:
            print_failure(error)
