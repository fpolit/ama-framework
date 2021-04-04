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
    HashesStatus,
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
    Cewl
)

# full attacks

## hash attacks
from ama.core.modules.attack.hashes import (
    HashID_JohnWordlist__,
    HashID_JohnMasks__,
    HashID_JohnSingle__,
    Nth_JohnWordlist__,
    PackMaskgen_JohnMasks__,
    PackWholegen_JohnMasks__,
    PackPolicygen_JohnMasks__,
    CuppInteractive_JohnWordlist__,
    Cewl_JohnWordlist__,
    CuppRefine_JohnWordlist__,
    __JohnWordlist_HashesStatus as None_JohnWordlist_HashesStatus,

    HashID_JohnWordlist_HashesStatus,
    HashID_JohnMasks_HashesStatus,
    HashID_JohnSingle_HashesStatus,
    Nth_JohnWordlist_HashesStatus,
    PackMaskgen_JohnMasks_HashesStatus,
    PackWholegen_JohnMasks_HashesStatus,
    PackPolicygen_JohnMasks_HashesStatus,
    CuppInteractive_JohnWordlist_HashesStatus,
    CuppRefine_JohnWordlist_HashesStatus,
)


fullAttack = namedtuple('fullAttack', ["preattack", "attack", "postattack"])

