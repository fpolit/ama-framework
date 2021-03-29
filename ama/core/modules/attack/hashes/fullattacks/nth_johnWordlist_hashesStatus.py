#!/usr/bin/env python3
#
# wordlist attack using john with hashid as pre attack module
#
# date: Feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any

from .nth_john_wordlist__ import Nth_JohnWordlist__

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
class Nth_JohnWordlist_HashesStatus(Nth_JohnWordlist__):
    def __init__(self, init_options):
        super().__init__(init_options)
        self.fulldescription = (
            """
            Perform wordlists attacks against hashes
            with john using the most likely john hashes type parsed by nth and reporting hashes status,
            also this parallel task can be submited in a cluster using Slurm
            """
        )


