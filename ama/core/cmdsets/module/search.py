#!/usr/bin/env python3
#
# ama subcommand - search avaliables ama modules
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import re

# cliff imports
from cliff.lister import Lister

# import data/modules
from ama.data import getAmaModules


class SearchModules(Lister):
    """
    Search avaliables ama modules
    """
    def get_parser(self, prog_name):
        parser = super(SearchModules, self).get_parser(prog_name)
        parser.add_argument('name',
                            help='module name')
        parser.add_argument('-mt', '--moduleType',
                            help='module type')

        return parser

    def take_action(self, parsed_args):
        moduleName = parsed_args.name
        moduleType = parsed_args.moduleType

        filteredAmaModules = SearchModules.search(moduleName, moduleType)

        return (('#', 'Module'),
                filteredAmaModules)

    @staticmethod
    def search(self, moduleName, moduleType):
        """
        Search availables ama modules given a moduleName and moduleType.
        Return a tuple of formated tuples
        like (enumeration module, ModuleType/ModuleSubtype/amaModule)
        """
        amaModules = getAmaModules()
        filteredModules = []
        if moduleType and moduleName:
            if moduleType in amaModules:
                amaModulesSubtype = amaModules[moduleType]
                moduleNamePattern = re.compile(rf"[\w\W]*{moduleName}[\w\W]*")

                idModule = 0
                for moduleSubtype, modules in amaModulesSubtype:
                    for amaModule in modules:
                        if moduleNamePattern.fullmatch(amaModule):
                            idModule += 1
                            filteredModules.append((idModule,
                                                    f"{moduleType}/{moduleSubtype}/{amaModule}"))

                return filteredModules

            else:
                filteredModules = [(None, None)]
                return filteredModules
        else:
            if not moduleName:
                filteredModules = [(None, None)]
                return filteredModules
            else:
                for moduleType in amaModules.keys():
                    filteredModules += \
                        SearchModules.search(moduleName, moduleType)
                return filteredModules
