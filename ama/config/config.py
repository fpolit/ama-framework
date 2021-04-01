#!/usr/bin/env python3
#
# configure ama directory (AMA_HOME) in user home directory
#
# date: Mar 31  2021
# Maintainer: glozanoa <glozanoa@uni.pe>


# AMA_HOME directory structure

# .ama
# |- db
# | |- database.json (database credentials)
# |
# |- log
# | |- database.log (logs relate to database bugs)
# | |- ama.log      (logs relate to ama-framework bugs)
# | |- modules.log  (logs relate to modules bugs)
# |
# |- modules
# | |- attack       (directory to save custom attack modules)
# | |- auxiliary    (directory to save custom auxiliary modules)
# |
# |- plugins
# | |- auxiliary   (directory to save custom auxiliary plugins)
# | |- cracker     (directory to save custom cracker plugins)
# |
# |- data
# | |- modules.py  (python script with custom ama modules)

import os
from ama.core.files import Path

from fineprint.status import print_successful
from fineprint.color import ColorStr

class FilesStruct:
    def __init__(self, name, base_path,
                 inside_dirs = [],  # list of inside directories (strings)
                 inside_files = [], # list of inside files (string)
                 filesStructs = []): # list of inside files structs (instances of FilesStruct)

        self.base_path = Path(base_path)
        self.path = Path.joinpath(self.base_path, name)
        #list of FilesStruct instances
        self.inside_dirs = [Path.joinpath(self.path, inside_dir) for inside_dir in inside_dirs]
        #list of Path instances
        self.inside_files = [Path.joinpath(self.path, inside_file) for inside_file in inside_files]
        self.filesStructs = filesStructs

    def create(self):
        #import pdb;pdb.set_trace()
        if not self.path.exists():
            self.path.mkdir()
        for directory in self.inside_dirs:
            if not directory.exists():
                directory.mkdir()

        for inside_file in self.inside_files:
            if not inside_file.exists():
                inside_file.touch()

        for filesStruct in self.filesStructs:
            filesStruct.create()


USER_HOME = Path.home()
AMA_HOME = Path.joinpath(USER_HOME, '.ama')

def create_ama_home(base_path: Path = USER_HOME):
    """
    create ama-framework home file structure
    """
    #import pdb;pdb.set_trace()
    ama_home = FilesStruct('.ama', base_path=base_path)

    BASE_PATH = ama_home.path
    ama_db = FilesStruct('db', base_path=BASE_PATH,
                         inside_files=['database.json'])

    ama_logs = FilesStruct('log', base_path=BASE_PATH,
                           inside_files=['database.log',
                                         'ama.log',
                                         'modules.log'])

    ama_data = FilesStruct('data', base_path=BASE_PATH,
                         inside_files=['modules.py'])

    ama_modules = FilesStruct('modules', base_path=BASE_PATH,
                              inside_dirs=['attack', 'auxiliary'])

    ama_plugins = FilesStruct('plugins', base_path=BASE_PATH,
                              inside_dirs=['auxiliary', 'cracker'])

    ama_home.filesStructs = [ama_db, ama_logs, ama_data, ama_modules, ama_plugins]
    ama_home.create()
    print_successful(f"Ama home directory has been created at {ColorStr(ama_home.path).StyleBRIGHT}")
