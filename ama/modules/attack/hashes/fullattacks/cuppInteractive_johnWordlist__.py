#!/usr/bin/env python3
#
# wordlist attack using john with cupp-interactive as pre attack module
#
# date: Mar 30 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any

from ..john_wordlist import JohnWordlist
from ama.core.modules.auxiliary.wordlists import CuppInteractive

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
class CuppInteractive_JohnWordlist__(JohnWordlist):
    def __init__(self, init_options = None):

        if init_options is None:
            init_options = {
                "pre_attack": CuppInteractive(),
                "post_attack": None
            }

        super().__init__(**init_options)
        self.options['wordlist'].required = False
        self.fulldescription = (
            """
            Perform wordlists attacks against hashes
            with john using the generated wordlist by cupp-interactive,
            also this parallel task can be submited in a cluster using Slurm
            """
        )

        # pre attack options
        # if self.selected_pre_attack:
        #     self.selected_pre_attack.options['wordlist'].value = self.options['wordlist'].value

    # preattack output format:  {hash: [POSIBLE_IDENTITIES, ...], ...}
    def attack(self, local:bool = False, force: bool = False, pre_attack_output: Any = None):
        """
        Wordlist attack using John the Ripper with cupp-interactive as pre attack module

        Args:
           local (bool): if local is True run attack localy otherwise
                         submiting parallel tasks in a cluster using slurm
        """
        #import pdb; pdb.set_trace()
        try:
            if not force:
                self.no_empty_required_options(local)

            jtr = John()

            wordlist = pre_attack_output
            hash_types = self.options['hash_type'].value.split(',')
            jtr.wordlist_attack(hash_types = hash_types,
                                hashes_file = self.options['hashes_file'].value,
                                wordlist = wordlist,
                                slurm = self.slurm,
                                local = local)

        except Exception as error:
            print_failure(error)

    def setv(self, option, value, *, pre_attack: bool = False, post_attack: bool = False):
        #import pdb; pdb.set_trace()
        super().setv(option, value, pre_attack = pre_attack, post_attack = post_attack)

        # option = option.lower()
        # # attack -> pre atack
        # if option == "wordlist":
        #     if self.selected_pre_attack:
        #         self.selected_pre_attack.options['wordlist'].value = self.options['wordlist'].value

        # # pre atack -> attack
        # if option == "wordlist":
        #     if self.selected_pre_attack:
        #         self.options['wordlist'].value = self.selected_pre_attack.options['wordlist'].value