class Glue:
    full_attacks = {
        # None + hash cracker + None
        # fullAttack(preattack=None,
        #            attack=JohnBenchmark,
        #            postattack=None): JohnBenchmark,

        # fullAttack(preattack=None,
        #            attack=JohnWordlist,
        #            postattack=None): JohnWordlist,

        # fullAttack(preattack=None,
        #            attack=JohnSingle,
        #            postattack=None): JohnSingle,

        # fullAttack(preattack=None,
        #            attack=JohnMasks,
        #            postattack=None): JohnMasks,

        # None + hash cracker + HashesStatus
        fullAttack(preattack=None,
                   attack=JohnWordlist,
                   postattack=HashesStatus): None_JohnWordlist_HashesStatus, # debugged - date: Mar 30 2021

        # fullAttack(preattack=None,
        #            attack=JohnSingle,
        #            postattack=HashesStatus): None,

        # fullAttack(preattack=None,
        #            attack=JohnIncremental,
        #            postattack=HashesStatus): None,

        # fullAttack(preattack=None,
        #            attack=JohnMasks,
        #            postattack=HashesStatus): None,

        # fullAttack(preattack=None,
        #            attack=JohnHybrid,
        #            postattack=HashesStatus): None,


        # HashID + hash cracker + None
        fullAttack(preattack=HashID,
                   attack=JohnWordlist,
                   postattack=None): HashID_JohnWordlist__, # debugged - date: Mar 30 2021

        fullAttack(preattack=HashID,
                   attack=JohnSingle,
                   postattack=None): HashID_JohnSingle__, # debugged - date Apr 3 2021

        # fullAttack(preattack=HashID,
        #            attack=JohnIncremental,
        #            postattack=None): None,

        fullAttack(preattack=HashID,
                   attack=JohnMasks,
                   postattack=None): HashID_JohnMasks__,

        # fullAttack(preattack=HashID,
        #            attack=JohnHybrid,
        #            postattack=None): None,

        # HashID + hash cracker + HashesStatus
        fullAttack(preattack=HashID,
                   attack=JohnWordlist,
                   postattack=HashesStatus): HashID_JohnWordlist_HashesStatus, # debugged - date: Mar 30 2021

        fullAttack(preattack=HashID,
                   attack=JohnSingle,
                   postattack=HashesStatus): HashID_JohnSingle_HashesStatus, # debugged - date: Apr 3 2021

        # fullAttack(preattack=HashID,
        #            attack=JohnIncremental,
        #            postattack=HashesStatus): None,

        fullAttack(preattack=HashID,
                   attack=JohnMasks,
                   postattack=HashesStatus): HashID_JohnMasks_HashesStatus,

        # fullAttack(preattack=HashID,
        #            attack=JohnHybrid,
        #            postattack=HashesStatus): None,

        # Nth + hash cracker + None
        fullAttack(preattack=Nth,
                   attack=JohnWordlist, postattack=None): Nth_JohnWordlist__, # debugged - date: Mar 30 2021

        # fullAttack(preattack=Nth,
        #            attack=JohnSingle,
        #            postattack=None): None,

        # fullAttack(preattack=Nth,
        #            attack=JohnIncremental,
        #            postattack=None): None,

        # fullAttack(preattack=Nth,
        #            attack=JohnMasks,
        #            postattack=None): None,

        # fullAttack(preattack=Nth,
        #            attack=JohnHybrid,
        #            postattack=None): None,

        # Nth + hash cracker + HashesStatus
        fullAttack(preattack=Nth,
                   attack=JohnWordlist,
                   postattack=HashesStatus): Nth_JohnWordlist_HashesStatus, # debugged - date: Mar 30 2021

        # fullAttack(preattack=Nth,
        #            attack=JohnSingle,
        #            postattack=HashesStatus): None,

        # fullAttack(preattack=Nth,
        #            attack=JohnIncremental,
        #            postattack=HashesStatus): None,

        # fullAttack(preattack=Nth,
        #            attack=JohnMasks,
        #            postattack=HashesStatus): None,

        # fullAttack(preattack=Nth,
        #            attack=JohnHybrid,
        #            postattack=HashesStatus): None,

        # Cupp + hash cracker + None
        fullAttack(preattack=CuppInteractive,
                   attack=JohnWordlist,
                   postattack=None): CuppInteractive_JohnWordlist__, # debugged - date: Mar 30 2021

        fullAttack(preattack=CuppRefine,
                   attack=JohnWordlist,
                   postattack=None): CuppRefine_JohnWordlist__, # debugged - date: Mar 30 2021

        fullAttack(preattack=CuppInteractive,
                   attack=JohnWordlist,
                   postattack=HashesStatus): CuppInteractive_JohnWordlist_HashesStatus, # debugged - date: Mar 30 2021

        fullAttack(preattack=CuppRefine,
                   attack=JohnWordlist,
                   postattack=HashesStatus): CuppRefine_JohnWordlist_HashesStatus, # debugged - date: Mar 30 2021

        # fullAttack(preattack=CuppInteractive,
        #            attack=JohnSingle,
        #            postattack=None): None,

        # fullAttack(preattack=CuppInteractive,
        #            attack=JohnIncremental,
        #            postattack=None): None,

        # fullAttack(preattack=CuppInteractive,
        #            attack=JohnMasks,
        #            postattack=None): None,

        # fullAttack(preattack=CuppInteractive,
        #            attack=JohnHybrid,
        #            postattack=None): None,

        # Pack + hash cracker + None
        fullAttack(preattack=PackMaskgen,
                   attack=JohnMasks,
                   postattack=None): PackMaskgen_JohnMasks__, # debugged - date: Mar 30 2021

        fullAttack(preattack=PackWholegen,
                   attack=JohnMasks,
                   postattack=None): PackWholegen_JohnMasks__, # debugged - date: Mar 30 2021

        fullAttack(preattack=PackPolicygen,
                   attack=JohnMasks,
                   postattack=None): PackPolicygen_JohnMasks__,

        fullAttack(preattack=PackMaskgen,
                   attack=JohnMasks,
                   postattack=HashesStatus): PackMaskgen_JohnMasks_HashesStatus,

        fullAttack(preattack=PackWholegen,
                   attack=JohnMasks,
                   postattack=HashesStatus): PackWholegen_JohnMasks_HashesStatus,

        fullAttack(preattack=PackPolicygen,
                   attack=JohnMasks,
                   postattack=HashesStatus): PackPolicygen_JohnMasks_HashesStatus,

        # cewl + hash cracker + None
        fullAttack(preattack=Cewl,
                   attack=JohnWordlist,
                   postattack=None): Cewl_JohnWordlist__,
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
            if (full_attack.preattack == preattack or (full_attack.preattack and isinstance(preattack,full_attack.preattack))) and \
               (full_attack.attack == attack or (full_attack.attack and isinstance(attack,full_attack.attack))) and \
               (full_attack.postattack == postattack or (full_attack.postattack and isinstance(postattack,full_attack.postattack))):
                #import pdb; pdb.set_trace()
                return full_attack_class

        return None
