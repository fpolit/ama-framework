#!/usr/bin/env python3
#
# hash generator - hashlib
#
# Status:
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
import hashlib
from fineprint.status import print_failure, print_status, print_successful

# module.base imports
from ama.core.modules.base import (
    Auxiliary,
    Argument
)

import hashlib

class HashGenerator(Auxiliary):
    """

    """
    DESCRIPTION = "Hash Generator"
    MNAME = "auxiliary/hashes/hash_generator"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "abjoschevaro <acheva@uni.pe>"
    ]

    _algorithms_available = list(hashlib.algorithms_available)
    FULLDESCRIPTION = (
        f"""
        Generate hashes for a given text.
        Supported hash functions:
           {' '.join(_algorithms_available[:10])}
           {' '.join(_algorithms_available[10:])}
        """
    )

    REFERENCES = [
        "https://docs.python.org/3/library/hashlib.html"
    ]

    def __init__(self, *,
                 text: str = None):

        auxiliary_options = {
            'text': Argument(text, True, "Text to generate a hash", value_type=str),
            'hfunc': Argument(None, True, "Hash function", value_type=str),
            'output': Argument(None, False, "Output file", value_type=str)
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
        Hash generator - auxiliary module
        """
        #import pdb; pdb.set_trace()
        try:
            self.no_empty_required_options()

            print_status(f"Generating a {self.options['hfunc'].value} hash for '{self.options['text'].value}'")

            hash_algorithm = hashlib.new(self.options['hfunc'].value)
            hash_algorithm.update(bytes(self.options['text'].value, 'utf-8'))

            generated_hash = hash_algorithm.hexdigest()
            print_successful(f"Generated hash: {generated_hash}")

            if self.options['output'].value:
                with open(self.options['output'].value, 'w') as output:
                    output.write(f"{generated_hash}\n")

                print_successful(f"Hash was saved to {self.options['output'].value} file")

        except Exception as error:
            print_failure(error)