#!/usr/bin/env python3
#
# this module return the PATH of a os (without repetitions and check if the directories returned
# by os.get_exec_path() exists
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os

def getExecPath():
    PATH = []
    OSPATH = os.get_exec_path()
    for k, dirPath in enumerate(OSPATH):
        if dirPath not in PATH[:k] and os.path.isdir(dirPath):
            PATH.append(dirPath)

    return PATH
