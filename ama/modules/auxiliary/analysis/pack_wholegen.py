#!/usr/bin/env python3
#
# wholegen pack - auxiliary/analysis/pack_wholegen ama module
#
# implementation -  date: Mar 7 2021
# State: TESTED - date: Jul 13 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from fineprint.status import print_failure
from typing import List

# module.base imports
from ama.modules.base import Auxiliary
from ama.plugins.auxiliary.analysis import Pack

from ama.utils import Argument
from ama.utils.fineprint import print_failure

# exceptions imports
from .exceptions import InvalidSortingMode

class PackWholegen(Auxiliary):
    """
    wholegen (pack) - statsgen and maksgen
    """

    DESCRIPTION = "Analize Passwords and generate Masks"
    MNAME = "auxiliary/analysis/pack_wholegen"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Analyze a wordlist and generate password masks to use with a password cracker (hashcat or john)
        Perform the same work as statsgen and maskgen together
        """
    )

    REFERENCES = [
        "https://github.com/iphelix/pack"
    ]

    def __init__(self, *,
                 wordlist: str = None, output: str = None,
                 charsets: List[str] = None,
                 min_length: int      = None, max_length: int    = None,
                 min_digit:int        = None, max_digit:int      = None,
                 min_upper:int        = None, max_upper:int      = None,
                 min_lower:int        = None, max_lower:int      = None,
                 min_special:int      = None, max_special:int    = None,
                 min_complexity:int   = None, max_complexity:int = None,
                 min_occurrence:int   = None, max_occurrence:int = None,
                 min_time:int         = None, max_time:int       = None,
                 target_time:int     = None,
                 hiderare: int       = 0,
                 show_masks:bool = True, quiet: bool = False,
                 sorting = "optindex"):

        auxiliary_options = {
            'WORDLIST': Argument(wordlist, True, "Wordlist to analyze", value_type=str),
            'OUTPUT': Argument(output, True, "File name to save generated masks and occurrence", value_type=str),
            'CHARSETS': Argument(charsets, False, "Password charset filter (e.g. loweralpha,numeric)", value_type=str),
            'MIN_LENGTH': Argument(min_length, False, "Minimum password length", value_type=int),
            'MAX_LENGTH': Argument(max_length, False, "Maximum password length", value_type=int),
            'MIN_SPECIAL': Argument(min_special, False, "Minimum number of special characters", value_type=int),
            'MIN_UPPER': Argument(min_upper, False, "Minimum number of uppercase characters", value_type=int),
            'MIN_LOWER': Argument(min_lower, False, "Minimum number of lowercase characters", value_type=int),
            'MIN_DIGIT': Argument(min_digit, False, "Minimum number of digit", value_type=int),
            'MAX_SPECIAL': Argument(max_special, False, "Maximum number of special characters", value_type=int),
            'MAX_UPPER': Argument(max_upper, False, "Maximum number of uppercase characters", value_type=int),
            'MAX_DIGIT': Argument(max_digit, False, "Maximum number of digit", value_type=int),
            'MAX_LOWER': Argument(max_lower, False, "Maximum number of lowercase characters", value_type=int),
            'MIN_COMPLEXITY': Argument(min_complexity, False, "Minimum complexity", value_type=int),
            'MAX_COMPLEXITY': Argument(max_complexity, False, "Maximum complexity", value_type=int),
            'MIN_OCCURRENCE': Argument(min_occurrence, False, "Minimum occurrence", value_type=int),
            'MAX_OCCURRENCE': Argument(max_occurrence, False, "Maximum occurrence", value_type=int),
            'MIN_TIME': Argument(min_time, False, "Minimum mask runtime (seconds)", value_type=int),
            'MAX_TIME': Argument(max_time, False, "Maximum mask runtime (seconds)", value_type=int),
            'TARGET_TIME': Argument(target_time, False, "Target time of all masks (seconds)", value_type=int),
            'SORTING': Argument(sorting, True, "Mask sorting (<optindex|occurrence|complexity>)", value_type=str),
            'HIDERARE': Argument(hiderare, True, "Hide statistics lower than the supplied percent", value_type=int),
            'SHOW_MASKS': Argument(show_masks, True, "Show matching mask", value_type=bool),
            'JOB_NAME': Argument('pack-wholegen-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': PackWholegen.MNAME,
            'authors': PackWholegen.AUTHORS,
            'description': PackWholegen.DESCRIPTION,
            'fulldescription':  PackWholegen.FULLDESCRIPTION,
            'references': PackWholegen.REFERENCES,
            'auxiliary_options': auxiliary_options
        }

        super().__init__(**init_options)


    def run(self, quiet:bool = False):
        """
        Run auxiliary/analysis/PackWholegen module
        """

        #import pdb; pdb.set_trace()

        try:

            #self.no_empty_required_options()

            if maskgen_sorting := self.options['SORTING'].value:
                if maskgen_sorting not in Pack.MASKGEN_SORTING_MODES:
                    raise InvalidSortingMode(maskgen_sorting)

            if self.options['CHARSETS'].value:
                charsets = [charset for charset in self.options['CHARSETS'].value.split(',')]
            else:
                charsets = None

            Pack.wholegen(wordlist = self.options['WORDLIST'].value,
                          output = self.options['OUTPUT'].value,
                          charsets = charsets,
                          minlength = self.options['MIN_LENGTH'].value,
                          maxlength = self.options['MAX_LENGTH'].value,
                          mindigit = self.options['MIN_DIGIT'].value,
                          maxdigit = self.options['MAX_DIGIT'].value,
                          minupper = self.options['MIN_UPPER'].value,
                          maxupper = self.options['MAX_UPPER'].value,
                          minlower = self.options['MIN_LOWER'].value,
                          maxlower = self.options['MAX_LOWER'].value,
                          minspecial = self.options['MIN_SPECIAL'].value,
                          maxspecial = self.options['MAX_SPECIAL'].value,
                          mincomplexity = self.options['MIN_COMPLEXITY'].value,
                          maxcomplexity = self.options['MAX_COMPLEXITY'].value,
                          minoccurrence = self.options['MIN_OCCURRENCE'].value,
                          maxoccurrence = self.options['MAX_OCCURRENCE'].value,
                          mintime = self.options['MIN_TIME'].value,
                          maxtime = self.options['MAX_TIME'].value,
                          target_time = self.options['TARGET_TIME'].value,
                          sorting = self.options['SORTING'].value,
                          hiderare = self.options['HIDERARE'].value,
                          showmasks = self.options['SHOW_MASKS'].value,
                          quiet = quiet)

            output = self.options['OUTPUT'].value
            return output

        except Exception as error:
            print(error) # print_failure


    # def setv(self, option, value):

    #     #import pdb; pdb.set_trace()
    #     super().setv(option, value)

    #     option = option.lower()
    #     # attack ->  atack
    #     if option == "wordlist":
    #         output_file_name = os.path.basename(value) + ".masks"
    #         super().setv('output', output_file_name)
