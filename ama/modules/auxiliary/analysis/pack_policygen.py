#!/usr/bin/env python3
#
# pack policygen - Analyze and Generate password masks according to a password policy
#
# State: TESTED - date: Jul 13 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

# cmd2 import
import cmd2

from ama.modules.base import Auxiliary
from ama.plugins.auxiliary.analysis import Pack

from ama.utils import Argument
from ama.utils.fineprint import print_failure


class PackPolicygen(Auxiliary):
    """
    policygen (pack) - Masks generator
    """

    DESCRIPTION = "Masks generator according to a password policy"
    MNAME = "auxiliary/analysis/pack_policygen"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
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
                 show_masks:bool = True):

        auxiliary_options = {
            'OUTPUT': Argument(output, True, "File to save generated masks"),

            # mask filters
            'MIN_LENGTH': Argument(min_length, True, "Minimum password length", value_type=int),
            'MAX_LENGTH': Argument(max_length, True, "Maximum password length", value_type=int),

            'MIN_SPECIAL': Argument(min_special, False, "Minimum number of special characters", value_type=int),
            'MIN_UPPER': Argument(min_upper, False, "Minimum number of uppercase characters", value_type=int),
            'MIN_LOWER': Argument(min_lower, False, "Minimum number of lowercase characters", value_type=int),
            'MIN_DIGIT': Argument(min_digit, False, "Minimum number of digit", value_type=int),
            'MAX_SPECIAL': Argument(max_special, False, "Maximum number of special characters", value_type=int),
            'MAX_UPPER': Argument(max_upper, False, "Maximum number of uppercase characters", value_type=int),
            'MAX_DIGIT': Argument(max_digit, False, "Maximum number of digit", value_type=int),
            'MAX_LOWER': Argument(max_lower, False, "Maximum number of lowercase characters", value_type=int),

            # miscellaneous
            'SHOW_MASKS': Argument(show_masks, True, "Show matching mask", value_type=bool),
            'JOB_NAME': Argument('pack-policygen-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }


        init_options = {
            'mname': PackPolicygen.MNAME,
            'authors': PackPolicygen.AUTHORS,
            'description': PackPolicygen.DESCRIPTION,
            'fulldescription':  PackPolicygen.FULLDESCRIPTION,
            'references': PackPolicygen.REFERENCES,
            'auxiliary_options': auxiliary_options
        }

        super().__init__(**init_options)



    def run(self, quiet=False):

        #import pdb; pdb.set_trace()

        try:
            #self.no_empty_required_options()
            output = Pack.policygen(output = self.options['OUTPUT'].value,
                                    min_length = self.options['MIN_LENGTH'].value,
                                    max_length = self.options['MAX_LENGTH'].value,
                                    min_digit = self.options['MIN_DIGIT'].value,
                                    max_digit = self.options['MAX_DIGIT'].value,
                                    min_upper = self.options['MIN_UPPER'].value,
                                    max_upper = self.options['MAX_UPPER'].value,
                                    min_lower = self.options['MIN_LOWER'].value,
                                    max_lower = self.options['MAX_LOWER'].value,
                                    min_special = self.options['MIN_SPECIAL'].value,
                                    max_special = self.options['MAX_SPECIAL'].value,
                                    show_masks = self.options['SHOW_MASKS'].value,
                                    quiet = quiet)


            return output

        except Exception as error:
            print_failure(error)
