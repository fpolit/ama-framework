#!/usr/bin/env python3
#
# wordlist attack using hashcat with hashid as pre attack module and hashStatus as post attack module
#
# Implemented - date: Apr 3 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any
from fineprint.status import (
    print_failure,
    print_status
)


from .hashid_hashcat_wordlist__ import HashID_HashcatWordlist__
from ama.core.modules.auxiliary.hashes import HashID
from ama.core.modules.auxiliary.hashes import HashesStatus
from ama.core.plugins.cracker import Hashcat
from ama.core.slurm import Slurm


# name format: PREATTACK_ATTACK_POSTATTACK
# (if pre/post attack is null then _ replace its name)
class HashID_HashcatWordlist_HashesStatus(HashID_HashcatWordlist__):
    def __init__(self, init_options = None):
        if init_options is None:
            init_options = {
                "pre_attack": HashID(),
                "post_attack": HashesStatus()
            }

        super().__init__(init_options)
        self.selected_post_attack.options['cracker'].value = Hashcat.MAINNAME
        self.fulldescription = (
            """
            Perform wordlists attacks against hashes
            with hashcat using the most likely john hashes type parsed by hashid and report hashes status,
            also this parallel task can be submited in a cluster using Slurm
            """
        )

        # post attack options
        if self.selected_post_attack:
            self.selected_post_attack.options['hashes_file'].value = self.options['hashes_file'].value

    def setv(self, option, value, *, pre_attack: bool = False, post_attack: bool = False):
        #import pdb; pdb.set_trace()
        super().setv(option, value, pre_attack = pre_attack, post_attack = post_attack)

        option = option.lower()

        # attack -> post atack
        if option == "hashes_file":
            if self.selected_post_attack and not (pre_attack or post_attack):
                self.selected_post_attack.options['hashes_file'].value = self.options['hashes_file'].value

        # post atack -> attack
        if option == "hashes_file":
            if self.selected_pre_attack and post_attack:
                self.options['hashes_file'].value = self.selected_post_attack.options['hashes_file'].value
