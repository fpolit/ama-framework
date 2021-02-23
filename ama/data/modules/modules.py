#!/usr/bin/env python3
#
# ama supported modules
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import json


### attacks modules imports
## import attack/hashes modules

# john attacks import
from ama.core.modules.attack.hashes import (
    JohnWordlist,
    JohnIncremental,
    JohnSingle,
    JohnCombination,
    JohnHybrid
)

# hashcat attacks import
from ama.core.modules.attack.hashes import (
    HashcatWordlist,
    HashcatIncremental,
    HashcatCombination,
    HashcatHybrid
)

## import attack/hashes modules
# hydra attacks import
from ama.core.modules.attack.services import (
    hydraWordlist
)


### auxiliary modules imports
## import auxiliary/wordlists modules



amaModulesType = [
    "attack",
    "auxiliary"
]

amaModules = {
    f"{JohnWordlist.mname}": JohnWordlist,
    f"{JohnIncremental.mname}": JohnIncremental,
    f"{JohnSingle.mname}": JohnSingle,
    f"{JohnCombination.mname}": JohnCombination,
    f"{JohnHybrid.mname}": JohnHybrid,

    f"{HashcatWordlist.mname}": HashcatWordlist,
    f"{HashcatIncremental.mname}": HashcatIncremental,
    f"{HashcatCombination.mname}": HashcatCombination,
    f"{HashcatHybrid.mname}": HashcatHybrid,

    f"Hydra.mname": hydraWordlist
}
