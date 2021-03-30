#!/usr/bin/env python3
#
# wordlist attack using john with cupp-interactive as pre attack module and hashesStatus as post attack
#
# date: Mar 30 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any

from .cuppInteractive_johnWordlist__ import CuppInteractive_JohnWordlist__

# cracker imports
from ama.core.plugins.cracker import John

# slurm import
from ama.core.slurm import Slurm

#fineprint status
from fineprint.status import (
    print_failure,
    print_status
)

from ama.core.modules.auxiliary.wordlists import CuppInteractive
from ama.core.modules.auxiliary.hashes import HashesStatus

# name format: PREATTACK_ATTACK_POSTATTACK
# (if pre/post attack is null then _ replace its name)
class CuppInteractive_JohnWordlist_HashesStatus(CuppInteractive_JohnWordlist__):
    def __init__(self, init_options = None):

        if init_options is None:
            init_options = {
                "pre_attack": CuppInteractive(),
                "post_attack": HashesStatus()
            }

        super().__init__(**init_options)
        self.options['wordlist'].required = False
        self.fulldescription = (
            """
            Perform wordlist attacks against hashes
            with john using the generated wordlist by cupp-interactive and report hashes status ,
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
            if self.selected_post_attack and \
               not (pre_attack or post_attack):# and \
               #self.options['hashes_file'].value is not None:
                self.selected_post_attack.options['hashes_file'].value = self.options['hashes_file'].value

        # post atack -> attack
        if option == "hashes_file":
            if self.selected_post_attack and \
               post_attack: # and \
               #self.selected_post_attack.options['hashes_file'].value:
                self.options['hashes_file'].value = self.selected_post_attack.options['hashes_file'].value
