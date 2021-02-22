#!/usr/bin/env python3
#
# ama supported modules
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import json


# import attack/hashes modules
from ama.core.modules.attack.hashes import (
    JohnWordlist,
    JohnIncremental,
    JohnCombination,
    JohnHybrid
)

# hashcat attack import
from ama.core.modules.attack.hashes import (
    HashcatWordlist,
    HashcatIncremental,
    HashcatCombination,
    HashcatHybrid
)

amaModulesType = [
    "attack",
    "auxiliary"
]

amaModules = {
    f"{JohnWordlist.mname}": JohnWordlist,
    f"{JohnIncremental.mname}", JohnIncremental,
    f"{JohnCombination.mname}", JohnCombination,
    f"{JohnHybrid.mname}", JohnHybrid,

    f"{HashcatWordlist.mname}", HashcatWordlist,
    f"{HashcatIncremental.mname}", HashcatIncremental,
    f"{HashcatCombination.mname}", HashcatCombination,
    f"{HashcatHybrid.mname}", HashcatHybrid
}
