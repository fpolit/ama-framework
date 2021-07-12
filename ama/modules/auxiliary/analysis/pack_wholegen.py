#!/usr/bin/env python3
#
# wholegen pack - auxiliary/analysis/pack_wholegen ama module
#
# implementation -  date: Mar 7 2021
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
    AUTHOR = [
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
                 show_masks:bool = False, quiet: bool = False,
                 sorting = "optindex"):

        auxiliary_options = {
            'wordlist': Argument(wordlist, True, "Wordlist to analyze", value_type=str),
            'output': Argument(output, True, "File name to save generated masks and occurrence", value_type=str),
            'charsets': Argument(charsets, False, "Password charset filter (e.g. loweralpha,numeric)", value_type=str),
            'min_length': Argument(min_length, False, "Minimum password length", value_type=int),
            'max_length': Argument(max_length, False, "Maximum password length", value_type=int),
            'min_special': Argument(min_special, False, "Minimum number of special characters", value_type=int),
            'min_upper': Argument(min_upper, False, "Minimum number of uppercase characters", value_type=int),
            'min_lower': Argument(min_lower, False, "Minimum number of lowercase characters", value_type=int),
            'min_digit': Argument(min_digit, False, "Minimum number of digit", value_type=int),
            'max_special': Argument(max_special, False, "Maximum number of special characters", value_type=int),
            'max_upper': Argument(max_upper, False, "Maximum number of uppercase characters", value_type=int),
            'max_digit': Argument(max_digit, False, "Maximum number of digit", value_type=int),
            'max_lower': Argument(max_lower, False, "Maximum number of lowercase characters", value_type=int),
            'min_complexity': Argument(min_complexity, False, "Minimum complexity", value_type=int),
            'max_complexity': Argument(max_complexity, False, "Maximum complexity", value_type=int),
            'min_occurrence': Argument(min_occurrence, False, "Minimum occurrence", value_type=int),
            'max_occurrence': Argument(max_occurrence, False, "Maximum occurrence", value_type=int),
            'min_time': Argument(min_time, False, "Minimum mask runtime (seconds)", value_type=int),
            'max_time': Argument(max_time, False, "Maximum mask runtime (seconds)", value_type=int),
            'target_time': Argument(target_time, False, "Target time of all masks (seconds)", value_type=int),
            'sorting': Argument(sorting, True, "Mask sorting (<optindex|occurrence|complexity>)", value_type=str),
            'hiderare': Argument(hiderare, True, "Hide statistics lower than the supplied percent", value_type=int),
            'show_masks': Argument(show_masks, True, "Show matching mask", value_type=bool),
        }

        init_options = {
            'mname': PackWholegen.MNAME,
            'author': PackWholegen.AUTHOR,
            'description': PackWholegen.DESCRIPTION,
            'fulldescription':  PackWholegen.FULLDESCRIPTION,
            'references': PackWholegen.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)


    def run(self, quiet:bool = False):
        """
        Run auxiliary/analysis/PackWholegen module
        """

        #import pdb; pdb.set_trace()

        try:

            self.no_empty_required_options()

            if maskgen_sorting := self.options['sorting'].value:
                if maskgen_sorting not in Pack.MASKGEN_SORTING_MODES:
                    raise InvalidSortingMode(maskgen_sorting)

            if self.options['charsets'].value:
                charsets = [charset for charset in self.options['charsets'].value.split(',')]
            else:
                charsets = None

            Pack.wholegen(wordlist = self.options['wordlist'].value,
                          output = self.options['output'].value,
                          charsets = charsets,
                          minlength = self.options['min_length'].value,
                          maxlength = self.options['max_length'].value,
                          mindigit = self.options['min_digit'].value,
                          maxdigit = self.options['max_digit'].value,
                          minupper = self.options['min_upper'].value,
                          maxupper = self.options['max_upper'].value,
                          minlower = self.options['min_lower'].value,
                          maxlower = self.options['max_lower'].value,
                          minspecial = self.options['min_special'].value,
                          maxspecial = self.options['max_special'].value,
                          mincomplexity = self.options['min_complexity'].value,
                          maxcomplexity = self.options['max_complexity'].value,
                          minoccurrence = self.options['min_occurrence'].value,
                          maxoccurrence = self.options['max_occurrence'].value,
                          mintime = self.options['min_time'].value,
                          maxtime = self.options['max_time'].value,
                          target_time = self.options['target_time'].value,
                          sorting = self.options['sorting'].value,
                          hiderare = self.options['hiderare'].value,
                          showmasks = self.options['show_masks'].value,
                          quiet = quiet)

            output = self.options['output'].value
            return output

        except Exception as error:
            print_failure(error)


    def setv(self, option, value):
        #import pdb; pdb.set_trace()
        super().setv(option, value)

        option = option.lower()
        # attack ->  atack
        if option == "wordlist":
            output_file_name = os.path.basename(value) + ".masks"
            super().setv('output', output_file_name)
