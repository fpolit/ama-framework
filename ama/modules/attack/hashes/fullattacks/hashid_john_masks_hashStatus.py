#!/usr/bin/env python3
#
# wordlist attack using john with hashid as pre attack module and hashStatus as post attack module
#
# date: Apr 3 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any
from fineprint.status import (
    print_failure,
    print_status
)

from .hashid_john_masks__ import HashID_JohnMasks__
from ama.core.modules.auxiliary.hashes import HashID
from ama.core.modules.auxiliary.hashes import HashesStatus
from ama.core.files import Path
from ama.core.plugins.cracker import John
from ama.core.slurm import Slurm


# name format: PREATTACK_ATTACK_POSTATTACK
# (if pre/post attack is null then _ replace its name)
class HashID_JohnMasks_HashesStatus(HashID_JohnMasks__):
    def __init__(self, init_options = None):

        if init_options is None:
            init_options = {
                "pre_attack": HashID(),
                "post_attack": HashesStatus()
            }

        super().__init__(init_options)
        self.fulldescription = (
            """
            Perform masks attacks against hashes
            with john using the most likely john hashes type parsed by hashid and report hashes status,
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
