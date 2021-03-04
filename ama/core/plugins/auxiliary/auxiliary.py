#!/usr/bin/env python3
#
# Auxiliary  - main class to generate auxiliary applications (hashid, pack, pydictor, ...)
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from ..plugin import Plugin

class Auxiliary(Plugin):
    """
        Password Cracker (hash and credential cracker) - Main Password Cracker class
    """
    # Supported auxiliary plugins
    WORDLISTS  = ["pydictor", "cupp", "crunch"]
    HASHES  = ["nth", "sth", "hashid"]
    ANALYSIS = ["pack", "ppack", "pipal"]
    COMBINATOR = ["mixer"]

    def __init__(self, name, *, version=None, main_exec=None):
        super().__init__(name,
                         version = version,
                         main_exec = main_exec)

