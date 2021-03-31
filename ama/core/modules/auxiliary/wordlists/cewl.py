#!/usr/bin/env python3
#
# Cewl - wordlist generator
#
# date: Mar 31 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from fineprint.status import print_failure

# Cupp plugin
from ama.core.plugins.auxiliary.wordlists import Cewl as Cewlplugin

# Auxliary base class
from ama.core.modules.base import (
    Auxiliary,
    Argument
)


# debugged - date: Mar 4 2021
class Cewl(Auxiliary):
    """
    Cewl - Custom Word List generator
    """
    DESCRIPTION = "Cewl - Custom Word List generator"
    MNAME = "auxiliary/wordlists/cewl"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Cewl spiders a given URL to a specified depth and return a wordlist
        """
    )

    REFERENCES = [
        "https://www.hackingarticles.in/comprehensive-guide-on-cewl-tool/",
        "https://github.com/fpolit/cewl"
    ]

    def __init__(self, *, url:str = None,
                 depth: int = 2, min_length: int = 3, offsite: bool = False,
                 exclude: str = None, allowed: str = None, write: str = None,
                 lowercase: bool = False, with_numbers: bool = False,
                 convert_umlauts: bool = True, meta: bool = False, meta_file: str = None,
                 email: bool = False, email_file: str = None, count: bool = False,
                 verbose: bool = True, debug: bool = False):
        """
        Initialization of Cewl
        """

        auxiliary_options = {
            "url": Argument(url, True, "The site to spider"),
            "depth": Argument(depth, True, "Depth to spider to"),
            "min_length": Argument(min_length, True, "Minimum word length"),
            "offsite": Argument(offsite, True, "Let the spider visit other sites"),
            "exclude": Argument(exclude, False, "A file containing a list of paths to exclude"),
            "allowed": Argument(allowed, False, "A regex pattern that path must match to be followed"),
            "write": Argument(write, False, "Write the output to the file"),
            "lowercase": Argument(lowercase, True, "Lowercase all parsed words"),
            "with_numbers": Argument(with_numbers, True, "Accept words with numbers in as well as just letters"),
            "convert_umlauts": Argument(convert_umlauts, True, "Convert common ISO-8859-1 (Latin-1) umlauts"),
            "meta": Argument(meta, False, "Include meta data"),
            "meta_file": Argument(meta_file, False, "Output file for meta data"),
            "email": Argument(email, False, "Include email addresses"),
            "email_file": Argument(email_file, False, "Output file for email addresses"),
            "count": Argument(count, True, "Show the count for each word found"),
            "verbose": Argument(verbose, True, "Verbose"),
            "debug": Argument(debug, False, "Extra debug information")
        }

        init_options = {
            'mname': Cewl.MNAME,
            'author': Cewl.AUTHOR,
            'description': Cewl.DESCRIPTION,
            'fulldescription': Cewl.FULLDESCRIPTION,
            'references': Cewl.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self, quiet:bool = False):
        """
        Execution of Cupp interactive mode
        """

        #import pdb; pdb.set_trace()
        try:
            self.no_empty_required_options()
            cewl = Cewlplugin()

            cewl.spider(self.options['url'].value,
                        depth = self.options['depth'].value,
                        min_length = self.options['min_length'].value,
                        offsite = self.options['offsite'].value,
                        exclude = self.options['exclude'].value,
                        allowed = self.options['allowed'].value,
                        write = self.options['write'].value,
                        lowercase = self.options['lowercase'].value,
                        with_numbers = self.options['with_numbers'].value,
                        convert_umlauts = self.options['convert_umlauts'].value,
                        meta = self.options['meta'].value,
                        meta_file = self.options['meta_file'].value,
                        email = self.options['email'].value,
                        email_file = self.options['email_file'].value,
                        count = self.options['count'].value,
                        verbose = self.options['verbose'].value,
                        debug = self.options['debug'].value,
                        )

            return self.options['write'].value

        except Exception as error:
            print_failure(error)


    def setv(self, option, value, quiet:bool = False):
        #import pdb; pdb.set_trace()
        super().setv(option, value, quiet=quiet)

        option = option.lower()
        if option  == "meta" and self.options["meta"].value:
            self.options["meta_file"].required = True

        if option  == "email" and self.options["email"].value:
            self.options["email_file"].required = True
