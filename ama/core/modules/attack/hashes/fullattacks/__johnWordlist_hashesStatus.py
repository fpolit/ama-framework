#!/usr/bin/env python3
#
# wordlist attack using john with HashesStatus as post attack module
#
# date: Mar 24 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any
from ..john_wordlist import JohnWordlist


# name format: PREATTACK_ATTACK_POSTATTACK
# (if pre/post attack is null then _ replace its name)
# Here __JohnWordlist_HashesStatus means: preattack: null, attack: JohnWordlist, postattack: HashesStatus
class __JohnWordlist_HashesStatus(JohnWordlist):
    def __init__(self, init_options):
        super().__init__(**init_options)
        self.fulldescription = (
            """
            Perform wordlists attacks against hashes
            with john and at the end report the status of the hashes (cracked or not)
            """
        )

        # pre attack options

        # post attack options
        if self.selected_post_attack and 'hashes_file' in self.selected_post_attack.options:
            self.selected_post_attack.options['hashes_file'].value = self.options['hashes_file'].value

