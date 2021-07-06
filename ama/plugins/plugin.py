#!/usr/bin/env python3
#
# Plugin class to make password crackers and auxiliary applications
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import re
import os

# core.files imports
from ..files import (
    Path,
    get_exec_path
)

# typing import
from typing import List


class Plugin:
    def __init__(self, name: List[str], *, version=None, main_exec=None, search_exec=True):
        #import pdb;pdb.set_trace()

        self.name = name #it can be a list of name (e.g. ["hashcat", "hc"])
        self.main_name = name[0] if isinstance(name, list) else name
        self.version = version
        self.main_exec= main_exec
        self.enable = False

        if main_exec:
            self.enable = True
        else:
            if search_exec:
                self.main_exec = Plugin.search_main_exec(name)
                if self.main_exec is None:
                    self.enable = False
                else:
                    self.enable = True
            else: #this plugin doesn't havent a cli command but the source code is avaliable
                self.enable = True
                self.main_exec = None

    def __repr__(self):
        return f"Plugin(Name: {self.main_name}, exec: {self.main_exec}, version: {self.version})"

    #debugged - date: Feb 27 2021
    @staticmethod
    def search_main_exec(plugin_name: List[str]):
        """
        Search an executable file of a plugin using its names (list) as patterns
        """
        # searching the executable for a plugin in the PATH
        #import pdb; pdb.set_trace()
        exec_path = get_exec_path()
        for name in plugin_name:
            exec_pattern = re.compile(rf"{name}(\.exe)?")
            for dir_path in exec_path:
                dirname = dir_path
                for executable in os.listdir(dir_path):
                    if exec_pattern.fullmatch(executable):
                        main_exec = os.path.join(dirname, executable)
                        return main_exec

        return None
