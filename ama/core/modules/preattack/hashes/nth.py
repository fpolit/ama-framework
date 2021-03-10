#!/usr/bin/env python3
#
# hash identifier - nth pre attack module
#
# implemetation - date: Mar 9 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from fineprint.status import print_failure

# module.base imports
from ama.core.modules.base import (
    PreAttack,
    Argument
)

# module.auxiliaries.hashes imports
from ama.core.modules.auxiliary.hashes import Nth as NthAuxiliary


class Nth(PreAttack):
    """
    name-that-hash pre attack
    """

    DESCRIPTION = "Nth - Hash Identifier"
    MNAME = "preattack/hashes/nth"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]

    FULLDESCRIPTION = (
        """
        Identify different types of hashes used to encrypt data
        and return valid Hashcat or John hashes types used to
        perform attacks with a password cracker
        """
    )

    REFERENCES = [
        "https://github.com/HashPals/Name-That-Hash"
    ]


    def __init__(self, *,
                 hashes: str = None,
                 hashcat: bool = True, john: bool = True,
                 base64: bool = False,
                 banner: bool = False, most_likely: bool = True):

        preattack_options = {
            'hashes': Argument(hashes, True, "Hashes to identify (hashes[split by commas] or hashes file)"),
            'most_likely': Argument(most_likely, True, "Show the most like hashes type"),
            'hashcat': Argument(hashcat, True, "Show corresponding Hashcat mode"),
            'john': Argument(john, True, "Show corresponding John hash format"),
            'base64': Argument(base64, True, "Decodes hashes in Base64 before identification"),
        }

        init_options = {
            'mname': Nth.MNAME,
            'author': Nth.AUTHOR,
            'description': Nth.DESCRIPTION,
            'fulldescription': Nth.FULLDESCRIPTION,
            'references': Nth.REFERENCES,
            'preattack_options': preattack_options,
            'slurm': None
        }

        super().__init__(**init_options)


    def run(self):
        """
        default method to tun nth pre attack
        """
        nth_auxiliary = NthAuxiliary(**self.preattack_options_values())
        hashes_identities = nth_auxiliary.run(quiet=True)

        return hashes_identities

