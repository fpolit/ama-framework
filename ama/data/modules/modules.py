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

amaModules = [
    [JohnWordlist.mname, JohnWordlist],
    [JohnIncremental.mname, JohnIncremental],
    [JohnCombination.mname, JohnCombination],
    [JohnHybrid.mname, JohnHybrid],

    [HashcatWordlist.mname, HashcatWordlist],
    [HashcatIncremental.mname, HashcatIncremental]
    [HashcatCombination.mname, HashcatCombination]
    [HashcatHybrid.mname, HashcatHybrid]
]
