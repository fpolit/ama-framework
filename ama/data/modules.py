#!/usr/bin/env python3
#
# ama supported modules
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import json


def getAmaModules(modules='modules.json'):
    with open(modules, 'r') as supportedModules:
        amaModules = json.load(supportedModules)

    return amaModules

