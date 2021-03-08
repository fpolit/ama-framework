#!/usr/bin/env python3
#
# pack policygen - Analyze and Generate password masks according to a password policy
#
# date: Mar 5 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# cmd2 import
import cmd2

from fineprint.status import print_failure

# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

# plugin imports
from ama.core.plugins.auxiliary.analysis import Pack


class PackPolicygen(Auxiliary):
    """
    policygen (pack) - Masks generator
    """

    DESCRIPTION = "Masks generator according to a password policy"
    MNAME = "auxiliary/analysis/pack_policygen"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Analyze and Generate password masks according to a password policy
        """
    )

    REFERENCES = [
        "https://github.com/iphelix/pack"
    ]


    def __init__(self, *,
                 output: str = None,
                 min_length:int = None, max_length:int = None, min_digit:int = None, max_digit: int = None,
                 min_upper:int = None, max_upper:int = None, min_lower:int = None, max_lower:int = None,
                 min_special:int = None, max_special:int = None,
                 show_masks:bool = False, quiet:bool = True):

        auxiliary_options = {
            'output': Argument(output, True, "File to save generated masks"),

            # mask filters
            'min_length': Argument(min_length, True, "Minimum password length"),
            'max_length': Argument(max_length, True, "Maximum password length"),

            'min_special': Argument(min_special, False, "Minimum number of special characters"),
            'min_upper': Argument(min_upper, False, "Minimum number of uppercase characters"),
            'min_lower': Argument(min_lower, False, "Minimum number of lowercase characters"),
            'min_digit': Argument(min_digit, False, "Minimum number of digit"),
            'max_special': Argument(max_special, False, "Maximum number of special characters"),
            'max_upper': Argument(max_upper, False, "Maximum number of uppercase characters"),
            'max_digit': Argument(max_digit, False, "Maximum number of digit"),
            'max_lower': Argument(max_lower, False, "Maximum number of lowercase characters"),

            # miscellaneous
            'show_masks': Argument(show_masks, True, "Show matching mask"),
            'quiet': Argument(quiet, True, "Don't show headers")
        }


        init_options = {
            'mname': PackPolicygen.MNAME,
            'author': PackPolicygen.AUTHOR,
            'description': PackPolicygen.DESCRIPTION,
            'fulldescription':  PackPolicygen.FULLDESCRIPTION,
            'references': PackPolicygen.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)



    def run(self):

        #import pdb; pdb.set_trace()

        try:
            self.no_empty_required_options()
            Pack.policygen(output = self.options['output'].value,
                           min_length = self.options['min_length'].value,
                           max_length = self.options['max_length'].value,
                           min_digit = self.options['min_digit'].value,
                           max_digit = self.options['max_digit'].value,
                           min_upper = self.options['min_upper'].value,
                           max_upper = self.options['max_upper'].value,
                           min_lower = self.options['min_lower'].value,
                           max_lower = self.options['max_lower'].value,
                           min_special = self.options['min_special'].value,
                           max_special = self.options['max_special'].value,
                           show_masks = self.options['show_masks'].value,
                           quiet = self.options['quiet'].value)


        except Exception as error:
            print_failure(error)
