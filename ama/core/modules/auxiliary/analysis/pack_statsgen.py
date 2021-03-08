#!/usr/bin/env python3
#
# statsgen pack - auxiliary/analysis/pack_statsgen ama module
#
# implemented - date: Mar 5 2021
# debug - date: Mar 7 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import cmd2
from fineprint.status import print_failure
from typing import List

# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

from ama.core.plugins.auxiliary.analysis import Pack


class PackStatsgen(Auxiliary):
    """
    statsgen (pack) - Stats generator
    """

    DESCRIPTION = "Password Statistical Analysis tool"
    MNAME = "auxiliary/analysis/pack_statsgen"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Generate statistics of a wordlist and generate masks that will be used by maskgen to generate masks
        """
    )

    REFERENCES = [
        "https://github.com/iphelix/pack"
    ]

    def __init__(self, *,
                 wordlist:str = None, output: str = None,
                 minlength: int = None, maxlength: int = None,
                 charsets: List[str] = None, simplemasks: List[str] = None,
                 hiderare:int = 0, quiet: bool = True):

        auxiliary_options = {
            'wordlist': Argument(wordlist, True, "Wordlist to analyze"),
            'output': Argument(output, False, "File name to save generated masks and occurrence"),

            # password filters
            'min_length': Argument(minlength, False, "Minimum password length"),
            'max_length': Argument(maxlength, False, "Maximum password length"),
            'charsets': Argument(charsets, False, "Password charset filter (e.g. loweralpha,numeric)"),
            'simple_masks': Argument(simplemasks, False, "Password mask filter (e.g.stringdigit,allspecial)"),

            'hiderare': Argument(hiderare, True, "Hide statistics lower than the supplied percent"),
            'quiet': Argument(quiet, True, "Don't show headers")
        }


        init_options = {
            'mname': PackStatsgen.MNAME,
            'author': PackStatsgen.AUTHOR,
            'description': PackStatsgen.DESCRIPTION,
            'fulldescription':  PackStatsgen.FULLDESCRIPTION,
            'references': PackStatsgen.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    #debugged - date: Mar 7 2021
    def run(self):

        #import pdb; pdb.set_trace()
        try:

            self.no_empty_required_options()

            if self.options['charsets'].value:
                charsets = [charset for charset in self.options['charsets'].value.split(',')]
            else:
                charsets = None

            if self.options['simple_masks'].value:
                simple_masks = [simplemask for simplemask in self.options['simple_masks'].value.split(',')]
            else:
                simple_masks = None

            Pack.statsgen(wordlist = self.options['wordlist'].value,
                          min_length = self.options['min_length'].value,
                          max_length = self.options['max_length'].value,
                          charsets = charsets,
                          simple_masks = simple_masks,
                          output = self.options['output'].value,
                          hiderare = self.options['hiderare'].value,
                          quiet = self.options['quiet'].value)

        except Exception as error:
            print_failure(error)
