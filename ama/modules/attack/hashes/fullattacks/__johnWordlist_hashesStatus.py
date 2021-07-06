#!/usr/bin/env python3
#
# wordlist attack using john with HashesStatus as post attack module
#
# date: Mar 24 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any
from ama.core.plugins.cracker import John
from ..john_wordlist import JohnWordlist
from ama.core.modules.auxiliary.hashes import HashesStatus


# name format: PREATTACK_ATTACK_POSTATTACK
# (if pre/post attack is null then _ replace its name)
# Here __JohnWordlist_HashesStatus means: preattack: null, attack: JohnWordlist, postattack: HashesStatus
class __JohnWordlist_HashesStatus(JohnWordlist):
    def __init__(self, init_options=None):
        if init_options is None:
            init_options = {
                "pre_attack": None,
                "post_attack": HashesStatus()
            }

        super().__init__(**init_options)
        self.selected_post_attack.options['cracker'].value = John.MAINNAME
        self.fulldescription = (
            """
            Perform wordlists attacks against hashes
            with john and at the end report the status of the hashes (cracked or not)
            """
        )

        # post attack options
        self.selected_post_attack.options['hashes_file'].value = self.options['hashes_file'].value


    def setv(self, option, value, *, pre_attack: bool = False, post_attack: bool = False):
        #import pdb; pdb.set_trace()
        super().setv(option, value, pre_attack = pre_attack, post_attack = post_attack)

        option = option.lower()
        # attack -> post atack
        if option in ["hashes_file"]:
            if not (pre_attack or post_attack):
                super().setv(option, self.options[option].value, post_attack = True)

        # post atack -> attack
        if option in ["hashes_file"]:
            if post_attack:
                super().setv(option, self.selected_post_attack.options[option].value)
