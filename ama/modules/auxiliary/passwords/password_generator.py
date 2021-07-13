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

class PasswordGenerator(Auxiliary):
    """
    Strong Password Generator
    """
    DESCRIPTION = "Strong Passwords Generator"
    MNAME = "auxiliary/passwords/password_generator"
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

    def __init__(self, *,
                 min_length:int = 6,
                 max_length:int = 16,
                 min_uchars:int = 1,
                 min_lchars:int = 1,
                 min_digits:int = 1,
                 min_schars:int = 1):

        auxiliary_options = {
            'MIN_LENGTH': Argument(min_length, True, "Minimum password length", value_type=int),
            'MAX_LENGTH': Argument(max_length, True, "Minimum password length", value_type=int),
            'MIN_UPPERS': Argument(min_uchars, True, "Minimum number of upper characters", value_type=int),
            'MIN_LOWERS': Argument(min_lchars, True, "Minimum number of lower characters", value_type=int),
            'MIN_DIGITS': Argument(min_digits, True, "Minimum number of digits", value_type=int),
            'MIN_SPECIALS': Argument(min_schars, True, "Minimum number of special characters", value_type=int),
            'EXCLUDE': Argument('', False, "Characters to exclude"),
            'JOB_NAME': Argument('passwd-gen-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': PasswordGenerator.MNAME,
            'authors': PasswordGenerator.AUTHORS,
            'description': PasswordGenerator.DESCRIPTION,
            'fulldescription': PasswordGenerator.FULLDESCRIPTION,
            'references': PasswordGenerator.REFERENCES,
            'auxiliary_options': auxiliary_options
        }

        super().__init__(**init_options)

    def run(self, quiet=False):
        """
        Strong password generator - auxiliary module
        """
        #import pdb; pdb.set_trace()
        try:
            #self.no_empty_required_options()

            password = RandomPasswordGenerator()

            password.minlen = self.options['MIN_LENGTH'].value
            password.maxlen = self.options['MAX_LENGTH'].value
            password.minuchars = self.options['MIN_UPPERS'].value
            password.minlchars = self.options['MIN_LOWERS'].value
            password.minnumbers = self.options['MIN_DIGITS'].value
            password.minschars = self.options['MIN_SPECIALS'].value


            exclude = {
                'upper': '',
                'lower': '',
                'digits': '',
                'special': ''
                }

            for char in self.options['EXCLUDE'].value:
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
