#!/usr/bin/env python3
#
# hash generator - hashlib
#
# State: TESTED - date: Jul 13 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
import hashlib

from ama.modules.base import Auxiliary

from ama.utils import Argument
from ama.utils.fineprint import (
    print_failure,
    print_status,
    print_successful
)

import hashlib

class HashGenerator(Auxiliary):
    """

    """
    DESCRIPTION = "Hash Generator"
    MNAME = "auxiliary/hashes/hash_generator"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
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
            'TEXT': Argument(text, True, "Text to generate a hash", value_type=str),
            'HFUNC': Argument(None, True, "Hash function", value_type=str),
            'OUTPUT': Argument(None, False, "Output file", value_type=str),
            'JOB_NAME': Argument('hashgen-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': HashGenerator.MNAME,
            'authors': HashGenerator.AUTHORS,
            'description': HashGenerator.DESCRIPTION,
            'fulldescription': HashGenerator.FULLDESCRIPTION,
            'references': HashGenerator.REFERENCES,
            'auxiliary_options': auxiliary_options
        }

        super().__init__(**init_options)

    def run(self, quiet=False):
        """
        Hash generator - auxiliary module
        """
        #import pdb; pdb.set_trace()
        try:
            #self.no_empty_required_options()

            hash_func = self.options['HFUNC'].value
            text = self.options['TEXT'].value

            # print_status
            print(f"Generating a {hash_func} hash for '{text}'")

            hash_algorithm = hashlib.new(hash_func)
            hash_algorithm.update(bytes(text, 'utf-8'))

            generated_hash = hash_algorithm.hexdigest()
            print(f"Generated hash: {generated_hash}") # print_succesful

            output_file = self.options['OUTPUT'].value
            if output_file:
                with open(output_file, 'w') as output:
                    output.write(f"{generated_hash}\n")

                print(f"Hash was saved to {output_file} file") # print_succesful

        except Exception as error:
            print(error) # print_failure
