#!/usr/bin/env python3
#
# PPACK integrator
#
# Maintainer: Gustavo Lozano <glozanoa@uni.pe>


# base modules imports
from ..base.FilePath import FilePath


from sbash.core import Bash
from fineprint.status import print_failure, print_status

from collections import namedtuple

maskLength = namedtuple('maskLength', ['min', 'max'])
maskOccurrence = namedtuple('maskOccurrence', ['min', 'max'])
maskComplexity = namedtuple('maskComplexity', ['min', 'max'])

# mask Character Structure
lowerChar = namedtuple('lowerChar', ['min', 'max'])
upperChar = namedtuple('upperChar', ['min', 'max'])
digitChar = namedtuple('digitChar', ['min', 'max'])
specialChar = namedtuple('specialChar', ['min', 'max'])



class PPACK:
    SCS = ("loweralpha", "upperalpha", "numeric", "special", "alpha", "mixalphaspecial", "mixalphanum", "mixspecialnum", "mixall")
    ACS = ("alphaspecial", "loweralphaspecial", "upperalphaspecial", "specialalpha", "specialloweralpha",
           "specialupperalpha", "alphanum","loweralphanum", "upperalphanum", "specialnum", "numspecial")

    @staticmethod
    def statsgen(*, wordlist = None, output = None,
                 scs = [], acs = [],
                 length = maskLength(0, -1)):

        if output:
            statsgen_cmd = f"statsgen -o {output} --minlength {length.min} --maxlength {length.max}"

            # scs
            for simpleCharset in scs:
                if simpleCharset in PPACK.SCS:
                    statsgen_cmd += " --scs {simpleCharset}"
                else:
                    print_failure(f"Invalid SCS: {simpleCharset}")

            # acs
            for advCharset in acs:
                if advCharset in PPACK.ACS:
                    statsgen_cmd += " --acs {simpleCharset}"
                else:
                    print_failure(f"Invalid ACS: {advcharset}")


            print_status(f"Executing: {statsgen_cmd}")
            Bash.exec(statsgen_cmd)


        else:
            print_failure("No output file supplied!")


    @staticmethod
    def maskgen(*, stats = None, output = None,
                scs=[], acs=[],
                length = maskLength(0, -1),
                occurrence = maskOccurrence(0, -1),
                complexity = maskComplexity(0, -1),
                checkMasks = [], checkMasksFile = None):
        if checkMasks or checkMasksFile:
            # perform the test of coverage
            pass
        else:
            if stats and output:
                maskgen_cmd = f"maskgen -s {stats} -o {output}"
                maskgen_cmd += f" --minlength {length.min} --maxlength {length.max}"
                maskgen_cmd += f" --minoccurrence {occurrence.min} --maxoccurence {occurrence.max}"
                maskgen_cmd += f" --mincomplexity {complexity.min} --maxcomplexity {complexity.max}"

                # scs
                for simpleCharset in scs:
                    if simpleCharset in PPACK.SCS:
                        maskgen_cmd += " --scs {simpleCharset}"
                    else:
                        print_failure(f"Invalid SCS: {simpleCharset}")

                # acs
                for advCharset in acs:
                    if advCharset in PPACK.ACS:
                        maskgen_cmd += " --acs {simpleCharset}"
                    else:
                        print_failure(f"Invalid ACS: {advcharset}")


                print_status(f"Executing: {maskgen_cmd}")
                Bash.exec(maskgen_cmd)

            else:
                if stats:
                    print_failure("No output file supplied")
                else:
                    print_failure("No stats supplied")

    @staticmethod
    def policygen(*, output = None,
                  length = maskLength(0, 0),
                  lower = lowerChar(0, 0),
                  upper = upperChar(0, 0),
                  digit = digitChar(0, 0),
                  special = specialChar(0, 0)):
        if output:
            policygen_cmd = f"policygen -o {output}"
            policygen_cmd += f" --minlength {length.min} --maxlength {length.max}"
            policygen_cmd += f" --minlower {lower.min} --maxlower {lower.max}"
            policygen_cmd += f" --minupper {upper.min} --maxupper {upper.max}"
            policygen_cmd += f" --mindigit {digit.min} --maxdigit {digit.max}"
            policygen_cmd += f" --minspecial {special.min} --maxspecial {special.max}"

            print_status(f"Executing: {policygen_cmd}")
            Bash.exec(policygen_cmd)

        else:
            print_failure("No output file supplied")
