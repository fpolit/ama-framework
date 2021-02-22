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

@with_default_category(Category.MODULE)
class Information(CommandSet):
    """
    Module command set category related to supplied information of ama modules
    commands set: info, options, advance
    """

    def __init__(self):
        super().__init__()

    info_parser = argparse.ArgumentParser()
    info_parser.add_argument('module', nargs='?', default=None
                             help="ama module")
    @with_argparser(info_parser)
    def do_info(self, args):
        """
        Supplied information about a module
        """

        if isinstance(module, int): # request information about a filtered module
            for moduleId, moduleClass in self._cmd.filteredModules:
                if moduleId == module:
                    cmd2.Cmd.poutput(moduleClass.infoMsg())
                    break

        elif isinstance(module, str):
            for moduleClass in self._cmd.modules.values():
                if module == moduleClass.mname:
                    cmd2.Cmd.poutput(moduleClass.infoMsg())
                    break

        elif module is None:
            if self._cmd.selectedModule is not None:
                cmd2.Cmd.poutput(self._cmd.selectedModule.infoMsg())

        else:
            cmd2.Cmd.pwarning("No module selected")



    options_parser = argparse.ArgumentParser()
    options_parser.add_argument('module', nargs='?', default=None
                             help="ama module")
    def do_options(self, args):
        """
        Show availables options of a module
        """

        if isinstance(module, int): # request information about a filtered module
            for moduleId, moduleClass in self._cmd.filteredModules:
                if moduleId == module:
                    cmd2.Cmd.poutput(moduleClass.optionsMsg())
                    break

        elif isinstance(module, str):
            for moduleClass in self._cmd.modules.values():
                if module == moduleClass.mname:
                    cmd2.Cmd.poutput(moduleClass.optionsMsg())
                    break

        elif module is None:
            if self._cmd.selectedModule is not None:
                cmd2.Cmd.poutput(self._cmd.selectedModule.optionsMsg())

        else:
            cmd2.Cmd.pwarning("No module selected")
