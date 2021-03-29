#!/usr/bin/env python3
#
# module commands set for ama-framework (Module Commands Category)
# commands set related to interactionw with modules
# defined commands: use, setv, setvg, back, attack
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import sys
import argparse

from fineprint.status import (
    print_failure,
    print_status,
    print_successful
)

from fineprint.color import ColorStr

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
    Auxiliary,
    #PreAttack,
    #PostAttack
)

from ama.data.modules import Glue

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



    bkp_parser = argparse.ArgumentParser()
    bkp_parser.add_argument('-o', '--output',
                            help="Backup file")

    bkp_options_type = bkp_parser.add_mutually_exclusive_group()
    bkp_options_type.add_argument('-m', '--module', dest='only_module', action='store_true',
                            help="Backup only module options")

    bkp_options_type.add_argument('-s', '--slurm', dest='only_slurm', action='store_true',
                            help="Backup only slurm options")

    # debugged - date: Mar 13 2021
    @with_argparser(bkp_parser)
    def do_bkp(self, args):
        """
        Save all the commands used to set options of a module
        """
        #import pdb; pdb.set_trace()
        if selectedModule := self._cmd.selectedModule:
            print_status(f"Performing backup of {selectedModule.mname} options")
            output = None
            if args.output:
                output = open(args.output, 'w')
            else:
                output = sys.stdout

            no_empty_options = selectedModule.get_no_empty_options()

            only_module = args.only_module
            only_slurm  = args.only_slurm

            for name, value in no_empty_options.items():
                if (selectedModule.isModuleOption(name) and only_module) or \
                   (selectedModule.isSlurmOption(name) and only_slurm) or \
                   (not only_module and not only_slurm):
                    bkp_cmd = f"setv {name.upper()} {value}"
                    output.write(f"{bkp_cmd}\n")

            if pre_attack_module := selectedModule.selected_pre_attack:
                no_empty_pre_attack_options = pre_attack_module.get_no_empty_options()
                for name, value in no_empty_pre_attack_options.items():
                    if (selectedModule.isModuleOption(name) and only_module) or \
                       (selectedModule.isSlurmOption(name) and only_slurm) or \
                       (not only_module and not only_slurm):
                        bkp_cmd = f"setv --pre {name.upper()} {value}"
                        output.write(f"{bkp_cmd}\n")

            if post_attack_module := selectedModule.selected_post_attack:
                no_empty_post_attack_options = post_attack_module.get_no_empty_options()
                for name, value in no_empty_post_attack_options.items():
                    if (selectedModule.isModuleOption(name) and only_module) or \
                       (selectedModule.isSlurmOption(name) and only_slurm) or \
                       (not only_module and not only_slurm):
                        bkp_cmd = f"setv --post {name.upper()} {value}"
                        output.write(f"{bkp_cmd}\n")


            if args.output:
                print_successful(f"Backup saved to {args.output} file")
                output.close()

        else:
            print_failure("No module selected")


    # read_parser = argparse.ArgumentParser()
    # read_parser.add_argument('backup',
    #                          help="Backup file to read")
    # @with_argparser(read_parser)
    # def do_read(self, args):
    #     """
    #     Read a backuo file a setv options of a module
    #     """
    #     import pdb; pdb.set_trace()
    #     if selectedModule := self._cmd.selectedModule:
    #         backup_file = args.backup
    #         print_status(f"Reading {backup_file} backup file and setting {selectedModule.MNAME} module options")
    #         with open(backup_file, 'r') as backup:
    #             while setv_cmd := backup.readline():
    #                 setv_cmd = setv_cmd.rstrip()
    #                 setv, name, value = setv_cmd.split(' ')
    #                 if not setv == 'setv':
    #                     print_failure(f"Invalid setv command: {setv_cmd}")
    #                 else:
    #                     args = argparse.Namespace(**{'option': name.lower(), 'value': value, 'pre': False, 'post': False})
    #                     #self.do_setv(args)
    #     else:
    #         print_failure("No module selected")

    use_parser = argparse.ArgumentParser()
    use_parser.add_argument('module', help="ama module")
    attack_helper = use_parser.add_mutually_exclusive_group(required=False)
    attack_helper.add_argument('-pre', '--preattack', action='store_true',
                               help='Enable selection of preattack modules')
    attack_helper.add_argument('-post', '--postattack', action='store_true',
                               help='Enable selection of postattack modules')

    # debugged - date: Feb 28 2021
    @with_argparser(use_parser)
    def do_use(self, args):
        """
        Select a available module
        """
        #import pdb; pdb.set_trace()
        selected = False
        module = args.module

        moduleId = moduleName = None

        try:
            try:
                moduleId = int(module)

            except ValueError: # module is a string
                moduleName = module

            import pdb; pdb.set_trace()

            if args.preattack:
                if selectedModule := self._cmd.selectedModule:
                    possible_preattacks = self._cmd.filteredModules + [(None, pre_attack_class)
                                                                       for pre_attack_class in selectedModule.PRE_ATTACKS.values()]
                    for module_id, module_class in possible_preattacks:
                        if moduleId == module_id or moduleName == module_class.MNAME :
                            import pdb;pdb.set_trace()
                            if module_class.MNAME not in selectedModule.PRE_ATTACKS:
                                raise Exception(f"Selected {module_class.MNAME} isn't a preattack module")

                            selectedModule.options[option].value = module_class.MNAME
                            selectedModule.selected_pre_attack = module_class()

                            if attack_class := Glue.get_full_attack(preattack=module_class,
                                                                    attack=selectedModule,
                                                                    postattack=selectedModule.selected_post_attack):
                                import pdb; pdb.set_trace()
                                init_options = selectedModule.get_init_options()
                                attack = attack_class(init_options)
                                #attack.selected_pre_attack = module_class()
                                self._cmd.selectedModule = attack
                                print_successful(f"Selected preattack module: {module_class.MNAME}")

                            else:
                                preattack_name = module_class.MNAME
                                postattack_name = selectedModule.selected_pre_attack.mname if selectedModule.selected_pre_attack else None
                                attack_name = selectedModule.mname

                                raise Exception(f"Invalid full attack combination: fullAttack(preattack={preattack_name}, attack={attack_name}, postattack={posattack_name})")

                else:
                    raise Exception("No attack module selected")

            elif args.postattack:
                if selectedModule := self._cmd.selectedModule:
                    possibles_postattacks = self._cmd.filteredModules + [(None, post_attack_class)
                                                                         for post_attack_class in selectedModule.POST_ATTACKS.values()]
                    for module_id, module_class in possibles_postattacks:
                        if moduleId == module_id or moduleName == module_class.MNAME :
                            import pdb;pdb.set_trace()
                            if module_class.MNAME not in selectedModule.POST_ATTACKS:
                                raise Exception(f"Selected {module_class.MNAME} isn't a postattack module")

                            selectedModule.options[option].value = module_class.MNAME
                            selectedModule.selected_post_attack = module_class()

                            if attack_class := Glue.get_full_attack(preattack=selectedModule.selected_pre_attack,
                                                                    attack=selectedModule,
                                                                    postattack=module_class):
                                import pdb; pdb.set_trace()
                                init_options = selectedModule.get_init_options()
                                attack = attack_class(init_options)
                                #attack.selected_pre_attack = module_class()
                                self._cmd.selectedModule = attack
                                print_successful(f"Selected postattack module: {module_class.MNAME}")

                            else:
                                preattack_name = selectedModule.selected_post_attack.mname if selectedModule.selected_post_attack else None
                                postattack_name = module_class.MNAME
                                attack_name = selectedModule.mname

                                raise Exception(f"Invalid full attack combination: fullAttack(preattack={preattack_name}, attack={attack_name}, postattack={posattack_name})")

                else:
                    raise Exception("No attack module selected")

            else:
                available_modules = self._cmd.filteredModules + list(self._cmd.modules.items())

                for module_id, moduleClass in available_modules:
                    if moduleId == module_id or moduleName == moduleClass.MNAME:
                        import pdb;pdb.set_trace()
                        selected = True
                        self._cmd.selectedModule = moduleClass()
                        moduleType = moduleClass.MTYPE
                        moduleSubtype = moduleClass.MSUBTYPE
                        moduleName = moduleClass.NAME
                        subtype_name = ColorStr.ForeRED(f"{moduleSubtype}/{moduleName}")
                        self._cmd.prompt = f"ama {moduleType}({subtype_name}) > "
                        break

                if not selected:
                    if isinstance(module, int):
                        print_failure(f"No module available with id:  {module}")
                    else: # if module is string or other type
                        print_failure(f"No module available:  {module}")

        except Exception as error:
            print_failure(error)

        # else: #initialization of selectedModule's options with the global options' values
        #     selectedModule = self._cmd.selectedModule
        #     for option, value in self._cmd.gvalues.items():
        #         if selectedModule.isOption(option):
        #             if selectedModule.isModuleOption(option):
        #                 argument = selectedModule.options.get(option)
        #                 argument.value = value
        #                 selectedModule.options[option] = argument
        #             else:
        #                 if selectedModule.slurm:
        #                     argument = selectedModule.slurm.options.get(option)
        #                     argument.value = value
        #                     selectedModule.slurm.options[option] = argument
        #                     setattr(selectedModule.slurm, option, value)

        #     self._cmd.selectedModule = selectedModule

    unset_parser = argparse.ArgumentParser()
    unset_parser.add_argument('option', help='Option to unset value')

    @with_argparser(unset_parser)
    def do_unset(self, args):
        """
        Unset value of an option
        """
        selectedModule = self._cmd.selectedModule

        if selectedModule:
            option = args.option.lower()
            if selectedModule.isOption(option):
                if selectedModule.isModuleOption(option):
                    selectedModule.options[option].value = None
                else: #is a valid slurm option
                    selectedModule.slurm.options[option].value = None
                    setattr(selectedModule.slurm, option, None)
            else:
                print_failure(f"No {option.upper()} option in {selectedModule.mname} module")

        else:
            print_failure("No module selected")


    unsetg_parser = argparse.ArgumentParser()
    unsetg_parser.add_argument('option', help='Option to unset value')
    @with_argparser(unsetg_parser)
    def do_unsetg(self, args):
        """
        Unset global value of an option
        """
        selectedModule = self._cmd.selectedModule

        if selectedModule:
            option = args.option.lower()
            if selectedModule.isOption(option):
                if selectedModule.isModuleOption(option):
                    selectedModule.options[option].value = None
                else: #is a valid slurm option
                    selectedModule.slurm.options[option].value = None
                    setattr(selectedModule.slurm, option, None)

                #delete option:value from global values
                if option in self._cmd.gvalues:
                    del self._cmd.gvalues[option]
                else:
                    print_status("{option.upper()} value is not a global value")

            else:
                print_failure(f"No {option.upper()} option in {selectedModule.mname} module")

        else:
            print_failure("No module selected")


    setvg_parser = argparse.ArgumentParser()
    setvg_parser.add_argument("option", help="Option to set value")
    setvg_parser.add_argument("value", help="Value of option")

    @with_argparser(setvg_parser)
    def do_setvg(self, args):
        """
        Set globally a value to an valid option
        """
        #import pdb; pdb.set_trace()

        selectedModule = self._cmd.selectedModule

        if selectedModule:
            option = args.option.lower()
            value = args.value

            try:
                value = int(value)

            except ValueError: # value is a string
                if value in ["True", "False"]:
                    if value == "True":
                        value = True
                    else:
                        value = False

            if selectedModule.isOption(option):
                if selectedModule.isModuleOption(option): #option is a valid module option
                    selectedModule.options[option].value = value

                else: #option is a valid slurm option
                    argument = selectedModule.slurm.options.get(option)
                    argument.value = value
                    selectedModule.slurm.options[option] = argument
                    setattr(selectedModule.slurm, option, value)

                self._cmd.selectedModule = selectedModule
                self._cmd.gvalues[option] = value
            else:
                print_failure(f"No {option.upper()} option in {selectedModule.mname} module")

        else:
            print_failure("No module selected")


    setv_parser = argparse.ArgumentParser()
    setv_parser.add_argument("option", help="Option to set value")
    setv_parser.add_argument("value", help="Value of option")

    setv_parser.add_argument('--pre', action='store_true',
                             help="set value to pre attack module option")
    setv_parser.add_argument('--post', action='store_true',
                             help="set value to post attack module option")

    #debugged - date: Feb 28 2021
    # modify (pre and post module) - date Mar 6 2021
    @with_argparser(setv_parser)
    def do_setv(self, args):
        """
        Set a value to an valid option
        """
        #import pdb; pdb.set_trace()

        selectedModule = self._cmd.selectedModule

        try:
            if selectedModule:
                option = args.option.lower()
                value = args.value

                try:
                    value = int(value)

                except ValueError: # value is a string
                    if value in ["True", "False"]:
                        if value == "True":
                            value = True
                    else:
                        value = False

                if args.pre:
                    if isinstance(selectedModule, Attack):
                        if pre_attack_module := selectedModule.selected_pre_attack:
                            if pre_attack_module.isOption(option):
                                if pre_attack_module.isModuleOption(option): #option is a valid module option
                                    pre_attack_module.options[option].value = value

                            else: #option is a valid slurm option
                                argument = pre_attack_module.slurm.options.get(option)
                                argument.value = value
                                pre_attack_module.slurm.options[option] = argument
                                setattr(pre_attack_module.slurm, option, value)

                            selectedModule.pre_attack = pre_attack_module
                            print(f"(preattack) {option.upper()} => {value}")
                        else:
                            raise Exception(f"{selectedModule.MNAME} module hasn't selected a pre attack module yet")
                    else:
                        raise Exception("Auxiliary modules doesn't support pre attack modules")

                elif args.post:
                    if isinstance(selectedModule, Attack):
                        if post_attack_module := selectedModule.selected_post_attack:
                            if post_attack_module.isOption(option):
                                if post_attack_module.isModuleOption(option): #option is a valid module option
                                    post_attack_module.options[option].value = value

                            else: #option is a valid slurm option
                                argument = post_attack_module.slurm.options.get(option)
                                argument.value = value
                                post_attack_module.slurm.options[option] = argument
                                setattr(post_attack_module.slurm, option, value)

                            selectedModule.post_attack = post_attack_module
                            print(f"(postattack) {option.upper()} => {value}")
                        else:
                            raise Exception(f"{selectedModule.MNAME} module hasn't selected a post attack module yet")
                    else:
                        raise Exception("Auxiliary modules doesn't support post attack modules")

                else: # set option of main attack module
                    if selectedModule.isOption(option):
                        if selectedModule.isModuleOption(option): #option is a valid module option
                            selectedModule.options[option].value = value

                        else: #option is a valid slurm option
                            argument = selectedModule.slurm.options.get(option)
                            argument.value = value
                            selectedModule.slurm.options[option] = argument
                            setattr(selectedModule.slurm, option, value)

                        self._cmd.selectedModule = selectedModule
                        print(f"{option.upper()} => {value}")

                    else:
                        raise Exception(f"No {option.upper()} option in {selectedModule.mname} module")

            else:
                raise Exception("No module selected")

        except Exception as error:
            print_failure(error)

    def do_back(self, args):
        """
        Stop interaction with selected module and go back to main ama-framework console
        """
        self._cmd.selectedModule = None
        self._cmd.prompt = "ama > "

    attack_parser = argparse.ArgumentParser()
    attack_parser.add_argument('-l', '--local', action='store_true',
                               help="Try to perform the attack locally")
    attack_parser.add_argument('-f', '--force', action='store_true',
                               help="Force the attack")
    attack_parser.add_argument('-q', '--quiet', action='store_true',
                               help="Run quietly")

    #debugged - date: feb 27 2021
    @with_argparser(attack_parser)
    def do_attack(self, args):
        """
        Perform an attack with the selected module
        """
        #import pdb; pdb.set_trace()

        if selectedModule := self._cmd.selectedModule:
            if isinstance(selectedModule, Attack):
                pre_attack_output = None
                if pre_attack := selectedModule.selected_pre_attack:
                    print_status(f"Running {pre_attack.mname} preattack module")
                    pre_attack_output = pre_attack.run(quiet=args.quiet)

                print_status(f"Running {selectedModule.mname} attack module")
                attack_output = selectedModule.attack(args.local, args.force, pre_attack_output)

                #import pdb; pdb.set_trace()
                if post_attack := selectedModule.selected_post_attack:
                    print_status(f"Running {post_attack.mname} posattack module")
                    post_attack.run(quiet=args.quiet, attack_output=attack_output)

            else: # selectedModule is an instance of Auxiliary
                print_failure(f"No attack method for {selectedModule.MNAME} module")
        else:
            print_failure("No module selected")

    #debugged - data: feb 27 2021
    def do_run(self, args):
        """
        Run the selected auxiliary module
        """
        #import pdb; pdb.set_trace()
        selectedModule = self._cmd.selectedModule
        if selectedModule:
            if isinstance(selectedModule, Auxiliary):
                print_status(f"Running {selectedModule.MNAME} module")
                selectedModule.run()
            else: # selectedModule is an instance of Attack
                print_failure(f"No run method for {selectedModule.MNAME} module")
        else:
            print_failure("No module selected")
