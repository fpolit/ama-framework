#!/usr/bin/env python3
#
# ama-framework interactor
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import sys
import argparse
import psycopg2
from fineprint.status import print_failure
# cmdsets imports
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

# cmd2 imports
import cmd2
from cmd2 import Cmd

# banner imports
from .core.banner import Banner

# cmdset categories
from .core.cmdsets import CmdsetCategory as Category

# import ama version
from ama.core.version import get_version

# import ama availables modules
from ama.data.modules import amaModules

from ama.core.files import Path
from ama.config import AMA_HOME

class Ama(Cmd):
    """
    CLI App to interact with ama-framework
    """
    # CORE_CATEGORY = Category.CORE
    # MODULE_CATEGORY = Category.MODULE
    # DB_CATEGORY = Category.DB
    # SLURM_CATEGORY = Category.SLURM

    AMA_HOME = AMA_HOME

    def __init__(self, db_credentials:Path = Path.joinpath(AMA_HOME, 'db/database.json')):
        super().__init__(use_ipython=True)

        self.debug = True
        self.intro = Banner.random()
        self.prompt = "ama > "
        self.continuation_prompt = "> "
        self.default_category = Category.CORE
        self.db_conn = self.init_db_connection(db_credentials)
        self.workspace = "default" # selected workspace
        self.database_credentials_file = db_credentials
        self.modules = amaModules # format {NAME: MODULE_CLASS, ....}
        self.selectedModule = None # selected module with use command (Instance of the module)
        self.filteredModules = [] # filtered modules by a search (format: [(#, MODULE_CLASS), ...])
        self.gvalues = {} # global values set by setvg (format {OPTION_NAME: OPTION_VALUE, ...})

    def init_db_connection(self, db_credentials:Path):
        db_conn = None
        try:
            dbCredentials = Connection.dbCreds(db_credentials)
            db_conn = psycopg2.connect(**dbCredentials)
            del dbCredentials

        except Exception as error:
            print_failure(error)
            print_failure("Error while connecting to database")

        finally:
            return db_conn


def main(argv=sys.argv[1:]):
    ama = Ama()
    sys.exit(ama.cmdloop())
