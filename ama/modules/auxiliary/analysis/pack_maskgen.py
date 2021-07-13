#!/usr/bin/env python3
#
# maskgen pack - auxiliary/analysis/pack_maskgen ama module
#
# State: TESTED - date: Jul 13 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import cmd2
from fineprint.status import print_failure
from typing import List

# module.base imports
from ama.modules.base import Auxiliary
from ama.utils import Argument

# plugin imports
from ama.plugins.auxiliary.analysis import Pack

# exceptions imports
from .exceptions import InvalidSortingMode

class PackMaskgen(Auxiliary):
    """
    maskgen (pack) - Masks generator
    """

    DESCRIPTION = "Generate Password Masks"
    MNAME = "auxiliary/analysis/pack_maskgen"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Generate Password Masks using the generated stats of auxiliary/hashes/pack_statsgen module
        """
    )

    REFERENCES = [
        "https://github.com/iphelix/pack"
    ]

    def __init__(self, *,
                 statsgen_output: str = None, output: str = None,
                 min_length: int = None, max_length: int = None,
                 target_time: int = None, min_time:int = None, max_time:int = None,
                 min_complexity: int = None, max_complexity: int = None,
                 min_occurrence: int = None, max_occurrence: int = None,
                 sorting:str = "optindex",
                 check_masks: List[str] = None, check_masks_file: str = None,
                 show_masks: bool = True, quiet: bool = True):

        auxiliary_options = {
            'STATS': Argument(statsgen_output, True, "Statsgen output file"),
            'OUTPUT': Argument(output, True, "File name to save generated masks"),

            # password filters
            'MIN_LENGTH': Argument(min_length, False, "Minimum password length", value_type=int),
            'MAX_LENGTH': Argument(max_length, False, "Maximum password length", value_type=int),
            'MIN_TIME': Argument(min_time, False, "Minimum mask runtime (seconds)", value_type=int),
            'MAX_TIME': Argument(max_time, False, "Maximum mask runtime (seconds)", value_type=int),
            'TARGET_TIME': Argument(target_time, False, "Target time of all masks (seconds)", value_type=int),
            'MIN_COMPLEXITY': Argument(min_complexity, False, "Minimum complexity", value_type=int),
            'MAX_COMPLEXITY': Argument(max_complexity, False, "Maximum complexity", value_type=int),
            'MIN_OCCURRENCE': Argument(min_occurrence, False, "Minimum occurrence", value_type=int),
            'MAX_OCCURRENCE': Argument(max_occurrence, False, "Maximum occurrence", value_type=int),
            'SORTING': Argument(sorting, True, "Mask sorting (<optindex|occurrence|complexity>)"),
            'CHECK_MASKS': Argument(check_masks, False, "Check mask coverage(e.g. ?u?l?d,?l?d?d)"),
            'CHECK_MASKS_FILE': Argument(check_masks_file, False, "Check mask coverage in a file"),

            'SHOW_MASKS': Argument(show_masks, True, "Show matching mask", value_type=bool),
            'JOB_NAME': Argument('pack-maskgen-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }


        init_options = {
            'mname': PackMaskgen.MNAME,
            'authors': PackMaskgen.AUTHORS,
            'description': PackMaskgen.DESCRIPTION,
            'fulldescription':  PackMaskgen.FULLDESCRIPTION,
            'references': PackMaskgen.REFERENCES,
            'auxiliary_options': auxiliary_options
        }

        super().__init__(**init_options)

    #debugged - date: Mar 7 2021
    def run(self, quiet:bool = False):

        #import pdb; pdb.set_trace()
        try:

            #self.no_empty_required_options()

            if self.options['CHECK_MASKS'].value:
                checkmasks = [checkmask for checkmask in self.options['CHECK_MASKS'].value.split(',')]
            else:
                checkmasks = None

            if maskgen_sorting := self.options['SORTING'].value:
                if maskgen_sorting not in Pack.MASKGEN_SORTING_MODES:
                    raise InvalidSortingMode(maskgen_sorting)


            Pack.maskgen(statsgen_output = self.options['STATS'].value,
                         output = self.options['OUTPUT'].value,
                         min_length = self.options['MIN_LENGTH'].value,
                         max_length = self.options['MAX_LENGTH'].value,
                         target_time = self.options['TARGET_TIME'].value,
                         min_time = self.options['MIN_TIME'].value,
                         max_time = self.options['MAX_TIME'].value,
                         min_complexity = self.options['MIN_COMPLEXITY'].value,
                         max_complexity = self.options['MAX_COMPLEXITY'].value,
                         min_occurrence = self.options['MIN_OCCURRENCE'].value,
                         max_occurrence = self.options['MAX_OCCURRENCE'].value,
                         sorting = self.options['SORTING'].value,
                         check_masks = checkmasks,
                         check_masks_file = self.options['CHECK_MASKS'].value,
                         show_masks = self.options['SHOW_MASKS'].value,
                         quiet = quiet)

            output = self.options['OUTPUT'].value
            return output

        except Exception as error:
            print_failure(error)
