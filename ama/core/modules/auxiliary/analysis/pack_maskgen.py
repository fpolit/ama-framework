#!/usr/bin/env python3
#
# maskgen pack - auxiliary/analysis/pack_maskgen ama module
#
# date: Mar 5 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# cmd2 import
import cmd2

# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

# pack import
# from ama.core.plugins.auxiliary.analysis import Pack


# class PackMaskgen(Auxiliary):
#     """
#     maskgen (pack) - Masks generator
#     """

#     DESCRIPTION = "Generate Password Masks"
#     MNAME = "auxiliary/analysis/pack_maskgen"
#     AUTHOR = [
#         "glozanoa <glozanoa@uni.pe>"
#     ]
#     FULLDESCRIPTION = (
#         """
#         Generate Password Masks using generated stats of auxiliary/hashes/pack_statsgen module
#         """
#     )

#     REFERENCES = [
#         "https://github.com/iphelix/pack"
#     ]

#     def __init__(self, *,
#                  output: str = None,
#                  minlength: int = None, maxlength: int = None,
#                  mintime: int = None, maxtime: int = None,
#                  mincomplexity: int = None, maxcomplexity: int = None,
#                  minoccurrence: int = None, maxoccurrence: int= None,
#                  optindex: bool = False, occurrence: bool = False, complexity: bool = False,
#                  checkmasks: List[str] = None, checkmasksfile: str = None,
#                  targettime: int = None, showmasks: bool = False, pps: int = None, quiet: bool = False):

#         self.banner = Pack.MASKGEN_BANNER
#         auxiliary_options = {
#             'output': output,

#             # mask filters
#             'min_length': minlength,
#             'max_length': maxlength,
#             'min_time': mintime,
#             'max_time': maxtime,
#             'min_complexity': mincomplexity,
#             'max_complexity': maxcomplexity,
#             'min_occurrence': minoccurrence,
#             'max_occurrence': maxoccurrence,

#             # mask sorting
#             'optindex': optindex,
#             'occurrence': occurrence,
#             'complexity': complexity,

#             # mask coverage
#             'check_masks': checkmasks,
#             'check_masksfile': checkmasksfile,

#             # miscellaneous
#             'target_time': targettime,
#             'show_masks': showmasks,
#             'pps': pps,
#             'quiet': quiet
#         }


#         init_options = {
#             'mname': PackMaskgen.MNAME,
#             'author': PackMaskgen.author,
#             'description': PackMaskgen.description,
#             'fulldescription':  PackMaskgen.fulldescription,
#             'references': PackMaskgen.REFERENCES,
#             'auxiliary_options': auxiliary_options,
#             'slurm': None
#         }

#         super().__init__(**init_options)


#     def run(self):
#         """
#         Masks generator (maskgen - pack)
#         """
#         pass
