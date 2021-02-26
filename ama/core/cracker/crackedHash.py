#!/usr/bin/env python3
#
# cracked hash class
#
# date: feb 25 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>


class CrackedHash:
    """
    Cracked hash by some password cracker
    """

    def __init__(self, *, crackedHash, hashType=None, password, cracker):
        self.crackedHash = crackedHash
        self.hashType = hahsType
        self.password = password
        self.cracker = cracker

    def getAttributes(self):
        """
        Return crackedHash, hashType, password and cracker attributes of CrackedHash
        """
        return [self.crackedHash, self.hashType, self.password, self.cracker]
