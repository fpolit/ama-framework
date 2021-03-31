#!/usr/bin/env python3
#
# cewl - auxiliary application (wordlists generator)
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
from ama.core.files import Path


class Cewl(Auxiliary):
    """
    Custom Word List generator
    """

    MAINNAME = "cewl"

    def __init__(self):
        super().__init__(["cewl.rb", "cewl"], version="v5.5.0")

    # add authentification and proxy options
    def spider(self, url:str, *,
               depth: int = 2, min_length: int = 3, offsite: bool = False,
               exclude: str = None, allowed: str = None, write: str = None,
               lowercase: bool = False, with_numbers: bool = False,
               convert_umlauts: bool = True, meta: bool = False, meta_file: str = None,
               email: bool = False, email_file: str = None, count: bool = False,
               verbose: bool = True, debug: bool = False):

        #import pdb; pdb.set_trace()

        try:
            permission = [os.R_OK]
            cewl_cmd = f"{self.main_exec} --depth {depth} --min_word_length {min_length}"

            if offsite:
                cewl_cmd += " --offsite"

            if exclude:
                Path.access(permission, exclude)
                cewl_cmd += f" --exclude {exclude}"

            if allowed:
                cewl_cmd += f" --allowed {allowed}"

            if write:
                Path.access(permission, write)
                cewl_cmd += f" --write {write}"

            if lowercase:
                cewl_cmd += " --lowercase"

            if with_numbers:
                cewl_cmd += " --with_numbers"

            if convert_umlauts:
                cewl_cmd += " --convert-umlauts"

            if meta:
                if meta_file:
                    Path.access(permission, meta_file)
                    cewl_cmd += f" --meta --meta_file {meta_file}"

                else:
                    raise Exception("meta option enable, but meta_file not supplied")

            if email:
                if email_file:
                    Path.access(permission, email_file)
                    cewl_cmd += f" --email --email_file {email_file}"
                else:
                    raise Exception("email option enable, but email_file not supplied")

            if count:
                cewl_cmd += " --count"

            if verbose:
                cewl_cmd += " --verbose"

            if debug:
                cewl_cmd += " --debug"

            cewl_cmd += f" {url}"

            print_status(f"Running: {cewl_cmd}")
            Bash.exec(cewl_cmd)

        except Exception as error:
            print_failure(error)
