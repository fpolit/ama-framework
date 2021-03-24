#!/usr/bin/env python3
#
# Glue class glue preattack, attack and postattack modules
#
# date: Feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from collections import namedtuple

# base attacks modules

## hash attacks
from ama.core.modules.attack.hashes import (
    ## john attacks
    JohnBenchmark,
    JohnWordlist,
    JohnSingle,
    JohnIncremental,
    JohnMasks,
    JohnHybrid,

    ## hashcat attacks
    HashcatBenchmark,
    HashcatWordlist,
    HashcatCombination,
    HashcatBruteForce,
    HashcatIncremental,
    HashcatMasks,
)

# auxiliaries modules

## auxiliaries/hashes
from ama.core.modules.auxiliary.hashes import (
    HashID,
    Nth,
    HashesStatus
)

## auxiliaries/analysis
from ama.core.modules.auxiliary.analysis import (
    PackStatsgen,
    PackMaskgen,
    PackPolicygen,
    PackWholegen,
)

## auxiliaries/wordlists
from ama.core.modules.auxiliary.wordlists import (
    CuppInteractive,
    CuppRefine,
    CuppDownload,
    CuppAlecto,
)

# full attacks

## hash attacks
from ama.core.modules.attack.hashes import (
    HashId_JohnWordlist__,
)


fullAttack = namedtuple('fullAttack', ["preattack", "attack", "postattack"])

class Glue:
    full_attacks = {
            # HashID + hash cracker + None
            fullAttack(preattack=HashID, attack=JohnWordlist, postattack=None): HashId_JohnWordlist__,
            fullAttack(preattack=HashID, attack=JohnSingle, postattack=None): None,
            fullAttack(preattack=HashID, attack=JohnIncremental, postattack=None): None,
            fullAttack(preattack=HashID, attack=JohnMasks, postattack=None): None,
            fullAttack(preattack=HashID, attack=JohnHybrid, postattack=None): None,

            # HashID + hash cracker + HashesStatus
            fullAttack(preattack=HashID, attack=JohnWordlist, postattack=HashesStatus): None,
            fullAttack(preattack=HashID, attack=JohnSingle, postattack=HashesStatus): None,
            fullAttack(preattack=HashID, attack=JohnIncremental, postattack=HashesStatus): None,
            fullAttack(preattack=HashID, attack=JohnMasks, postattack=HashesStatus): None,
            fullAttack(preattack=HashID, attack=JohnHybrid, postattack=HashesStatus): None,

            # Nth + hash cracker + None
            fullAttack(preattack=Nth, attack=JohnWordlist, postattack=None): None,
            fullAttack(preattack=Nth, attack=JohnSingle, postattack=None): None,
            fullAttack(preattack=Nth, attack=JohnIncremental, postattack=None): None,
            fullAttack(preattack=Nth, attack=JohnMasks, postattack=None): None,
            fullAttack(preattack=Nth, attack=JohnHybrid, postattack=None): None,

            # Nth + hash cracker + HashesStatus
            fullAttack(preattack=Nth, attack=JohnWordlist, postattack=HashesStatus): None,
            fullAttack(preattack=Nth, attack=JohnSingle, postattack=HashesStatus): None,
            fullAttack(preattack=Nth, attack=JohnIncremental, postattack=HashesStatus): None,
            fullAttack(preattack=Nth, attack=JohnMasks, postattack=HashesStatus): None,
            fullAttack(preattack=Nth, attack=JohnHybrid, postattack=HashesStatus): None,

            # Cupp + hash cracker + None
            ## CuppInteractive + hash cracker + None
            fullAttack(preattack=Nth, attack=JohnWordlist, postattack=None): None,
            fullAttack(preattack=Nth, attack=JohnSingle, postattack=None): None,
            fullAttack(preattack=Nth, attack=JohnIncremental, postattack=None): None,
            fullAttack(preattack=Nth, attack=JohnMasks, postattack=None): None,
            fullAttack(preattack=Nth, attack=JohnHybrid, postattack=None): None,

            # Nth + hash cracker + HashesStatus
            fullAttack(preattack=Nth, attack=JohnWordlist, postattack=HashesStatus): None,
            fullAttack(preattack=Nth, attack=JohnSingle, postattack=HashesStatus): None,
            fullAttack(preattack=Nth, attack=JohnIncremental, postattack=HashesStatus): None,
            fullAttack(preattack=Nth, attack=JohnMasks, postattack=HashesStatus): None,
            fullAttack(preattack=Nth, attack=JohnHybrid, postattack=HashesStatus): None,



        }

    @staticmethod
    def get_full_attack(preattack=None, attack=None, postattack=None):
        """
        preattack: pre attack class or instance
        attack: attack class or instance
        postattack: post attack class or instance
        """
        #import pdb; pdb.set_trace()

        for full_attack, full_attack_class in Glue.full_attacks.items():
            if (full_attack.preattack == preattack or isinstance(preattack,full_attack.preattack)) and \
               (full_attack.attack == attack or isinstance(attack,full_attack.attack)) and \
               (full_attack.postattack == postattack or isinstance(postattack,full_attack.postattack)):
                return full_attack_class

        return None
