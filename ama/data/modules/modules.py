#!/usr/bin/env python3
#
# ama supported modules
#
# date: Feb 18 2021
# john and hashcat attacks imports
#
# date: Feb 23 2021
# hydra attacks imports
#
# Maintainer: glozanoa <glozanoa@uni.pe>


### attacks modules imports
## attack/hashes modules imports

# john attacks imports
from ama.core.modules.attack.hashes import (
    JohnBenchmark,
    JohnWordlist,
    JohnIncremental,
    JohnSingle,
    JohnMasks,
    #JohnCombination,
    #JohnHybrid,
    JohnTest
)

# hashcat attacks imports
from ama.core.modules.attack.hashes import (
    HashcatBenchmark,
    HashcatWordlist,
    HashcatCombination,
    HashcatBruteForce,
    HashcatIncremental,
    HashcatMasks,
    HashcatHybrid
)

# sth
from ama.core.modules.attack.hashes import STH

## attack/services modules imports

#hydra attacks imports
from ama.core.modules.attack.services import (
    HydraWordlist
)

### auxiliary modules imports
## auxiliary/wordlists modules imports
from ama.core.modules.auxiliary.wordlists import (
    CuppInteractive,
    CuppRefine,
    CuppDownload,
    CuppAlecto,
    Cewl
)

## auxiliary/hashes modules imports
from ama.core.modules.auxiliary.hashes import (
    HashesStatus,
    HashID,
    Nth as NthAuxiliary
)

## auxiliary/analysis modules imports
from ama.core.modules.auxiliary.analysis import (
    PackStatsgen,
    PackMaskgen,
    PackPolicygen as PackPolicyAuxiliary,
    PackWholegen
)

amaAttackAuxiliariesModules = ["preattack", "postattack"]
amaModulesTypes = ["attack", "auxiliary", *amaAttackAuxiliariesModules]
amaModulesSubtypes = ["analysis", "wordlists", "hashes"]

# attack modules (hashes and services)
attackModules = {
    ## attack/hash modules
    # john attacks

    f"{JohnBenchmark.MNAME}": JohnBenchmark,
    f"{JohnWordlist.MNAME}": JohnWordlist,
    f"{JohnIncremental.MNAME}": JohnIncremental,
    f"{JohnSingle.MNAME}": JohnSingle,
    f"{JohnMasks.MNAME}": JohnMasks,
    #f"{JohnCombination.MNAME}": JohnCombination,
    #f"{JohnHybrid.MNAME}": JohnHybrid,
    f"{JohnTest.MNAME}": JohnTest,

    # hashcat attacks
    f"{HashcatBenchmark.MNAME}": HashcatBenchmark,
    f"{HashcatWordlist.MNAME}": HashcatWordlist,
    f"{HashcatCombination.MNAME}": HashcatCombination,
    f"{HashcatBruteForce.MNAME}": HashcatBruteForce,
    f"{HashcatIncremental.MNAME}": HashcatIncremental,
    f"{HashcatMasks.MNAME}": HashcatMasks,
    f"{HashcatHybrid.MNAME}": HashcatHybrid,

    # sth
    f"{STH.MNAME}": STH,

    ## attack/services modules
    # hydra attacks
    f"{HydraWordlist.MNAME}": HydraWordlist,
}

### auxiliary modules

## auxiliary/wordlists modules
auxiliaryWordlistModules = {
    f"{CuppInteractive.MNAME}": CuppInteractive,
    f"{CuppRefine.MNAME}": CuppRefine,
    f"{CuppDownload.MNAME}": CuppDownload,
    f"{CuppAlecto.MNAME}": CuppAlecto,
    f"{Cewl.MNAME}": Cewl
}

## auxiliary/hashes modules
auxiliaryHashesModules = {
    f"{HashesStatus.MNAME}": HashesStatus,
    f"{HashID.MNAME}": HashID,
    f"{NthAuxiliary.MNAME}": NthAuxiliary
}

## auxiliary/analysis modules
auxiliaryAnalysisModules = {
    f"{PackStatsgen.MNAME}": PackStatsgen,
    f"{PackMaskgen.MNAME}": PackMaskgen,
    f"{PackPolicyAuxiliary.MNAME}": PackPolicyAuxiliary,
    f"{PackWholegen.MNAME}": PackWholegen

}


amaModules = {
### attack modules
    **attackModules,

### pre/post attacks modules
    # **preAttackModules,
    # **postAttackModules,

### auxiliary modules
    ## auxiliary/wordlists modules
    **auxiliaryWordlistModules,

    ## auxiliary/hashes modules
    **auxiliaryHashesModules,

    ## auxiliary/analysis modules
    **auxiliaryAnalysisModules
}
