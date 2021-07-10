#!/usr/bin/env python3
#
# ama-framework interactor
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import threading
import os
import json
import sys
import argparse
#import psycopg2
import cmd2
from cmd2 import Cmd
from fineprint.status import print_failure, print_status


# categories
from .cmdsets import CmdsetCategory as Category

# cmdsets
# from .core.cmdsets.db import (
#     Workspace,
#     Connection,
#     Loot
# )

from .cmdsets.slurm import Slurm as SlurmCmds

# from .core.cmdsets.john import (
#     JohnUtilities
# )

from .cmdsets.module import (
    Search,
    Information,
    Interaction
)

from .core.cmdsets.core import (
    Core
)

# from .core.cmdsets.hashcat import (
#     HashcatUtils
# )

# banner
from .banner import Banner

# version
from ama.version import get_version

# availables modules
from ama.data.modules import amaModules
from ama.utils.files import Path
from ama.config import AMA_HOME

# slurm
from ama.slurm import Slurm


# attack manager
from ama.manager import AttackManager

# logger
import logging
from ama.config.logger import Logger

class Ama(Cmd):
    """
    CLI App to interact with ama-framework
    """

    AMA_HOME = AMA_HOME

    def __init__(self,
                 ama_config:Path = Path.joinpath(AMA_HOME, 'config/ama.json')):

        super().__init__(include_ipy=True,
                         allow_redirection=True,
                         persistent_history_file=Path.joinpath(AMA_HOME, "log/history.dat"))

        #import pdb; pdb.set_trace()
        self.default_to_shell = True
        self.debug = False
        self.intro = Banner.random()
        self.prompt = "ama > "
        self.continuation_prompt = "> "
        self.default_category = Category.CORE
        self.config = Ama.get_ama_configurations(ama_config)
        #self.db_conn = None #self.init_db_connection()
        #self.workspace = "default" # selected workspace
        self.modules = amaModules # format {NAME: MODULE_CLASS, ....}
        self.selectedModule = None # selected module with 'use' command (Instance of the module)
        self.filteredModules = [] # filtered modules(format: [(#, MODULE_CLASS), ...])
        self.manager = AttackManager()
        self.gvalues = {} # global values(format {OPTION_NAME: OPTION_VALUE, ...})

        ## settable options
        self.logfile = Path.joinpath(AMA_HOME, "log/ama.log")
        self.loglevel = logging.WARNING

        ## logging
        self.logger = Logger(__name__, filelog=self.logfile, level=self.loglevel,
                             formatlog='[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
        self.logger.add_handler(handler_type=logging.FileHandler)


    @staticmethod
    def get_ama_configurations(ama_config:Path):
        try:
            configurations = None

            if not os.path.exists(ama_config):
                raise Exception(f"Ama configuration file didn't exist: {ama_config}")

            with open(ama_config) as config:
                configurations = json.load(config)

            if db_credentials := configurations["db_credentials_file"]:
                configurations["db_credentials_file"] = Path(db_credentials)

            if slurm_conf_file := configurations["slurm_conf_file"]:
                configurations["slurm_conf_file"] = Path(slurm_conf_file)

            return configurations

        except Exception as error:
            print_failure(error)
            print_status("Using default ama configuration")


    # def init_db_connection(self):
    #     db_conn = None
    #     #import pdb; pdb.set_trace()
    #     try:
    #         if self.config is None:
    #             raise Exception("Ama configuration file wasn't load.")
    #         db_credentials = Path(self.config.get("db_credentials_file"))
    #         dbCredentials = Connection.dbCreds(db_credentials)
    #         db_conn = psycopg2.connect(**dbCredentials)
    #         del dbCredentials

    #     except Exception as error:
    #         print_failure(error)
    #         print_failure("Error while connecting to database.")
    #         print_status("Database status: disconnected")

    #     finally:
    #         return db_conn


    # def init_slurm_config(self):
    #     #import pdb;pdb.set_trace()
    #     try:

    #         slurm_config_file = None
    #         if self.config:
    #             slurm_config_file = self.config.get("slurm_conf_file")

    #         if slurm_config_file is None:
    #             slurm_config_file = Slurm.find_slurm_config()

    #         return Slurm.parser_slurm_conf(slurm_config_file)

    #     except Exception as error:
    #         print_failure(error)
    #         #print_failure("Error while parsing slurm configuration file")

def main(argv=sys.argv[1:]):
    ama = Ama()
    attack_processor = threading.Thread(target=ama.manager.process, deamon=True)
    attack_processor.start()
    sys.exit(ama.cmdloop())
