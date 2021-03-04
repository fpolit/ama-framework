#!/usr/bin/env python3
#
# maskgen pack - auxiliary/analysis/pack_maskgen ama module
#
# date: Feb 23 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# cmd2 import
import cmd2


# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

# pack import
from ama.core.auxiliary.analysis.pack import (
    MaskGen,
    getPackversion,
    getPackBanner
)



class PackMaskgen(Auxiliary):
    """
    maskgen (pack) - Masks generator
    """

    description = "maskgen (pack) - Masks generator"
    mname = "auxiliary/analysis/pack_maskgen"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    fulldescription = (
        """
        Genarate masks using maskgen (pack)
        submiting tasks in a cluster using Slurm
        """
    )

    def __init__(self, *,
                 output: str = None,
                 minlength: int = None, maxlength: int = None,
                 mintime: int = None, maxtime: int = None,
                 mincomplexity: int = None, maxcomplexity: int = None,
                 minoccurrence: int = None, maxoccurrence: int= None,
                 optindex: bool = False, occurrence: bool = False, complexity: bool = False,
                 checkmasks: List[str] = None, checkmasksfile: str = None,
                 targettime: int = None, showmasks: bool = False, pps: int = None, quiet: bool = False
                 slurm = None):

        self.banner = getPackBanner()
        auxiliary_options = {
            'output': output,

            # mask filters
            'min_length': minlength,
            'max_length': maxlength,
            'min_time': mintime,
            'max_time': maxtime,
            'min_complexity': mincomplexity,
            'max_complexity': maxcomplexity,
            'min_occurrence': minoccurrence,
            'max_occurrence': maxoccurrence,

            # mask sorting
            'optindex': optindex,
            'occurrence': occurrence,
            'complexity': complexity,

            # mask coverage
            'check_masks': checkmasks,
            'check_masksfile': checkmasksfile,

            # miscellaneous
            'target_time': targettime,
            'show_masks': showmasks,
            'pps': pps,
            'quiet': quiet
        }


        init_options = {
            'mname': mname,
            'author': author,
            'description': description,
            'fulldescription':  fulldescription,
            'auxiliaryOptions': auxiliaryOptions,
            'slurm': slurm
        }

        supper().__init__(**init_options)


    def run(self):
        """
        Masks generator (maskgen - pack)
        """
        pass
    #     # Print program header
    #     if not options.quiet:
    #         print header

    # if len(args) < 1:
    #     parser.error("no masks file specified! Please provide statsgen output.")
    #     exit(1)

    # print "[*] Analyzing masks in [%s]" % args[0]

    # maskgen = MaskGen()

    # # Settings
    # if options.target_time: maskgen.target_time = options.target_time
    # if options.output_masks:
    #     print "[*] Saving generated masks to [%s]" % options.output_masks
    #     maskgen.output_file = open(options.output_masks, 'w')

    # # Filters
    # if options.minlength:     maskgen.minlength     = options.minlength
    # if options.maxlength:     maskgen.maxlength     = options.maxlength
    # if options.mintime:       maskgen.mintime       = options.mintime
    # if options.maxtime:       maskgen.maxtime       = options.maxtime
    # if options.mincomplexity: maskgen.mincomplexity = options.mincomplexity
    # if options.maxcomplexity: maskgen.maxcomplexity = options.maxcomplexity
    # if options.minoccurrence: maskgen.minoccurrence = options.minoccurrence
    # if options.maxoccurrence: maskgen.maxoccurrence = options.maxoccurrence

    # # Custom
    # if options.customcharset1len: maskgen.customcharset1len = options.customcharset1len
    # if options.customcharset2len: maskgen.customcharset2len = options.customcharset2len
    # if options.customcharset3len: maskgen.customcharset3len = options.customcharset3len
    # if options.customcharset4len: maskgen.customcharset4len = options.customcharset4len

    # # Misc
    # if options.pps: maskgen.pps = options.pps
    # if options.showmasks: maskgen.showmasks = options.showmasks

    # print "[*] Using {:,d} keys/sec for calculations.".format(maskgen.pps)

    # # Load masks
    # for arg in args:
    #     maskgen.loadmasks(arg)

    # # Matching masks from the command-line
    # if options.checkmasks:
    #     checkmasks = [m.strip() for m in options.checkmasks.split(',')]
    #     print "[*] Checking coverage of the these masks [%s]" % ", ".join(checkmasks)
    #     maskgen.getmaskscoverage(checkmasks)

    # # Matching masks from a file
    # elif options.checkmasks_file:
    #     checkmasks_file = open(options.checkmasks_file, 'r')
    #     print "[*] Checking coverage of masks in [%s]" % options.checkmasks_file
    #     maskgen.getmaskscoverage(checkmasks_file)

    # # Printing masks in a file
    # else:
    #     # Process masks according to specified sorting algorithm
    #     if options.occurrence:
    #         sorting_mode = "occurrence"
    #     elif options.complexity:
    #         sorting_mode = "complexity"
    #     else:
    #         sorting_mode = "optindex"

    #     print "[*] Sorting masks by their [%s]." % sorting_mode
    #     maskgen.generate_masks(sorting_mode)
