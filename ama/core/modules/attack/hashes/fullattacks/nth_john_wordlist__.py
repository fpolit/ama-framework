#!/usr/bin/env python3
#
# wordlist attack using john with nth as pre attack module
#
# date: Mar 29 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any

from ..john_wordlist import JohnWordlist

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
class Nth_JohnWordlist__(JohnWordlist):
    def __init__(self, init_options):
        #import pdb; pdb.set_trace()
        super().__init__(**init_options)

        self.options['hash_type'].required = False
        self.fulldescription = (
            """
            Perform wordlists attacks against hashes
            with john using the most likely john hashes type parsed by name-that-hash,
            also this parallel task can be submited in a cluster using Slurm
            """
        )

        # pre attack options
        if self.selected_pre_attack and 'hashes' in self.selected_pre_attack.options:
            self.selected_pre_attack.options['hashes'].value = self.options['hashes_file'].value

        # post attack options
        if self.selected_post_attack and 'hashes' in self.selected_post_attack.options:
            self.selected_post_attack.options['hashes'].value = self.options['hashes_file'].value

    def attack(self, local:bool = False, force: bool = False, pre_attack_output: Any = None):
        """
        Wordlist attack using John the Ripper with HashId as pre attack module

        Args:
           local (bool): if local is True run attack localy otherwise
                         submiting parallel tasks in a cluster using slurm
        """
        #import pdb; pdb.set_trace()
        try:
            if not force:
                self.no_empty_required_options(local)

            jtr = John()

            hashes_identities = self.most_probably_hash_identities(pre_attack_output)
            #import pdb; pdb.set_trace()
            jtr.wordlist_attack(hash_types = hashes_identities,
                                hashes_file = self.options['hashes_file'].value,
                                wordlist = self.options['wordlist'].value,
                                slurm = self.slurm,
                                local = local)

        except Exception as error:
            print_failure(error)


    # helper function to hashid preattack
    #preattacK_output format: [{QUERY_HASH : [{POSIBLE_HASH_IDENTITY}, ...]}, ...]
    def most_probably_hash_identities(self, preattack_output):
        #import pdb; pdb.set_trace()
        hash_type_frequency = {} # {john the ripper hash type: frequency, ...}
        for hashes_identities in preattack_output:
            for qhash, identities in hashes_identities.items():
                for identity in identities:
                    jtr_hash_type = identity['john']
                    if jtr_hash_type:
                        if jtr_hash_type in hash_type_frequency:
                            hash_type_frequency[jtr_hash_type] += 1
                        else:
                            hash_type_frequency[jtr_hash_type] = 0

        #import pdb; pdb.set_trace()
        #print(hash_type_frequency)
        most_likely_identities = sorted(hash_type_frequency.items(), key=lambda x: x[1], reverse=True)
        return [identity for identity, frequency in most_likely_identities]

    def setv(self, option, value, *, pre_attack: bool = False, post_attack: bool = False):
        #import pdb; pdb.set_trace()
        super().setv(option, value, pre_attack = pre_attack, post_attack = post_attack)

        option = option.lower()
        # attack -> pre atack
        if option == "hashes_file":
            if self.selected_pre_attack:
                self.selected_pre_attack.options['hashes'].value = self.options['hashes_file'].value

        # pre atack -> attack
        if option == "hashes":
            if self.selected_pre_attack:
                self.options['hashes_file'].value = self.selected_pre_attack.options['hashes'].value

