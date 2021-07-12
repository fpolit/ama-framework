#!/usr/bin/env python3
#
# module commands set for ama-framework (Module Commands Category)
# commands set related to information of modules
# defined commands: info, options, advanced
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse

# core.modules.base imports
from ama.modules.base import (
    Attack,
    Auxiliary
)

# version import
from ama.version import get_version

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
        Provide information about a module
        """
        #import pdb; pdb.set_trace()
        module = args.module

        if module is None:
            if selectedModule := self._cmd.selectedModule:
                print(selectedModule.info())
                #cmd2.Cmd.poutput(moduleInstance.infoMsg())
            else:
                print_failure("No module selected")

        else:
            try:
                module = int(module)
                for moduleId, moduleClass in self._cmd.filteredModules:
                    if moduleId == module:
                        moduleInstance = moduleClass()
                        print(moduleInstance.info())
                        break

            except ValueError: # module is a string
                for moduleClass in self._cmd.modules.values():
                    if module == moduleClass.MNAME:
                        moduleInstance = moduleClass()
                        print(moduleInstance.info())
                        break


    options_parser = argparse.ArgumentParser()
    options_parser.add_argument('module', nargs='?', default=None,
                             help="ama module")
    options_parser.add_argument('-r', '--required', action='store_true',
                                help="Only show required options")
    # options_parser.add_argument('-s', '--slurm', action='store_true', dest='only_slurm',
    #                             help="Show only slurm options")
    # options_parser.add_argument('-m', '--module', action='store_true', dest='only_module',
    #                             help="Show only module options")


    @with_argparser(options_parser)
    def do_options(self, args):
        """
        Show availables options of a module
        """

        module = args.module

        if module is None:
            if selectedModule := self._cmd.selectedModule:
                print(selectedModule.options2table(only_required=args.required))
            else:
                print_failure("No module selected")

        else:
            for moduleId, moduleClass in self._cmd.filteredModules:
                if moduleId == module or moduleClass.MNAME == module:
                    moduleInstance = moduleClass()
                    print(moduleInstance.options2table(only_required=args.required))
                    break
