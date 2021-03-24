#!/usr/bin/env python3
#
# wordlist attack using john with hashid as pre attack module
#
# date: Feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any

from ama.core.modules.base import Attack

# cracker imports
from ama.core.plugins.cracker import John

# slurm import
from ama.core.slurm import Slurm

#fineprint status
from fineprint.status import (
    print_failure,
    print_status
)


# name format: PREATTACK_ATTACK_POSTATTACK
# (if pre/post attack is null then _ replace its name)
# Here HashId_JohnWordlist__ means: preattack: HashId, attack: JohnWordlist, postattack: null
class HashId_JohnWordlist__(Attack):
    def __init__(self, init_options):
        init_options['attack_options']['hash_type'].required = False
        init_options['fulldescription'] = (
            """
            Perform wordlists attacks against hashes
            with john using the most likely john hashes type parsed by hashid,
            also this parallel task can be submited in a cluster using Slurm
            """
        )
        super().__init__(**init_options)

    # preattack output format:  {hash: [POSIBLE_IDENTITIES, ...], ...}
    def attack(self, local:bool = False, force: bool = False, pre_attack_output: Any = None):
        """
        Wordlist attack using John the Ripper with HashId as pre attack module

        Args:
           local (bool): if local is True run attack localy otherwise
                         submiting parallel tasks in a cluster using slurm
        """

        import pdb; pdb.set_trace()
        try:
            if not force:
                self.no_empty_required_options(local)

            jtr = John()


            hashes_identities = self.most_probably_hash_identities(pre_attack_output)
            for hash_identity in hashes_identities:
                jtr.wordlist_attack(hash_type = hash_identity,
                                    hashes_file = self.options['hashes_file'].value,
                                    wordlist = self.options['wordlist'].value,
                                    slurm = None)

            # if local:

            # else:
            #     for qhash, hash_info in pre_attack_output.items():
            #         jtr.wordlist_attack(hash_type = self.options['hash_type'].value,
            #                             hashes_file = self.options['hashes_file'].value,
            #                             wordlist = self.options['wordlist'].value,
            #                             slurm = self.slurm)

        except Exception as error:
            print_failure(error)


    def most_probably_hash_identities(self, preattack_output):
        import pdb; pdb.set_trace()
        hash_type_frequency = {} # {john the ripper hash type: frequency, ...}
        for qhash, modes in preattack_output.items():
            for hash_info in modes:
                jtr_hash_type = hash_info.john
                if jtr_hash_type:
                    if jtr_hash_type in hash_type_frequency:
                        hash_type_frequency[jtr_hash_type] += 1
                    else:
                        hash_type_frequency[jtr_hash_type] = 0

        return dict(sorted(hash_type_frequency.items(), key=lambda x: x[1], reverse=True))
