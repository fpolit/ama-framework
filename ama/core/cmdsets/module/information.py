#!/usr/bin/env python3
#
# module commands set for ama-framework (Module Commands Category)
# commands set related to information of modules
# defined commands: info, options, advanced
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse

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

from fineprint.status import (
    print_failure
)

@with_default_category(Category.MODULE)
class Information(CommandSet):
    """
    Module command set category related to supplied information of ama modules
    commands set: info, options, advance
    """

    def __init__(self):
        super().__init__()

    info_parser = argparse.ArgumentParser()
    info_parser.add_argument('module', nargs='?', default=None,
                             help="ama module")
    @with_argparser(info_parser)
    def do_info(self, args):
        """
        Supplied information about a module
        """
        #import pdb; pdb.set_trace()
        module = args.module

        if module is None:
            selectedModule = self._cmd.selectedModule
            if selectedModule:
                print(selectedModule.infoMsg())
                #cmd2.Cmd.poutput(moduleInstance.infoMsg())
            else:
                print_failure("No module selected")

        else:
            try:
                module = int(module)
                for moduleId, moduleClass in self._cmd.filteredModules:
                    if moduleId == module:
                        moduleInstance = moduleClass()
                        print(moduleInstance.infoMsg())
                        #cmd2.Cmd.poutput(moduleInstance.infoMsg())
                        break

            except ValueError: # module is a string
                for moduleClass in self._cmd.modules.values():
                    if module == moduleClass.MNAME:
                        moduleInstance = moduleClass()
                        print(moduleInstance.infoMsg())
                        #cmd2.Cmd.poutput(moduleInstance.infoMsg())
                        break


    # def do_modules(self, _: cmd2.Statement):
    #     """
    #     show all the availables ama modules
    #     """
    #     amaModulesTable = []


    #     for moduleName, moduleClass in self._cmd.modules:
    #         amaModulesTable.appen([moduleName, ])


    options_parser = argparse.ArgumentParser()
    options_parser.add_argument('module', nargs='?', default=None,
                             help="ama module")

    @with_argparser(options_parser)
    def do_options(self, args):
        """
        Show availables options of a module
        """

        module = args.module

        if module is None:
            selectedModule = self._cmd.selectedModule
            if selectedModule:
                print(selectedModule.optionsMsg())
                #cmd2.Cmd.poutput(moduleInstance.infoMsg())
            else:
                print_failure("No module selected")

        else:
            try:
                module = int(module)
                for moduleId, moduleClass in self._cmd.filteredModules:
                    if moduleId == module:
                        moduleInstance = moduleClass()
                        print(moduleInstance.optionsMsg())
                        #cmd2.Cmd.poutput(moduleInstance.infoMsg())
                        break

            except ValueError: # module is a string
                for moduleClass in self._cmd.modules.values():
                    if module == moduleClass.MNAME:
                        moduleInstance = moduleClass()
                        print(moduleInstance.optionsMsg())
                        #cmd2.Cmd.poutput(moduleInstance.infoMsg())
                        break
