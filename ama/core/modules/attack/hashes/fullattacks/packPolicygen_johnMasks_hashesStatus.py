#!/usr/bin/env python3
#
# masks attack using john with pack-maskgen as pre attack module and hashesstatus as post attack
#
# date: Mar 30 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any

from .packPolicygen_johnMasks__ import PackPolicygen_JohnMasks__

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
class PackPolicygen_JohnMasks_HashesStatus(PackPolicygen_JohnMasks__):
    def __init__(self, init_options):
        super().__init__(init_options)
        self.fulldescription = (
            """
            Perform masks attacks against hashes
            with john using the generated masks by pack-policygen and report hashes status ,
            also this parallel task can be submited in a cluster using Slurm
            """
        )

        # # post attack options
        # if self.selected_post_attack:
        #     self.selected_post_attack.options['hashes_file'].value = self.options['hashes_file'].value

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
