#!/usr/bin/env python3
#
# hash generator - nth
#
# Status:
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from fineprint.status import print_failure
#from typing import List

# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

# validator imports
#from ama.core.validator import Args
#from ama.core.files import Path

import hashlib

class HashGenerator(Auxiliary):
    """

    """
    DESCRIPTION = "Generate hashes"
    MNAME = "auxiliary/hashes/hash_generator"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "acher <acher@uni.pe>"
    ]

    FULLDESCRIPTION = (
        """
        Generate hashes given a word
        """
    )

    REFERENCES = [
        "https://docs.python.org/3/library/hashlib.html"
    ]

    def __init__(self, *,
                 word: str = None):

        auxiliary_options = {
            'word': Argument(word, True, "Word to generate a hash", value_type=str),
            'alg': Argument(word, True, "algorithm", value_type=str),
            'output': Argument(word, False, "Save in file", value_type=str)
        }

        init_options = {
            'mname': HashGenerator.MNAME,
            'author': HashGenerator.AUTHOR,
            'description': HashGenerator.DESCRIPTION,
            'fulldescription': HashGenerator.FULLDESCRIPTION,
            'references': HashGenerator.REFERENCES,
            'auxiliary_options': auxiliary_options,
            'slurm': None
        }

        super().__init__(**init_options)

    def run(self, quiet=False):
        """
        """
        #import pdb; pdb.set_trace()
        try:
            # CODE
            self.no_empty_required_options()
            print(f"word: {self.options['word'].value}, alg: {self.options['alg'].value}")
            print("hi chevar")

            if self.options['bye'].value:
                print("Bye Abraham")

            ###code added
            print_status(f"Generating a {args.hash_type} hash for '{args.text}'")

            hash_algorithm = hashlib.new(args.hash_type)
            hash_algorithm.update(bytes(args.text, 'utf-8'))

            generated_hash = hash_algorithm.hexdigest()
            print_successful(f"Generated hash: {generated_hash}")

            if args.output:
                with open(args.output, 'w') as output:
                    output.write(f"{generated_hash}\n")

                print_successful(f"Hash was saved to {args.output} file")

        except Exception as error:
            print_failure(error)
