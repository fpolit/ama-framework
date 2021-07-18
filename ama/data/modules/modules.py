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
from ama.modules.attack.hashes import (
    #JohnBenchmark,
    JohnWordlist,
    JohnMasks,
    JohnCombination
)
#     JohnIncremental,
#     JohnSingle,
#     #JohnHybrid,
# )

# # hashcat attacks imports
# from ama.modules.attack.hashes import (
#     HashcatBenchmark,
#     HashcatWordlist,
#     HashcatCombination,
#     HashcatBruteForce,
#     HashcatIncremental,
#     HashcatMasks,
#     HashcatHybrid
# )

# sth
#from ama.core.modules.attack.hashes import STH

## attack/services modules imports

#hydra attacks imports
# from ama.modules.attack.services import (
#     HydraWordlist
# )

### auxiliary modules imports
## auxiliary/wordlists modules imports
from ama.modules.auxiliary.wordlists import (
    CuppInteractive,
    CuppRefine,
    CuppDownload,
    CuppAlecto,
    HcutilsCombinator,
    HcutilsCombinator3,
    HcutilsCombipow,
    HcutilsMli2,
    HcutilsReqExclude,
    HcutilsReqInclude,
    HcutilsRli,
    HcutilsSplitlen
    #Cewl,
    #BopscrkInteractive,
    #BopscrkCombine
)

## auxiliary/hashes modules imports
from ama.modules.auxiliary.hashes import (
    #HashesStatus,
    HashID,
    Nth as NthAuxiliary,
    HashGenerator
)

## auxiliary/analysis modules imports
from ama.modules.auxiliary.analysis import (
    PackStatsgen,
    PackMaskgen,
    PackPolicygen as PackPolicyAuxiliary,
    PackWholegen
)

## auxiliary/passwords modules imports
from ama.modules.auxiliary.passwords import (
    PasswordGenerator,
    ShufflePassword
)


amaAttackAuxiliariesModules = ["preattack", "postattack"]
amaModulesTypes = ["attack", "auxiliary"]
amaModulesSubtypes = ["analysis", "wordlists", "hashes"]

# attack modules (hashes and services)
attackModules = {
    ## attack/hash modules
    # john attacks

    #f"{JohnBenchmark.MNAME}": JohnBenchmark,
    f"{JohnWordlist.MNAME}": JohnWordlist,
    # f"{JohnIncremental.MNAME}": JohnIncremental,
    # f"{JohnSingle.MNAME}": JohnSingle,
    f"{JohnMasks.MNAME}": JohnMasks,
    f"{JohnCombination.MNAME}": JohnCombination,
    # #f"{JohnHybrid.MNAME}": JohnHybrid,

    # # hashcat attacks
    # f"{HashcatBenchmark.MNAME}": HashcatBenchmark,
    # f"{HashcatWordlist.MNAME}": HashcatWordlist,
    # f"{HashcatCombination.MNAME}": HashcatCombination,
    # f"{HashcatBruteForce.MNAME}": HashcatBruteForce,
    # f"{HashcatIncremental.MNAME}": HashcatIncremental,
    # f"{HashcatMasks.MNAME}": HashcatMasks,
    # f"{HashcatHybrid.MNAME}": HashcatHybrid,

    # sth
    #f"{STH.MNAME}": STH,

    ## attack/services modules
    # hydra attacks
    #f"{HydraWordlist.MNAME}": HydraWordlist,
}

### auxiliary modules

## auxiliary/wordlists modules
auxiliaryWordlistModules = {
    f"{CuppInteractive.MNAME}": CuppInteractive,
    f"{CuppRefine.MNAME}": CuppRefine,
    f"{CuppDownload.MNAME}": CuppDownload,
    f"{CuppAlecto.MNAME}": CuppAlecto,
    f"{HcutilsCombinator.MNAME}": HcutilsCombinator,
    f"{HcutilsCombinator3.MNAME}": HcutilsCombinator3,
    f"{HcutilsCombipow.MNAME}": HcutilsCombipow,
    f"{HcutilsMli2.MNAME}": HcutilsMli2,
    f"{HcutilsReqExclude.MNAME}": HcutilsReqExclude,
    f"{HcutilsReqInclude.MNAME}": HcutilsReqInclude,
    f"{HcutilsRli.MNAME}": HcutilsRli,
    f"{HcutilsSplitlen.MNAME}": HcutilsSplitlen
    #f"{Cewl.MNAME}": Cewl
    #f"{BopscrkInteractive.MNAME}": BopscrkInteractive,
    #f"{BopscrkCombine.MNAME}": BopscrkCombine,
}

## auxiliary/hashes modules
auxiliaryHashesModules = {
    #f"{HashesStatus.MNAME}": HashesStatus,
    f"{HashID.MNAME}": HashID,
    f"{NthAuxiliary.MNAME}": NthAuxiliary,
    f"{HashGenerator.MNAME}": HashGenerator
}

## auxiliary/analysis modules
auxiliaryAnalysisModules = {
    f"{PackStatsgen.MNAME}": PackStatsgen,
    f"{PackMaskgen.MNAME}": PackMaskgen,
    f"{PackPolicyAuxiliary.MNAME}": PackPolicyAuxiliary,
    f"{PackWholegen.MNAME}": PackWholegen

}

## auxiliary/passwords modules
auxiliaryPasswordsModules = {
    f"{PasswordGenerator.MNAME}": PasswordGenerator,
    f"{ShufflePassword.MNAME}": ShufflePassword
}


## auxiliary modules
auxiliary_modules = {
    ## auxiliary/wordlists modules
    **auxiliaryWordlistModules,

    ## auxiliary/hashes modules
    **auxiliaryHashesModules,

    ## auxiliary/analysis modules
    **auxiliaryAnalysisModules,

    ## auxiliary/passwords modules
    **auxiliaryPasswordsModules
}

amaModules = {
    **attackModules,
    **auxiliary_modules
}
