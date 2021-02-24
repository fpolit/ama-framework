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
    JohnWordlist,
    JohnIncremental,
    JohnSingle,
    JohnCombination,
    JohnHybrid
)

# hashcat attacks imports
from ama.core.modules.attack.hashes import (
    HashcatWordlist,
    HashcatIncremental,
    HashcatCombination,
    HashcatHybrid
)

## attack/hashes modules imports
# hydra attacks imports
from ama.core.modules.attack.services import (
    hydraWordlist
)


### auxiliary modules imports
## auxiliary/wordlists modules imports


## auxiliary/hashes modules imports


## auxiliary/combinator modules imports


## auxiliary/analysis modules imports
# pack auxiliary/analysis modules
from ama.core.modules.auxiliary.analysis import (
    PackStatsgen,
    PackMaskgen
)


amaModulesType = [
    "attack",
    "auxiliary"
]

amaModules = {
### attack modules

    ## attack/hash modules
    # john attacks
    f"{JohnWordlist.mname}": JohnWordlist,
    f"{JohnIncremental.mname}": JohnIncremental,
    f"{JohnSingle.mname}": JohnSingle,
    f"{JohnCombination.mname}": JohnCombination,
    f"{JohnHybrid.mname}": JohnHybrid,

    # john attacks
    f"{HashcatWordlist.mname}": HashcatWordlist,
    f"{HashcatIncremental.mname}": HashcatIncremental,
    f"{HashcatCombination.mname}": HashcatCombination,
    f"{HashcatHybrid.mname}": HashcatHybrid,

    ## attack/services modules
    # hydra attacks
    f"{Hydra.mname}": hydraWordlist,


### auxiliary modules
    ## auxiliary/wordlists modules

    ## auxiliary/hashes modules

    ## auxiliary/combinator modules

    ## auxiliary/analysis modules
    f"{PackStatsgen.mname}": PackStatsgen,
    f"{PackMaskgen.mname}": PackMaskgen
}
