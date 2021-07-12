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
# | |- database.log (logs relate to database logs)
# | |- ama.log      (logs relate to ama logs)
# | |- history.dat  (history of commands)
# |
# |- modules
# | |- attack       (directory to save custom attack modules)
# | |- auxiliary    (directory to save custom auxiliary modules)
# |
# |- config
# | |- ama.json  (ama's configuration file)


import os
import json
from pathlib import Path

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
                                         'history.dat'])

    # ama_data = FilesStruct('data', base_path=BASE_PATH,
    #                      inside_files=['modules.py'])

    ama_modules = FilesStruct('modules', base_path=BASE_PATH,
                              inside_dirs=['attack', 'auxiliary'])

    # ama_plugins = FilesStruct('plugins', base_path=BASE_PATH,
    #                           inside_dirs=['auxiliary', 'cracker'])

    ama_config = FilesStruct('config', base_path=BASE_PATH,
                             inside_files=['ama.json'])

    ama_home.filesStructs = [ama_db, ama_logs, ama_modules, ama_config]
    ama_home.create()
    print_successful(f"Ama home directory has been created: {ColorStr(ama_home.path).StyleBRIGHT}")


def init_ama_config():
    #import pdb;pdb.set_trace()
    ama_config_file = Path.joinpath(AMA_HOME, 'config/ama.json')
    database_credentials = Path.joinpath(AMA_HOME, 'db/database.json')
    configurations = {
        'db_credentials_file': str(database_credentials),
        'john': None,
        'hashcat': None
    }

    with open(ama_config_file, 'w') as config:
        json.dump(configurations, config, indent=4)

    print_successful(f"Configuration file has been created: {ColorStr(ama_config_file).StyleBRIGHT}")
