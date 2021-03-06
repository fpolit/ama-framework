#!/usr/bin/env python3
#
# statsgen pack - auxiliary/analysis/pack_statsgen ama module
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


# class PackStatsgen(Auxiliary):
#     """
#     statsgen (pack) - Stats generator
#     """

#     DESCRIPTION = "Password Statistical Analysis tool"
#     MNAME = "auxiliary/analysis/pack_statsgen"
#     AUTHOR = [
#         "glozanoa <glozanoa@uni.pe>"
#     ]
#     FULLDESCRIPTION = (
#         """
#         Generate statistics of a wordlist and generate masks that will be used by maskgen to generate masks
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

#         self.banner = Pack.STATSGEN_BANNER
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
#             'mname': PackStatsgen.MNAME,
#             'author': PackStatsgen.AUTHOR,
#             'description': PackStatsgen.DESCRIPTION,
#             'fulldescription':  PackStatsgen.FULLDESCRIPTION,
#             'references': PackStatsgen.REFERENCES,
#             'auxiliary_options': auxiliary_options,
#             'slurm': None
#         }

#         super().__init__(**init_options)


#     def run(self):
#         # Args.notNone(self.wordlist)
#         # # Print program header
#         # if not self.quiet:
#         #     cmd2.Cmd.poutput(self.banner)

#         # cmd2.Cmd.poutput(f"[*] Analyzing passwords in {self.wordlist}")

#         # statsgen = StatsGen(**self.auxiliary)
#         # statsgen.generate_stats()
#         # statsgen.print_stats()
