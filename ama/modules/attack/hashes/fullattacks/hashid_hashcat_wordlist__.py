#!/usr/bin/env python3
#
# wordlist attack using hashcat with hashid as pre attack module
#
# Implementation - date: Apr 3 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import Any
from fineprint.status import (
    print_failure,
    print_status
)


from ..hashcat_wordlist import HashcatWordlist
from ama.core.modules.auxiliary.hashes import HashID
from ama.core.files import Path
from ama.core.plugins.cracker import Hashcat
from ama.core.slurm import Slurm


class HashID_HashcatWordlist__(HashcatWordlist):
    def __init__(self, init_options = None):
        if init_options is None:
            init_options = {
                "pre_attack": HashID(),
                "post_attack": None
            }

        super().__init__(**init_options)
        self.options['hash_type'].required = False
        self.fulldescription = (
            """
            Perform wordlists attacks against hashes
            with hashcat using the most likely john hashes type parsed by hashid,
            also this parallel task can be submited in a cluster using Slurm
            """
        )

        # pre attack options
        if self.selected_pre_attack:
            self.selected_pre_attack.options['hashes'].value = self.options['hashes_file'].value
            self.selected_pre_attack.options['john'].value = False
            self.selected_pre_attack.options['hashcat'].value = True
            self.selected_pre_attack.options['extended'].value = False

    # preattack output format:  {hash: [POSIBLE_IDENTITIES, ...], ...}
    def attack(self, local:bool = False, force: bool = False, pre_attack_output: Any = None,
               db_status:bool = False, workspace:str = None, db_credential_file: Path = None,
               cracker_main_exec:Path = None, slurm_conf=None):
        """
        Wordlist attack using John the Ripper with HashId as pre attack module

        Args:
           local (bool): if local is True run attack localy otherwise
                         submiting parallel tasks in a cluster using slurm
        """
        #import pdb; pdb.set_trace()
        try:

            self.no_empty_required_options(local)

            if not local and slurm_conf:
                self.slurm.config = slurm_conf

            if cracker_main_exec:
                hc = Hashcat(hc_exec=cracker_main_exec)
            else:
                hc = Hashcat()

            hashes_identities = self.most_probably_hash_identities(pre_attack_output)
            wordlists = self.options['wordlist'].value.split(',')

            hc.wordlist_attack(hash_types = hashes_identities,
                               hashes_file = self.options['hashes_file'].value,
                               wordlists = wordlists,
                               slurm = self.slurm,
                               local = local,
                               db_status= db_status,
                               workspace= workspace,
                               db_credential_file=db_credential_file)

        except Exception as error:
            print_failure(error)

    # helper function to hashid preattack
    def most_probably_hash_identities(self, preattack_output):
        #import pdb; pdb.set_trace()
        hash_type_frequency = {} # {john the ripper hash type: frequency, ...}
        for qhash, modes in preattack_output.items():
            for hash_info in modes:
                hc_hash_type = hash_info.hashcat
                if hc_hash_type:
                    if hc_hash_type in hash_type_frequency:
                        hash_type_frequency[hc_hash_type] += 1
                    else:
                        hash_type_frequency[hc_hash_type] = 0

        most_likely_identities = sorted(hash_type_frequency.items(), key=lambda x: x[1], reverse=True)
        return [identity for identity, frequency in most_likely_identities]


    def setv(self, option, value, *, pre_attack: bool = False, post_attack: bool = False):
        #import pdb; pdb.set_trace()
        super().setv(option, value, pre_attack = pre_attack, post_attack = post_attack)

        option = option.lower()
        # attack -> pre atack
        if option in ["hashes_file"]:
            if not (pre_attack or post_attack):
                if option == "hashes_file":
                    pre_attack_option = "hashes"
                super().setv(pre_attack_option, self.options[option].value, pre_attack = True)

        # pre atack -> attack
        if option in ["hashes"]:
            if pre_attack:
                if option == "hashes":
                    attack_option = "hashes_file"
                super().setv(attack_option, self.selected_pre_attack.options[option].value)
