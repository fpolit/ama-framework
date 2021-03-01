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

    def __init__(self, *, cracked_hash, hash_type=None, password, cracker):
        self.cracked_hash = cracked_hash
        self.hash_type = hash_type
        self.password = password
        self.cracker = cracker

    def getAttributes(self):
        """
        Return cracked_hash, hash_type, password and cracker attributes of CrackedHash
        """
        return [self.cracked_hash, self.hash_type, self.password, self.cracker.MAINNAME]
