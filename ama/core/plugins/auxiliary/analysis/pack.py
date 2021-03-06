#!/usr/bin/env python3
#
# pack - Password Analysis and Cracking Kit
#
# implemetation - date: Mar 5 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os

from sbash import Bash
from fineprint.status import (
    print_failure,
    print_status,
    print_successful
)


from ama.core.plugins.auxiliary import Auxiliary

# core.file imports
from ama.core.files import Path

# validator
from ama.core.validator import Args

from typing import List

# pack-ama imports
from pack_ama import (
    StatsGen,
    MaskGen,
    PolicyGen
)

from pack_ama.banner import (
    statsgen_banner,
    maskgen_banner,
    policygen_banner
)

# class Pack(Auxiliary):
#     """
#     Identify the different types of hashes
#     """

#     MAINNAME = "pack"

#     STATSGEN_BANNER = statsgen_banner()
#     MASKGEN_BANNER = maskgen_banner()
#     POLICYGEN_BANNER = policygen_banner()

#     def __init__(self):
#         super().__init__(["pack"], version="v0.0.3", search_exec=False)

#     def statsgen(self, wordlist: str, *
#                  min_length:int, max_length: int,
#                  charset: List[str], somple_masks: List[str],
#                  output: str, hide_rare: bool, quiet: bool):

#         # Print program header
#         if not options.quiet:
#             print header

#     if len(args) != 1:
#         parser.error("no passwords file specified")
#         exit(1)

#     print "[*] Analyzing passwords in [%s]" % args[0]

#     statsgen = StatsGen()

#     if not options.minlength   == None: statsgen.minlength   = options.minlength
#     if not options.maxlength   == None: statsgen.maxlength   = options.maxlength
#     if not options.charsets    == None: statsgen.charsets    = [x.strip() for x in options.charsets.split(',')]
#     if not options.simplemasks == None: statsgen.simplemasks = [x.strip() for x in options.simplemasks.split(',')]

#     if options.hiderare: statsgen.hiderare = options.hiderare

#     if options.output_file:
#         print "[*] Saving advanced masks and occurrences to [%s]" % options.output_file
#         statsgen.output_file = open(options.output_file, 'w')

#     statsgen.generate_stats(args[0])
#     statsgen.print_stats()


#     def maskgen(self, statsgen_output: str, *,
#                 output: str,
#                 min_length: int, max_length: int, max_time: int,
#                 min_complexity: int, max_complexity: int, min_occurrence: int max_occurrence: int,
#                 optindex: bool, occurence: bool, complexity: bool,
#                 check_masks: List[str], check_masks_file: str, show_masks: bool,
#                 quiet: bool):

#         # Print program header
#         if not quiet:
#             print(maskgen_banner())


#         print "[*] Analyzing masks in [%s]" % args[0]

#         maskgen = MaskGen()

#         # Settings
#         if options.target_time: maskgen.target_time = options.target_time
#         if options.output_masks:
#             print "[*] Saving generated masks to [%s]" % options.output_masks
#             maskgen.output_file = open(options.output_masks, 'w')

#         # Filters
#         if options.minlength:     maskgen.minlength     = options.minlength
#         if options.maxlength:     maskgen.maxlength     = options.maxlength
#         if options.mintime:       maskgen.mintime       = options.mintime
#         if options.maxtime:       maskgen.maxtime       = options.maxtime
#         if options.mincomplexity: maskgen.mincomplexity = options.mincomplexity
#         if options.maxcomplexity: maskgen.maxcomplexity = options.maxcomplexity
#         if options.minoccurrence: maskgen.minoccurrence = options.minoccurrence
#         if options.maxoccurrence: maskgen.maxoccurrence = options.maxoccurrence

#         # Custom
#         if options.customcharset1len: maskgen.customcharset1len = options.customcharset1len
#         if options.customcharset2len: maskgen.customcharset2len = options.customcharset2len
#         if options.customcharset3len: maskgen.customcharset3len = options.customcharset3len
#         if options.customcharset4len: maskgen.customcharset4len = options.customcharset4len

#         # Misc
#         if options.pps: maskgen.pps = options.pps
#         if options.showmasks: maskgen.showmasks = options.showmasks

#         print("[*] Using {:,d} keys/sec for calculations.".format(maskgen.pps))

#         # Load masks
#         for arg in args:
#             maskgen.loadmasks(arg)

#         # Matching masks from the command-line
#         if check_masks:
#             checkmasks = [m.strip() for m in check_masks.split(',')]
#             print("[*] Checking coverage of the these masks [%s]" % ", ".join(checkmasks))
#             maskgen.getmaskscoverage(checkmasks)

#         # Matching masks from a file
# elif check_masks_file:
#     checkmasks_file = open(options.checkmasks_file, 'r')
#     print "[*] Checking coverage of masks in [%s]" % options.checkmasks_file
#     maskgen.getmaskscoverage(checkmasks_file)

