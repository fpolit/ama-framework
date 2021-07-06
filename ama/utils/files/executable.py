#!/usr/bin/env python3
#
# this module return the PATH of a os (without repetitions and check if the directories returned
# by os.get_exec_path() exists
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os

def get_exec_path():
    PATH = []
    OSPATH = os.get_exec_path()
    for k, dir_path in enumerate(OSPATH):
        if dir_path not in PATH[:k] and os.path.isdir(dir_path):
            PATH.append(dir_path)

    return PATH
