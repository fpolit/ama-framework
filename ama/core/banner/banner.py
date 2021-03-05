#!/usr/bin/env python3
#
# ama-framework banners
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import random
from ama.data.modules import (
    attackModules,
    auxiliaryWordlistModules,
    auxiliaryHashesModules,
    auxiliaryCombinatortModules,
    auxiliaryAnalysisModules
)

from ama.core.version import get_version


class Banner:
    """
    Ama banner
    """
    AMA_INFO = "A specialized environment for the password cracking process"
    AMA_MODULES_INFO = (
        f"""
            Attack Modules: {len(attackModules)}
            Auxliary:
                Analysis Modules    : {len(auxiliaryAnalysisModules)}
                Wordlists Modules   : {len(auxiliaryWordlistModules)}
                Hashes Modules      : {len(auxiliaryHashesModules)}
                Combinator Modules  : {len(auxiliaryCombinatortModules)}
        """
    )
    AMA_VERSION = get_version()
    def __init__(self):
        self.banners = (
            r"""
              ____ _____ ___  ____ _
             / __ `/ __ `__ \/ __ `/
            / /_/ / / / / / / /_/ /
            \__,_/_/ /_/ /_/\__,_/
            """,
            r"""
            eeeee eeeeeee eeeee
            8   8 8  8  8 8   8
            8eee8 8e 8  8 8eee8
            88  8 88 8  8 88  8
            88  8 88 8  8 88  8
            """
        )

    @staticmethod
    def random():
        """
        return a random banner of ama
        """
        amaBanner = Banner()
        randomBanner = random.choice(amaBanner.banners)

        return (
        f"""
    {Banner.AMA_INFO}
        {randomBanner}
        VERSION: {Banner.AMA_VERSION}
        {Banner.AMA_MODULES_INFO}
        """
        )
