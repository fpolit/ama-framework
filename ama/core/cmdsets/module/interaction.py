#!/usr/bin/env python3
#
# module commands set for ama-framework (Module Commands Category)
# commands set related to interactionw with modules
# defined commands: use, setv, setvg, back, attack
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse

# version import
from ...version import get_version

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)

@with_default_category(Category.MODULE)
class Interaction(CommandSet):
    """
    Module command set category related to interaction with ama modules
    commands set: use, setv, setvg, back, attack
    """

    def __init__(self):
        super().__init__()


    use_parser = argparse.ArgumentParser()
    use_parser.add_argument('module', help="ama module")
    def do_use(self, args):
        """
        Select a avaliable module
        """

        selected = False # module no selected yet

        if isinstance(module, int): # request information about a filtered module
            for moduleId, moduleClass in self._cmd.filteredModules:
                if moduleId == module:
                    selected = True
                    self._cmd.selectedModule = moduleClass
                    moduleType = moduleclass.mtype
                    moduleSubtype = moduleClass.msubtype
                    moduleName = moduleClass.
                    #moduleType, moduleSubtype, moduleName = moduleClass.mname.split("/")
                    self._cmd.prompt = f"ama {moduleType}({moduleSubtype}/{moduleName})> "
                    break

        elif isinstance(module, str):
            for moduleClass in self._cmd.modules.values():
                if module == moduleClass.mname:
                    selected = True
                    self._cmd.selectedModule = moduleClass
                    moduleType, moduleSubtype, moduleName = moduleClass.mname.split("/")
                    self._cmd.prompt = f"ama {moduleType}({moduleSubtype}/{moduleName})> "
                    break

    setv_parser = argparse.ArgumentParser()
    setv_parser.add_argument("variable", help="variable to set value")
    setv_parser.add_argument("value", help="value")

    @with_argparser(setv_parser)
    def do_setv(self, args):
        """
        Set a value to a variable
        """
        moduleClass = self._cmd.selectedModule

        if moduleClass:
            variable = args.variable.lower()
            value = args.value
            if moduleClass.mtype == "attack":
                if variable in moduleClass.attack or
                variable in moduleClass.slurm:
                
                    self._cmd.selectedModule.attack[variable] = value
                else:
                    cmd2.Cmd.pwarning(f"No {variable} in {moduleClass.mname} module")

            elif moduleClass.mtype == "auxiliary":
                if variable in moduleClass.auxiliary:
                    self._cmd.selectedModule.auxiliary[variable] = value

                else:
                    cmd2.Cmd.pwarning(f"No {variable} in {moduleClass.mname} module")

        else:
            cmd2.Cmd.poutput("No module selected")

    def do_setvg(self, args):
        """
        Set a value to a variable globally
        """
        pass

    def do_back(self, args):
        """
        Stop interaction with selected module and go back to main ama-framework console
        """
        self._cmd.selectedModule = None
        self._cmd.prompt = "ama> "

    def do_attack(self, args):
        """
        Perform a attack with the selected module
        """
        attackModule = self._cmd.selectedModule
        cmd2.Cmd.poutput(f"Running {attackModule.mname} module")
        attackModule.attack()

    def do_run(self, args):
        """
        Run the selected auxiliary module
        """
        auxiliaryModule = self._cmd.selectedModule
        cmd2.Cmd.poutput(f"Running {auxiliaryModule.mname} module")
        auxiliaryModule.run()
