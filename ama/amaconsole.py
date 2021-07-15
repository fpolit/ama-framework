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
from pathlib import Path
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


# from .core.cmdsets.john import (
#     JohnUtilities
# )

# from .cmdsets.module import (
#     Search,
#     Information,
#     Interaction,
#     Manager
# )
from .cmdsets.module.manager import Manager

from .cmdsets.core import (
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
from ama.config import AMA_HOME

# slurm
#from ama.slurm import Slurm


# attack manager
from ama.manager import ProcessManager, Process

# logger
import logging
from ama.utils.logger import Logger

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
        self.debug = True
        self.intro = Banner.random()
        self.prompt = "ama > "
        self.continuation_prompt = "> "
        self.default_category = Category.CORE
        self.ama_config = ama_config

        # preloop hooks
        self.register_preloop_hook(self.init_logger)
        self.register_preloop_hook(self.init_config)
        self.register_preloop_hook(self.init_module_processor)

        #self.db_conn = None #self.init_db_connection()
        #self.workspace = "default" # selected workspace
        self.modules = amaModules # format {NAME: MODULE_CLASS, ....}
        self.selectedModule = None # selected module with 'use' command (Instance of the module)
        self.filteredModules = [] # filtered modules(format: [(#, MODULE_CLASS), ...])
        self.gvalues = {} # global values(format {OPTION_NAME: OPTION_VALUE, ...})


    def init_module_processor(self) -> None:
        self.manager = ProcessManager(logfile=self.logfile, loglevel=self.loglevel)
        self.logger.info("Init thread to process submitted modules")
        module_processor = threading.Thread(target=self.manager.process, daemon=True)
        module_processor.start()

    def init_logger(self) -> None:
        self.logfile = Path.joinpath(AMA_HOME, "log/ama.log")
        self.loglevel = logging.DEBUG
        self.logger = Logger(__name__, logfile=self.logfile, level=self.loglevel,
                             logformat='[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
        self.logger.add_handler(handler_type=logging.FileHandler)
        self.logger.info(f"Logger was created: level={self.loglevel}, logfile={self.logfile}")

    def init_config(self) -> None:
        try:
            config = None

            if not os.path.exists(self.ama_config):
                raise Exception(f"Ama configuration file didn't exist: {ama_config}")

            with open(self.ama_config) as config_file:
                config = json.load(config_file)

            if db_creds := config["db_credentials_file"]:
                config["db_credentials_file"] = Path(db_creds)

            self.config = config
            self.logger.info(f"Ama configuration file was read: {self.ama_config}")

        except Exception as error:
            self.logger.warning(f"Error while reading ama config file: {self.ama_config}")
            self.logger.pexcept(error)
            print_status("Using default configuration")
            self.config = {}


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

def main(argv=sys.argv[1:]):
    ama = None
    try:
        #import pdb; pdb.set_trace()
        ama = Ama()
        sys.exit(ama.cmdloop())
    except Exception as error:
        if ama:
            ama.logger.exception(error)
        print(error)