#     # Printing masks in a file
#     else:
#         # Process masks according to specified sorting algorithm
#         if options.occurrence:
#             sorting_mode = "occurrence"
#         elif options.complexity:
#             sorting_mode = "complexity"
#         else:
#             sorting_mode = "optindex"

#         print "[*] Sorting masks by their [%s]." % sorting_mode
#         maskgen.generate_masks(sorting_mode)

#     def policygen(self, *,
#                   output: str, pps: int,
#                   showmasks: bool,
#                   min_length:int, max_length:int, min_digit:int max_digit: int,
#                   min_upper:int, max_upper:int, min_special:int, max_special:int,
#                   quiet:bool):
#         # Print program header
#     if not options.quiet:
#         print header

#     policygen = PolicyGen()

#     # Settings
#     if options.output_masks:
#         print "[*] Saving generated masks to [%s]" % options.output_masks
#         policygen.output_file = open(options.output_masks, 'w')


#     # Password policy
#     if options.minlength  != None: policygen.minlength  = options.minlength
#     if options.maxlength  != None: policygen.maxlength  = options.maxlength
#     if options.mindigit   != None: policygen.mindigit   = options.mindigit
#     if options.minlower   != None: policygen.minlower   = options.minlower
#     if options.minupper   != None: policygen.minupper   = options.minupper
#     if options.minspecial != None: policygen.minspecial = options.minspecial
#     if options.maxdigit   != None: policygen.maxdigit   = options.maxdigit
#     if options.maxlower   != None: policygen.maxlower   = options.maxlower
#     if options.maxupper   != None: policygen.maxupper   = options.maxupper
#     if options.maxspecial != None: policygen.maxspecial = options.maxspecial

#     # Misc
#     if options.pps: policygen.pps = options.pps
#     if options.showmasks: policygen.showmasks = options.showmasks

#     print "[*] Using {:,d} keys/sec for calculations.".format(policygen.pps)

#     # Print current password policy
#     print "[*] Password policy:"
#     print "    Pass Lengths: min:%d max:%d" % (policygen.minlength, policygen.maxlength)
#     print "    Min strength: l:%s u:%s d:%s s:%s" % (policygen.minlower, policygen.minupper, policygen.mindigit, policygen.minspecial)
#     print "    Max strength: l:%s u:%s d:%s s:%s" % (policygen.maxlower, policygen.maxupper, policygen.maxdigit, policygen.maxspecial)

#     print "[*] Generating [%s] masks." % ("compliant" if not options.noncompliant else "non-compliant")
#     policygen.generate_masks(options.noncompliant)






############ statsgen

#if __name__ == "__main__":

    # header  = "                       _ \n"
    # header += "     StatsGen %s   | |\n"  % VERSION
    # header += "      _ __   __ _  ___| | _\n"
    # header += "     | '_ \ / _` |/ __| |/ /\n"
    # header += "     | |_) | (_| | (__|   < \n"
    # header += "     | .__/ \__,_|\___|_|\_\\\n"
    # header += "     | |                    \n"
    # header += "     |_| iphelix@thesprawl.org\n"
    # header += "\n"

    #parser = OptionParser("%prog [options] passwords.txt\n\nType --help for more options", version="%prog "+VERSION)

    #filters = OptionGroup(parser, "Password Filters")
    # filters.add_option("--minlength", dest="minlength", type="int", metavar="8", help="Minimum password length")
    # filters.add_option("--maxlength", dest="maxlength", type="int", metavar="8", help="Maximum password length")
    # filters.add_option("--charset", dest="charsets", help="Password charset filter (comma separated)", metavar="loweralpha,numeric")
    # filters.add_option("--simplemask", dest="simplemasks",help="Password mask filter (comma separated)", metavar="stringdigit,allspecial")
    # parser.add_option_group(filters)

    # parser.add_option("-o", "--output", dest="output_file",help="Save masks and stats to a file", metavar="password.masks")
    # parser.add_option("--hiderare", action="store_true", dest="hiderare", default=False, help="Hide statistics covering less than 1% of the sample")

    # parser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False, help="Don't show headers.")
    # (options, args) = parser.parse_args()






############ maskgen

