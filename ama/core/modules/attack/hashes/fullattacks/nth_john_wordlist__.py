#!/usr/bin/env python3
#
# wordlist attack using john with nth as pre attack module
#
# date: Mar 29 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any
from fineprint.status import (
    print_failure,
    print_status
)


from ..john_wordlist import JohnWordlist
from ama.core.modules.auxiliary.hashes import Nth
from ama.core.plugins.cracker import John
from ama.core.slurm import Slurm
from ama.core.files import Path

# name format: PREATTACK_ATTACK_POSTATTACK
# (if pre/post attack is null then _ replace its name)
class Nth_JohnWordlist__(JohnWordlist):
    def __init__(self, init_options=None):
        #import pdb; pdb.set_trace()
        if init_options is None:
            init_options = {
                "pre_attack": Nth(),
                "post_attack": None
            }

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

    def attack(self, *,
               local:bool = False, force: bool = False, pre_attack_output: Any = None,
               db_status:bool = False, workspace:str = None, db_credential_file: Path = None):
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
                                local = local,
                                db_status= db_status,
                                workspace= workspace,
                                db_credential_file=db_credential_file)

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
        if option in ["hashes_file"]:
            if not (pre_attack or post_attack):
                pre_attack_option = option
                super().setv(pre_attack_option, self.options[option].value, pre_attack = True)

        # pre atack -> attack
        if option in ["hashes"]:
            if pre_attack:
                if option == "hashes":
                    attack_option = "hashes_file"
                super().setv(attack_option, self.selected_post_attack.options[option].value)
