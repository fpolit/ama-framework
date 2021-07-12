#!/usr/bin/env python3
#
# Strong Password generator - random-password-generator
#
# Status:
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

class PasswordGenerator(Auxiliary):
    """
    Strong Password Generator
    """
    DESCRIPTION = "Strong Passwords Generator"
    MNAME = "auxiliary/passwords/password_generator"
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

    def __init__(self, *,
                 min_length:int = 6,
                 max_length:int = 16,
                 min_uchars:int = 1,
                 min_lchars:int = 1,
                 min_digits:int = 1,
                 min_schars:int = 1):

        auxiliary_options = {
            'min_length': Argument(min_length, True, "Minimum password length", value_type=int),
            'max_length': Argument(max_length, True, "Minimum password length", value_type=int),
            'min_uppers': Argument(min_uchars, True, "Minimum number of upper characters", value_type=int),
            'min_lowers': Argument(min_lchars, True, "Minimum number of lower characters", value_type=int),
            'min_digits': Argument(min_digits, True, "Minimum number of digits", value_type=int),
            'min_specials': Argument(min_schars, True, "Minimum number of special characters", value_type=int),
            'exclude': Argument('', False, "Characters to exclude")
        }

        init_options = {
            'mname': PasswordGenerator.MNAME,
            'author': PasswordGenerator.AUTHOR,
            'description': PasswordGenerator.DESCRIPTION,
            'fulldescription': PasswordGenerator.FULLDESCRIPTION,
            'references': PasswordGenerator.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self, quiet=False):
        """
        Strong password generator - auxiliary module
        """
        #import pdb; pdb.set_trace()
        try:
            self.no_empty_required_options()

            password = RandomPasswordGenerator()

            password.minlen = self.options['min_length'].value
            password.maxlen = self.options['max_length'].value
            password.minuchars = self.options['min_uppers'].value
            password.minlchars = self.options['min_lowers'].value
            password.minnumbers = self.options['min_digits'].value
            password.minschars = self.options['min_specials'].value


            exclude = {
                'upper': '',
                'lower': '',
                'digits': '',
                'special': ''
                }

            for char in self.options['exclude'].value:
                if char in string.ascii_lowercase:
                    exclude['lower'] += char

                elif char in string.ascii_uppercase:
                    exclude['upper'] += char

                elif char in string.digits:
                    exclude['digits'] += char

                else:
                    exclude['special'] += char


            password.excludeuchars = exclude['upper']
            password.excludelchars = exclude['lower']
            password.excludenumbers = exclude['digits']
            password.excludeschars = exclude['special']

            passwd = password.generate()

            print_successful(f"Generated password: {ColorStr(passwd).StyleBRIGHT}")

            return passwd


        except Exception as error:
            print_failure(error)
