#!/usr/bin/env python3
#
# module commands set for ama-framework (Module Commands Category)
# commands set related to search availables modules
# defined commands: search
#
# date: Feb 21 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse
import re
from tabulate import tabulate

# version import
from ...version import get_version

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
import cmd2
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)

# data/modules imports
from ama.data.modules import (
    amaModulesTypes,
    amaModulesSubtypes,
    amaAttackAuxiliariesModules
)

from ama.core.modules.base import Attack

@with_default_category(Category.MODULE)
class Search(CommandSet):
    """
    Module command set category related to search by avalilables ama modules
    commands set: search
    """

    def __init__(self):
        super().__init__()

    search_parser = argparse.ArgumentParser()
    search_parser.add_argument('-t', '--type', dest='moduleType', choices=amaModulesTypes, default=None,
                               help="Module type")
    search_parser.add_argument('-s', '--subtype', dest='moduleSubtype', choices=amaModulesSubtypes, default=None,
                               help="Module subtype")
    search_parser.add_argument('-p', '--previous', action='store_true',
                               help="Show previous search")
    search_parser.add_argument('pattern', nargs='?', default='',
                               help='Pattern to search availables modules')

    # debugged - date: Mar 4 2021
    @with_argparser(search_parser)
    def do_search(self, args):
        """
        search by availables modules given a pattern
        """
        filteredModules = []
        idModule = 0
        pattern = args.pattern
        #import pdb; pdb.set_trace()
        if pattern:
            moduleType = args.moduleType
            moduleSubtype = args.moduleSubtype
            if moduleType and moduleSubtype:
                for moduleName, moduleClass in self._cmd.modules.items():
                    if moduleType == moduleClass.MTYPE and \
                       moduleSubtype == moduleClass.MSUBTYPE and \
                       re.search(pattern, moduleName, flags=re.IGNORECASE):
                        filteredModules.append((idModule, moduleClass))
                        idModule += 1

            elif moduleType and (moduleSubtype is None):
                if moduleType in amaAttackAuxiliariesModules:
                    selectedModule = self._cmd.selectedModule
                    if selectedModule and isinstance(selectedModule, Attack):
                        attackAuxiliaries = {**selectedModule.PRE_ATTACKS, **selectedModule.POST_ATTACKS}
                        for moduleName, moduleClass in attackAuxiliaries.items():
                            if moduleType == moduleClass.MTYPE and \
                            re.search(pattern, moduleName, flags=re.IGNORECASE):
                                filteredModules.append((idModule, moduleClass))
                                idModule += 1
                    else:
                        for moduleName, moduleClass in self._cmd.modules.items():
                            if moduleType == moduleClass.MTYPE and \
                               re.search(pattern, moduleName, flags=re.IGNORECASE):
                                filteredModules.append((idModule, moduleClass))
                                idModule += 1
                else:
                    for moduleName, moduleClass in self._cmd.modules.items():
                        if moduleType == moduleClass.MTYPE and \
                           re.search(pattern, moduleName, flags=re.IGNORECASE):
                            filteredModules.append((idModule, moduleClass))
                            idModule += 1

            elif moduleSubtype and (moduleType is None):
                for moduleName, moduleClass in self._cmd.modules.items():
                    if moduleSubtype == moduleClass.MSUBTYPE and \
                       re.search(pattern, moduleName, flags=re.IGNORECASE):
                        filteredModules.append((idModule, moduleClass))
                        idModule += 1

            else: # no moduleType or moduleSubtype were supplied
                for moduleName, moduleClass in self._cmd.modules.items():
                    if re.search(pattern, moduleName, flags=re.IGNORECASE):
                        filteredModules.append((idModule, moduleClass))
                        idModule += 1

        else: # no pattern supplied
            moduleType = args.moduleType
            moduleSubtype = args.moduleSubtype

            if moduleType and moduleSubtype:
                for moduleName, moduleClass in self._cmd.modules.items():
                    if moduleType == moduleClass.MTYPE and \
                       moduleSubtype == moduleClass.MSUBTYPE:
                        filteredModules.append((idModule, moduleClass))
                        idModule += 1

            elif moduleType and (moduleSubtype is None):
                if moduleType in amaAttackAuxiliariesModules:
                    selectedModule = self._cmd.selectedModule
                    if selectedModule and isinstance(selectedModule, Attack):
                        attackAuxiliaries = {**selectedModule.PRE_ATTACKS, **selectedModule.POST_ATTACKS}
                        for moduleName, moduleClass in attackAuxiliaries.items():
                            if moduleType == moduleClass.MTYPE:
                                filteredModules.append((idModule, moduleClass))
                                idModule += 1
                    else:
                        for moduleName, moduleClass in self._cmd.modules.items():
                            if moduleType == moduleClass.MTYPE:
                                filteredModules.append((idModule, moduleClass))
                                idModule += 1
                else:
                    for moduleName, moduleClass in self._cmd.modules.items():
                        if moduleType == moduleClass.MTYPE:
                            filteredModules.append((idModule, moduleClass))
                            idModule += 1

            elif moduleSubtype and (moduleType is None):
                for moduleName, moduleClass in self._cmd.modules.items():
                    if moduleSubtype == moduleClass.MSUBTYPE:
                        filteredModules.append((idModule, moduleClass))
                        idModule += 1

            else: # no moduleType or moduleSubtype were supplied
                if args.previous:
                    filteredModules = self._cmd.filteredModules
                else:
                    for moduleName, moduleClass in self._cmd.modules.items():
                        filteredModules.append((idModule, moduleClass))
                        idModule += 1

        self._cmd.filteredModules = filteredModules

        Search.show(filteredModules)


    @staticmethod
    def show(filteredModules):
        """
        Show filtered modules
        """
        headerFM = ["#", "Name", "Description"] # FM: Filtered Modules

        tableFM = [(idModule, moduleClass.MNAME, moduleClass.DESCRIPTION) for idModule, moduleClass in filteredModules]

        #cmd2.Cmd.poutput(tabulate(tableFM, headers=headerFM))
        print(tabulate(tableFM, headers=headerFM))
