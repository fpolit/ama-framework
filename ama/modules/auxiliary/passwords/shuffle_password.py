#!/usr/bin/env python3
#
# Strong Password generator - random-password-generator
#
# Status:
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from password_generator import PasswordGenerator as RandomPasswordGenerator
from fineprint.status import print_failure, print_status, print_successful
from fineprint.color import ColorStr
import string

# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

class ShufflePassword(Auxiliary):
    """
    Password Generator (Shuffle Password)
    """
    DESCRIPTION = "Shuffle Passwords Generator"
    MNAME = "auxiliary/passwords/shuffle_password"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
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
            'length': Argument(min_length, True, "Minimum password length", value_type=int),
            'charset': Argument(None, True, "Characters to shuffle")
        }

        init_options = {
            'mname': ShufflePassword.MNAME,
            'author': ShufflePassword.AUTHOR,
            'description': ShufflePassword.DESCRIPTION,
            'fulldescription': ShufflePassword.FULLDESCRIPTION,
            'references': ShufflePassword.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self, quiet=False):
        """
        Strong password generator (Shuffle Passwords) - auxiliary module
        """
        #import pdb; pdb.set_trace()
        try:
            self.no_empty_required_options()

            password = RandomPasswordGenerator()

            charset = self.options['charset'].value
            length = self.options['length'].value
            passwd = password.shuffle_password(charset, length)

            print_successful(f"Generated password: {ColorStr(passwd).StyleBRIGHT}")

            return passwd


        except Exception as error:
            print_failure(error)
