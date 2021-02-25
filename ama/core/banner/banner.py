#!/usr/bin/env python3
#
# ama-framework banners
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import random

class Banners:
    """
    Ama banners
    """
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
        amaBanner = Banners()
        return random.choice(amaBanner.banners)
