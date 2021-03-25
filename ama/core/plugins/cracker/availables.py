#!/usr/bin/env python3
#
# get availables crackers supported by ama
#
# date: Feb 25 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


from .john import John
from .hashcat import Hashcat
from .hydra import Hydra

SUPPORTED_CRACKERS = [John, Hashcat, Hydra]

def get_availables_crackers(crackers=SUPPORTED_CRACKERS):
    availables_crackers = []
    for cracker in crackers:
        cracker_instance = cracker()
        if cracker_instance.enable:
            availables_crackers.append(cracker)

    return availables_crackers
