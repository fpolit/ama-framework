#!/usr/bin/env python3
#
# hashid - auxiliary application
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from ..auxiliary import Auxiliary

class HashID(Auxiliary):
    """
    Software to identify the different types of hashes
    """

    MAINNAME = "hashid"
    def __init__(self):
        super().__init__(["hashid"], version="v3.1.4")

    
