#!/usr/bin/env python3
#
# module commands set for ama-framework (Module Commands Category)
# commands set related to interactionw with modules
# defined commands: use, setv, setvg, back, attack
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse

from fineprint.status import (
    print_failure,
    print_status
)

# version import
from ama.core.version import get_version

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)

# modules.base import
from ama.core.modules.base import (
    Attack,
    Auxiliary
)

# slurm import
from ama.core.slurm import Slurm

@with_default_category(Category.MODULE)
class Interaction(CommandSet):
    """
    Module command set category related to interaction with ama modules
    commands set: use, setv, back, attack
    """

    def __init__(self):
        super().__init__()


    use_parser = argparse.ArgumentParser()
    use_parser.add_argument('module', help="ama module")

    @with_argparser(use_parser)
    def do_use(self, args):
        """
        Select a avaliable module
        """
        selected = False
        module = args.module

        try:
            module = int(module)

            for moduleId, moduleClass in self._cmd.filteredModules:
                if moduleId == module:
                    selected = True
                    self._cmd.selectedModule = moduleClass()
                    moduleType = moduleClass.MTYPE
                    moduleSubtype = moduleClass.MSUBTYPE
                    moduleName = moduleClass.NAME
                    self._cmd.prompt = f"ama {moduleType}({moduleSubtype}/{moduleName}) > "
                    break

        except ValueError: # module is a string
            for moduleName, moduleClass in self._cmd.modules.items():
                if module == moduleClass.MNAME:
                    selected = True
                    self._cmd.selectedModule = moduleClass()
                    moduleType = moduleClass.MTYPE
                    moduleSubtype = moduleClass.MSUBTYPE
                    moduleName = moduleClass.NAME
                    self._cmd.prompt = f"ama {moduleType}({moduleSubtype}/{moduleName}) > "
                    break


        if not selected:
            if isinstance(module, int):
                print_failure(f"No module available with id:  {module}")
            else: # if module string or other type
                print_failure(f"No module available:  {module}")


    setv_parser = argparse.ArgumentParser()
    setv_parser.add_argument("variable", help="variable to set value")
    setv_parser.add_argument("value", help="value")

    @with_argparser(setv_parser)
    def do_setv(self, args):
        """
        Set a value to a variable
        """
        #import pdb; pdb.set_trace()

        selectedModule = self._cmd.selectedModule

        if selectedModule:
            variable = args.variable.lower()
            value = args.value

            if selectedModule.isVariable(variable):
                if isinstance(selectedModule, Attack):
                    if selectedModule.isAttackVariable(variable):
                        selectedModule.attack[variable].value = value

                    else: #variable is a slurm variable
                        slurmOptions = selectedModule.slurm.options()
                        slurmOptions[variable].value = value
                        selectedModule.slurm = Slurm(**slurmOptions)

                elif isinstance(selectedModule, Auxiliary):
                    if selectedModule.isAuxiliaryVariable(variable):
                        selectedModule.auxiliary[variable].value = value

                    else: #variable is a slurm variable
                        slurmOptions = selectedModule.slurm.options()
                        slurmOptions[variable].value = value
                        selectedModule.slurm = Slurm(**slurmOptions)

                self._cmd.selectedModule = selectedModule
            else:
                print_failure(f"No {variable.upper()} variable in {selectedModule.mname} module")

        else:
            print_failure("No module selected")

    def do_back(self, args):
        """
        Stop interaction with selected module and go back to main ama-framework console
        """
        self._cmd.selectedModule = None
        self._cmd.prompt = "ama > "

    #debugged - data: feb 27 2021
    def do_attack(self, args):
        """
        Perform an attack with the selected module
        """
        attackModule = self._cmd.selectedModule
        if attackModule:
            if isinstance(attackModule, Attack):
                print_status(f"Running {attackModule.MNAME} module")
                attackModule.attack()
            else: # auxiliaryModule is an instance of Auxiliary
                print_failure(f"No attack method for {attackModule.MNAME} module")
        else:
            print_failure("No module selected")

    #debugged - data: feb 27 2021
    def do_run(self, args):
        """
        Run the selected auxiliary module
        """
        auxiliaryModule = self._cmd.selectedModule
        if auxiliaryModule:
            if isinstance(auxiliaryModule, Auxiliary):
                print_status(f"Running {auxiliaryModule.MNAME} module")
                auxiliaryModule.run()
            else: # auxiliaryModule is an instance of Attack
                print_failure(f"No run method for {auxiliaryModule.MNAME} module")
        else:
            print_failure("No module selected")
