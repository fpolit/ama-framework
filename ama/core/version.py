#!/usr/bin/env python3
from cement.utils.version import get_version as cement_get_version

VERSION = (1, 3, 0, 'alpha', 0)

def get_version(version=VERSION):
    return cement_get_version(version)
