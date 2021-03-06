#!/usr/bin/env python3
#
# pack policygen - Analyze and Generate password masks according to a password policy
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
# from ama.core.auxiliary.analysis.pack import Pack

# class PackPolicygen(Auxiliary):
#     """
#     policygen (pack) - Masks generator
#     """

#     DESCRIPTION = "Masks generator according to a password policy"
#     MNAME = "auxiliary/analysis/pack_policygen"
#     AUTHOR = [
#         "glozanoa <glozanoa@uni.pe>"
#     ]
#     FULLDESCRIPTION = (
#         """
#         Analyze and Generate password masks according to a password policy
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

#         self.banner = ()
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
#             'mname': PackPolicygen.MNAME,
#             'author': PackPolicygen.AUTHOR,
#             'description': PackPolicygen.DESCRIPTION,
#             'fulldescription':  PackPolicygen.FULLDESCRIPTION,
#             'references': PackPolicygen.REFERENCES,
#             'auxiliary_options': auxiliary_options,
#             'slurm': None
#         }

#         super().__init__(**init_options)
