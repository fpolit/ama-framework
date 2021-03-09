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
    PolicyGen,
    WholeGen
)

from pack_ama.banner import (
    statsgen_banner,
    maskgen_banner,
    policygen_banner
)

class Pack(Auxiliary):
    """
    Identify the different types of hashes
    """

    MAINNAME = "pack"

    STATSGEN_BANNER = statsgen_banner()
    MASKGEN_BANNER = maskgen_banner()
    POLICYGEN_BANNER = policygen_banner()


    MASKGEN_SORTING_MODES = ["optindex", "occurrence", "complexity"]

    def __init__(self):
        super().__init__(["pack"], version="v0.0.3", search_exec=False)


    #debugged - date: Mar 7 2021
    @staticmethod
    def statsgen(*, wordlist: str, output: str = None,
                 min_length:int = None, max_length: int = None,
                 simple_masks: List[str] = None, charsets: List[str] = None,
                 quiet: bool = True, hiderare: int = 0):

        #import pdb; pdb.set_trace()
        try:
            permission = [os.R_OK]
            Path.access(permission, wordlist)

            statsgen = StatsGen(wordlist = wordlist,
                                output = output,
                                minlength = min_length,
                                maxlength = max_length,
                                simplemasks = simple_masks,
                                charsets = charsets,
                                quiet = quiet,
                                hiderare = hiderare)


            if not quiet:
                print(Pack.STATSGEN_BANNER)

            print(f"[*] Analyzing passwords in {wordlist}")

            statsgen.generate_stats()
            statsgen.print_stats()

        except Exception as error:
            print_failure(error)



    def maskgen(*,
            statsgen_output: str, output: str,
            min_length: int = None, max_length: int = None,
            target_time: int = None, min_time:int = None, max_time:int = None,
            min_complexity: int = None, max_complexity: int = None,
            min_occurrence: int = None, max_occurrence: int = None,
            sorting:str = "optindex",
            check_masks: List[str] = None, check_masks_file: str = None,
            show_masks: bool = False, quiet: bool = True):

        #import pdb; pdb.set_trace()
        try:
            permission = [os.R_OK]
            Path.access(permission, statsgen_output)

            if not quiet:
                print(Pack.MASKGEN_BANNER)


            print(f"[*] Analyzing masks in {statsgen_output}")
            pps = 1000000000
            maskgen = MaskGen(
                target_time = target_time,
                output_file = output,
                minlength = min_length,
                maxlength = max_length,
                mintime = min_time,
                maxtime = max_time,
                mincomplexity = min_complexity,
                maxcomplexity = max_complexity,
                minoccurrence = min_occurrence,
                maxoccurrence = max_occurrence,
                showmasks = show_masks
            )

            print("[*] Using {:,d} keys/sec for calculations.".format(pps))

            # Load masks
            maskgen.loadmasks(statsgen_output)

            # Matching masks from the command-line
            if check_masks:
                print(f"[*] Checking coverage of the these masks [{', '.join(check_masks)}]")
                maskgen.getmaskscoverage(check_masks)

            # Matching masks from a file
            elif check_masks_file:
                checkmasksfile = open(check_masks_file, 'r')
                print("[*] Checking coverage of masks in [%s]" % check_masks_file)
                maskgen.getmaskscoverage(checkmasksfile)

            else:# Printing masks in a file
                print("[*] Sorting masks by their [%s]." % sorting)
                maskgen.generate_masks(sorting)

        except Exception as error:
            print_failure(error)


    #debugged - date: Mar 7 2021
    @staticmethod
    def policygen( *,
               output: str = None,
               min_length:int = None, max_length:int = None, min_digit:int = None, max_digit: int = None,
               min_upper:int = None, max_upper:int = None, min_lower:int = None, max_lower:int = None,
               min_special:int = None, max_special:int = None,
               show_masks:bool = False, quiet:bool = True):

        #import pdb; pdb.set_trace()
        #Print program header
        if not quiet:
            print(policygen_banner())

        policygen = PolicyGen(output = output,
                              min_length = min_length,
                              max_length = max_length,
                              min_digit = min_digit,
                              max_digit = max_digit,
                              min_upper = min_upper,
                              max_upper = max_upper,
                              min_lower = min_lower,
                              max_lower = max_lower,
                              min_special = min_special,
                              max_special = max_special,
                              show_masks = show_masks)

        print("[*] Generating masks.")
        policygen.generate_masks()
        if output:
            print("[*] Saving generated masks to [%s]" % output)


    @staticmethod
    def wholegen(*,
                 wordlist: str, output: str,
                 charsets: List[str] = None,
                 minlength: int      = None, maxlength: int    = None,
                 mindigit:int        = None, maxdigit:int      = None,
                 minupper:int        = None, maxupper:int      = None,
                 minlower:int        = None, maxlower:int      = None,
                 minspecial:int      = None, maxspecial:int    = None,
                 mincomplexity:int   = None, maxcomplexity:int = None,
                 minoccurrence:int   = None, maxoccurrence:int = None,
                 mintime:int         = None, maxtime:int       = None,
                 target_time:int     = None,
                 hiderare: int       = 0,
                 showmasks:bool = False, quiet: bool = False,
                 sorting = "optindex"):

        #import pdb; pdb.set_trace()

        try:
            permission = [os.R_OK]
            Path.access(permission, wordlist)


            print(f"[*] Analyzing passwords in {wordlist}")

            whole = WholeGen(
                wordlist = wordlist,
                output = output,
                charsets = charsets,
                minlength = minlength,
                maxlength = maxlength,
                mindigit = mindigit,
                maxdigit = maxdigit,
                minupper = minupper,
                maxupper = maxupper,
                minlower = minlower,
                maxlower = maxlower,
                minspecial = minspecial,
                maxspecial = maxspecial,
                mincomplexity = mincomplexity,
                maxcomplexity = maxcomplexity,
                minoccurrence = minoccurrence,
                maxoccurrence = maxoccurrence,
                mintime = mintime,
                maxtime = maxtime,
                target_time = target_time,
                hiderare = hiderare,
                showmasks = showmasks,
                quiet = quiet)

            whole.full_analysis(sorting)


        except Exception as error:
            print_failure(error)
