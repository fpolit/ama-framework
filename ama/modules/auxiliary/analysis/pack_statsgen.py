#!/usr/bin/env python3
#
# statsgen pack - auxiliary/analysis/pack_statsgen ama module
#
# implemented - date: Mar 5 2021
# debug - date: Mar 7 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import cmd2
from typing import List

from ama.modules.base import Auxiliary
from ama.plugins.auxiliary.analysis import Pack

from ama.utils import Argument
from ama.utils.fineprint import print_failure

class PackStatsgen(Auxiliary):
    """
    statsgen (pack) - Stats generator
    """

    DESCRIPTION = "Password Statistical Analysis Tool"
    MNAME = "auxiliary/analysis/pack_statsgen"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
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
                 hiderare:int = 0):

        auxiliary_options = {
            'WORDLIST': Argument(wordlist, True, "Wordlist to analyze"),
            'OUTPUT': Argument(output, False, "File name to save generated masks and occurrence"),

            # password filters
            'MIN_LENGTH': Argument(minlength, False, "Minimum password length", value_type=int),
            'MAX_LENGTH': Argument(maxlength, False, "Maximum password length", value_type=int),
            'CHARSETS': Argument(charsets, False, "Password charset filter (e.g. loweralpha,numeric)"),
            'SIMPLE_MASKS': Argument(simplemasks, False, "Password mask filter (e.g. stringdigit,allspecial)"),

            'HIDERARE': Argument(hiderare, True, "Hide statistics lower than the supplied percent", value_type=int),
            'JOB_NAME': Argument('pack-statsgen-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }


        init_options = {
            'mname': PackStatsgen.MNAME,
            'authors': PackStatsgen.AUTHORS,
            'description': PackStatsgen.DESCRIPTION,
            'fulldescription':  PackStatsgen.FULLDESCRIPTION,
            'references': PackStatsgen.REFERENCES,
            'auxiliary_options': auxiliary_options
        }

        super().__init__(**init_options)

    #debugged - date: Mar 7 2021
    def run(self, quiet:bool = False):

        #import pdb; pdb.set_trace()
        try:

            #self.no_empty_required_options()

            if self.options['CHARSETS'].value:
                charsets = self.options['CHARSETS'].value.split(',')
            else:
                charsets = None

            if self.options['SIMPLE_MASKS'].value:
                simple_masks = self.options['CHARSETS'].value.split(',')
            else:
                simple_masks = None

            Pack.statsgen(wordlist = self.options['WORDLIST'].value,
                          min_length = self.options['MIN_LENGTH'].value,
                          max_length = self.options['MAX_LENGTH'].value,
                          charsets = charsets,
                          simple_masks = simple_masks,
                          output = self.options['OUTPUT'].value,
                          hiderare = self.options['HIDERARE'].value,
                          quiet = quiet)

        except Exception as error:
            print(error) # print_failure