# if __name__ == "__main__":
#     parser = OptionParser("%prog pass0.masks [pass1.masks ...] [options]", version="%prog "+VERSION)

    #parser.add_option("-t", "--targettime",  dest="target_time",  type="int", metavar="86400", help="Target time of all masks (seconds)")
    #parser.add_option("-o", "--outputmasks", dest="output_masks", metavar="masks.hcmask",     help="Save masks to a file")

    #filters = OptionGroup(parser, "Individual Mask Filter Options")
    #filters.add_option("--minlength",     dest="minlength",     type="int", metavar="8",    help="Minimum password length")
    #filters.add_option("--maxlength",     dest="maxlength",     type="int", metavar="8",    help="Maximum password length")
    #filters.add_option("--mintime",       dest="mintime",       type="int", metavar="3600", help="Minimum mask runtime (seconds)")
    #filters.add_option("--maxtime",       dest="maxtime",       type="int", metavar="3600", help="Maximum mask runtime (seconds)")
    #filters.add_option("--mincomplexity", dest="mincomplexity", type="int", metavar="1",    help="Minimum complexity")
    #filters.add_option("--maxcomplexity", dest="maxcomplexity", type="int", metavar="100",  help="Maximum complexity")
    #filters.add_option("--minoccurrence", dest="minoccurrence", type="int", metavar="1",    help="Minimum occurrence")
    #filters.add_option("--maxoccurrence", dest="maxoccurrence", type="int", metavar="100",  help="Maximum occurrence")
    #parser.add_option_group(filters)

    #sorting = OptionGroup(parser, "Mask Sorting Options")
    #sorting.add_option("--optindex",   action="store_true", dest="optindex",   help="sort by mask optindex (default)", default=False)
    #sorting.add_option("--occurrence", action="store_true", dest="occurrence", help="sort by mask occurrence",         default=False)
    #sorting.add_option("--complexity", action="store_true", dest="complexity", help="sort by mask complexity",         default=False)
    #parser.add_option_group(sorting)

    #coverage = OptionGroup(parser, "Check mask coverage")
    # coverage.add_option("--checkmasks", dest="checkmasks", help="check mask coverage", metavar="?u?l?l?l?l?l?d,?l?l?l?l?l?d?d")
    # coverage.add_option("--checkmasksfile", dest="checkmasks_file", help="check mask coverage in a file", metavar="masks.hcmask")
    # parser.add_option_group(coverage)

    # parser.add_option("--showmasks", dest="showmasks",help="Show matching masks", action="store_true", default=False)

    # custom = OptionGroup(parser, "Custom charater set options")
    # custom.add_option("--custom-charset1-len", dest="customcharset1len", type="int", metavar="26",  help="Length of cutom character set 1")
    # custom.add_option("--custom-charset2-len", dest="customcharset2len", type="int", metavar="26",  help="Length of cutom character set 2")
    # custom.add_option("--custom-charset3-len", dest="customcharset3len", type="int", metavar="26",  help="Length of cutom character set 3")
    # custom.add_option("--custom-charset4-len", dest="customcharset4len", type="int", metavar="26",  help="Length of cutom character set 4")
    # parser.add_option_group(custom)

    # misc = OptionGroup(parser, "Miscellaneous options")
    # misc.add_option("--pps", dest="pps",help="Passwords per Second", type="int", metavar="1000000000")
    # misc.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False, help="Don't show headers.")
    # parser.add_option_group(misc)

    # (options, args) = parser.parse_args()


############ policygen


# if __name__ == "__main__":

#     header  = "                       _ \n"
#     header += "     PolicyGen %s  | |\n"  % VERSION
#     header += "      _ __   __ _  ___| | _\n"
#     header += "     | '_ \ / _` |/ __| |/ /\n"
#     header += "     | |_) | (_| | (__|   < \n"
#     header += "     | .__/ \__,_|\___|_|\_\\\n"
#     header += "     | |                    \n"
#     header += "     |_| iphelix@thesprawl.org\n"
#     header += "\n"

    # parse command line arguments
    #parser = OptionParser("%prog [options]\n\nType --help for more options", version="%prog "+VERSION)
    #parser.add_option("-o", "--outputmasks", dest="output_masks",help="Save masks to a file", metavar="masks.hcmask")
    #parser.add_option("--pps", dest="pps", help="Passwords per Second", type="int", metavar="1000000000")
    #parser.add_option("--showmasks", dest="showmasks", help="Show matching masks", action="store_true", default=False)
    #parser.add_option("--noncompliant", dest="noncompliant", help="Generate masks for noncompliant passwords", action="store_true", default=False)

    g#roup = OptionGroup(parser, "Password Policy", "Define the minimum (or maximum) password strength policy that you would like to test")
    #group.add_option("--minlength", dest="minlength", type="int", metavar="8", default=8, help="Minimum password length")
    #group.add_option("--maxlength", dest="maxlength", type="int", metavar="8", default=8, help="Maximum password length")
    #group.add_option("--mindigit",  dest="mindigit",  type="int", metavar="1", help="Minimum number of digits")
    #group.add_option("--minlower",  dest="minlower",  type="int", metavar="1", help="Minimum number of lower-case characters")
    #group.add_option("--minupper",  dest="minupper",  type="int", metavar="1", help="Minimum number of upper-case characters")
    #group.add_option("--minspecial",dest="minspecial",type="int", metavar="1", help="Minimum number of special characters")
    #group.add_option("--maxdigit",  dest="maxdigit",  type="int", metavar="3", help="Maximum number of digits")
    #group.add_option("--maxlower",  dest="maxlower",  type="int", metavar="3", help="Maximum number of lower-case characters")
    #group.add_option("--maxupper",  dest="maxupper",  type="int", metavar="3", help="Maximum number of upper-case characters")
    #group.add_option("--maxspecial",dest="maxspecial",type="int", metavar="3", help="Maximum number of special characters")
    #parser.add_option_group(group)

    #parser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False, help="Don't show headers.")

    #(options, args) = parser.parse_args()
