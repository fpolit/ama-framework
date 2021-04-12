#!/usr/bin/env python3
#
# ama-framework interactor
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import json
import sys
import argparse
import psycopg2
import cmd2
from cmd2 import Cmd
from fineprint.status import print_failure


# categories
from .core.cmdsets import CmdsetCategory as Category

# cmdsets
from .core.cmdsets.db import (
    Workspace,
    Connection,
    Loot
)

from .core.cmdsets.module import (
    Search,
    Information,
    Interaction
)

from .core.cmdsets.core import (
    Core
)

from .core.cmdsets.hashcat import (
    HashcatUtils
)

# banner
from .core.banner import Banner

# version
from ama.core.version import get_version

# availables modules
from ama.data.modules import amaModules
from ama.core.files import Path
from ama.config import AMA_HOME

# slurm
from ama.core.slurm import Slurm

class Ama(Cmd):
    """
    CLI App to interact with ama-framework
    """
    # CORE_CATEGORY = Category.CORE
    # MODULE_CATEGORY = Category.MODULE
    # DB_CATEGORY = Category.DB
    # SLURM_CATEGORY = Category.SLURM

    AMA_HOME = AMA_HOME

    def __init__(self,
                 ama_config:Path = Path.joinpath(AMA_HOME, 'config/ama.json')):

        super().__init__(use_ipython=True)

        self.debug = True
        self.intro = Banner.random()
        self.prompt = "ama > "
        self.continuation_prompt = "> "
        self.default_category = Category.CORE
        self.config = Ama.get_ama_configurations(ama_config)
        self.db_conn = self.init_db_connection()
        self.workspace = "default" # selected workspace
        # ama configuration (slurm.conf path, dbcreds path, john and hashcat executable path)
        self.modules = amaModules # format {NAME: MODULE_CLASS, ....}
        self.selectedModule = None # selected module with 'use' command (Instance of the module)
        self.filteredModules = [] # filtered modules(format: [(#, MODULE_CLASS), ...])
        self.gvalues = {} # global values(format {OPTION_NAME: OPTION_VALUE, ...})
        self.slurm_config = self.init_slurm_config()
        #import pdb; pdb.set_trace()


    @staticmethod
    def get_ama_configurations(ama_config:Path):
        configurations = None
        with open(ama_config) as config:
            configurations = json.load(config)

        if db_credentials := configurations["db_credentials_file"]:
            configurations["db_credentials_file"] = Path(db_credentials)

        if slurm_conf_file := configurations["slurm_conf_file"]:
            configurations["slurm_conf_file"] = Path(slurm_conf_file)

        return configurations


    def init_db_connection(self):
        db_conn = None
        #import pdb; pdb.set_trace()
        try:
            db_credentials = Path(self.config.get('db_credentials_file'))
            dbCredentials = Connection.dbCreds(db_credentials)
            db_conn = psycopg2.connect(**dbCredentials)
            del dbCredentials

        except Exception as error:
            print_failure(error)
            #print_failure("Error while connecting to database")

        finally:
            return db_conn


    def init_slurm_config(self):
        #import pdb;pdb.set_trace()
        try:
            slurm_config_file = self.config.get('slurm_conf_file')
            if slurm_config_file is None:
                slurm_config_file = Slurm.find_slurm_config()

            return Slurm.parser_slurm_conf(slurm_config_file)

        except Exception as error:
            print_failure(error)
            #print_failure("Error while parsing slurm configuration file")

def main(argv=sys.argv[1:]):
    ama = Ama()
    sys.exit(ama.cmdloop())
