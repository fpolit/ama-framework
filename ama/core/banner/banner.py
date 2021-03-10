#!/usr/bin/env python3
#
# ama-framework banners
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import random
from ama.data.modules import (
    attackModules,
    preAttackModules,
    postAttackModules,
    auxiliaryWordlistModules,
    auxiliaryHashesModules,
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
        Availables Modules:

            Attack      : {len(attackModules)}
            PreAttack   : {len(preAttackModules)}
            PostAttack  : {len(postAttackModules)}

            Auxiliary :
                  Analysis     : {len(auxiliaryAnalysisModules)}
                  Wordlists    : {len(auxiliaryWordlistModules)}
                  Hashes       : {len(auxiliaryHashesModules)}
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
            """,
            r"""
                :::.     .        :    :::.
               ;;`;;    ;;,.    ;;;   ;;`;;
             ,[[ '[[,  [[[[, ,[[[[, ,[[ '[[,
            c$$$cc$$$c $$$$$$$$"$$$c$$$cc$$$c
             888   888,888 Y88" 888o888   888,
             YMM   ""` MMM  M'  "MMMYMM   ""`
            """,
            r"""
               ,gggg,gg   ,ggg,,ggg,,ggg,     ,gggg,gg
              dP"  "Y8I  ,8" "8P" "8P" "8,   dP"  "Y8I
             i8'    ,8I  I8   8I   8I   8I  i8'    ,8I
            ,d8,   ,d8b,,dP   8I   8I   Yb,,d8,   ,d8b,
            P"Y8888P"`Y88P'   8I   8I   `Y8P"Y8888P"`Y8
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
