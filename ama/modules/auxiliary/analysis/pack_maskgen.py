#!/usr/bin/env python3
#
# maskgen pack - auxiliary/analysis/pack_maskgen ama module
#
# implementation -  date: Mar 7 2021
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
    AUTHOR = [
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
                 show_masks: bool = False, quiet: bool = True):

        auxiliary_options = {
            'stats': Argument(statsgen_output, True, "Statsgen output file"),
            'output': Argument(output, True, "File name to save generated masks"),

            # password filters
            'min_length': Argument(min_length, False, "Minimum password length"),
            'max_length': Argument(max_length, False, "Maximum password length"),
            'min_time': Argument(min_time, False, "Minimum mask runtime (seconds)"),
            'max_time': Argument(max_time, False, "Maximum mask runtime (seconds)"),
            'target_time': Argument(target_time, False, "Target time of all masks (seconds)"),
            'min_complexity': Argument(min_complexity, False, "Minimum complexity"),
            'max_complexity': Argument(max_complexity, False, "Maximum complexity"),
            'min_occurrence': Argument(min_occurrence, False, "Minimum occurrence"),
            'max_occurrence': Argument(max_occurrence, False, "Maximum occurrence"),
            'sorting': Argument(sorting, True, "Mask sorting (<optindex|occurrence|complexity>)"),
            'check_masks': Argument(check_masks, False, "Check mask coverage(e.g. ?u?l?d,?l?d?d)"),
            'check_masks_file': Argument(check_masks_file, False, "Check mask coverage in a file"),

            'show_masks': Argument(show_masks, True, "Show matching mask"),
        }


        init_options = {
            'mname': PackMaskgen.MNAME,
            'author': PackMaskgen.AUTHOR,
            'description': PackMaskgen.DESCRIPTION,
            'fulldescription':  PackMaskgen.FULLDESCRIPTION,
            'references': PackMaskgen.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    #debugged - date: Mar 7 2021
    def run(self, *, quiet:bool = False):

        #import pdb; pdb.set_trace()
        try:

            self.no_empty_required_options()

            if self.options['check_masks'].value:
                checkmasks = [checkmask for checkmask in self.options['check_masks'].value.split(',')]
            else:
                checkmasks = None

            if maskgen_sorting := self.options['sorting'].value:
                if maskgen_sorting not in Pack.MASKGEN_SORTING_MODES:
                    raise InvalidSortingMode(maskgen_sorting)


            Pack.maskgen(statsgen_output = self.options['stats'].value,
                         output = self.options['output'].value,
                         min_length = self.options['min_length'].value,
                         max_length = self.options['max_length'].value,
                         target_time = self.options['target_time'].value,
                         min_time = self.options['min_time'].value,
                         max_time = self.options['max_time'].value,
                         min_complexity = self.options['min_complexity'].value,
                         max_complexity = self.options['max_complexity'].value,
                         min_occurrence = self.options['min_occurrence'].value,
                         max_occurrence = self.options['max_occurrence'].value,
                         sorting = self.options['sorting'].value,
                         check_masks = checkmasks,
                         check_masks_file = self.options['check_masks'].value,
                         show_masks = self.options['show_masks'].value,
                         quiet = quiet)

            output = self.options['output'].value
            return output

        except Exception as error:
            print_failure(error)
