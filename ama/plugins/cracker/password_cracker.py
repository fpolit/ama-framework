#!/usr/bin/env python3
#
# PasswordCracker - main class to generate password crackers (john, hashcat, ...)
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from fineprint.status import print_failure
from ..plugin import Plugin
from .crackerException import InvalidPartition
from ama.core.files import (
    Path,
    line_counter
)

from math import ceil


class PasswordCracker(Plugin):
    """
        Password Cracker (hash and credential cracker) - Base class for Password Cracker
    """

    def __init__(self, name, *, version=None, main_exec=None):
        super().__init__(name,
                         version = version,
                         main_exec = main_exec)
