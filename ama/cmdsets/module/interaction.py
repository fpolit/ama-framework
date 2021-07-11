#!/usr/bin/env python3
#
# module commands set for ama-framework (Module Commands Category)
# commands set related to interactionw with modules
# defined commands: use, setv, setvg, back, attack
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
import sys
import argparse
import argcomplete

from fineprint.status import (
    print_failure,
    print_status,
    print_successful
)

from fineprint.color import ColorStr

# version import
from ama.version import get_version

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
from cmd2 import (
    Cmd,
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
)

# modules.base import
from ama.modules.base import (
    Attack,
    Auxiliary
)

# crackers
# from ama.plugins.cracker import (
#     John,
#     Hashcat
# )

from ama.data.modules import Glue
from ama.utils.autocomplete import autocomplete_setv
# slurm import
#from ama.core.slurm import Slurm


from ama.utils.files import Path

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

    bkp_parser.add_argument('-r', '--required', action='store_true',
                                  help="Backup only required options")

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
        output = None
        try:
            if selectedModule := self._cmd.selectedModule:
                if args.required and args.only_module:
                    print_status(f"Performing backup of {ColorStr(selectedModule.mname).StyleBRIGHT} require module options")
                elif (not args.required) and args.only_module:
                    print_status(f"Performing backup of {ColorStr(selectedModule.mname).StyleBRIGHT} module options")

                elif args.required and args.only_slurm:
                    if isinstance(selectedModule, Auxiliary):
                        raise Exception("Auxiliary modules have not slurm options")
                    else: # selectedModule is an Attack
                        print_status(f"Performing backup of {ColorStr(selectedModule.mname).StyleBRIGHT} required slurm options")

                elif (not args.required) and args.only_slurm:
                    if isinstance(selectedModule, Auxiliary):
                        raise Exception("Auxiliary modules have not slurm options")
                    else:
                        print_status(f"Performing backup of {ColorStr(selectedModule.mname).StyleBRIGHT} slurm options")

                elif args.required and not (args.only_module or  args.only_slurm):
                    print_status(f"Performing backup of {ColorStr(selectedModule.mname).StyleBRIGHT} required options")
                elif not (args.required or args.only_module or  args.only_slurm):
                    print_status(f"Performing backup of {ColorStr(selectedModule.mname).StyleBRIGHT} options")

                if args.output:
                    output = open(args.output, 'w')
                else:
                    output = sys.stdout

                no_empty_options = selectedModule.get_no_empty_options(args.required)

                only_module = args.only_module
                only_slurm  = args.only_slurm

                for name, value in no_empty_options.items():
                    if (selectedModule.isModuleOption(name) and only_module) or \
                       (selectedModule.isSlurmOption(name) and only_slurm) or \
                       (not only_module and not only_slurm):
                        bkp_cmd = f"setv {name.upper()} {value}"
                        output.write(f"{bkp_cmd}\n")

                if isinstance(selectedModule, Attack):
                    if pre_attack_module := selectedModule.selected_pre_attack:
                        no_empty_pre_attack_options = pre_attack_module.get_no_empty_options()
                        for name, value in no_empty_pre_attack_options.items():
                            if (selectedModule.isModuleOption(name) and only_module) or \
                               (selectedModule.isSlurmOption(name) and only_slurm) or \
                               (not only_module and not only_slurm):
                                bkp_cmd = f"setv -pre {name.upper()} {value}"
                                output.write(f"{bkp_cmd}\n")

                    if post_attack_module := selectedModule.selected_post_attack:
                        no_empty_post_attack_options = post_attack_module.get_no_empty_options()
                        for name, value in no_empty_post_attack_options.items():
                            if (selectedModule.isModuleOption(name) and only_module) or \
                               (selectedModule.isSlurmOption(name) and only_slurm) or \
                               (not only_module and not only_slurm):
                                bkp_cmd = f"setv -post {name.upper()} {value}"
                                output.write(f"{bkp_cmd}\n")

            else:
                raise Exception("No module selected")

        except Exception as error:
            print_failure(error)

        finally:
            if args.output:
                print_successful(f"Backup saved to {ColorStr(args.output).StyleBRIGHT} file")
                output.close()


    read_parser = argparse.ArgumentParser()
    read_parser.add_argument('backup',
                             help="Backup file to read")
    @with_argparser(read_parser)
    def do_read(self, args):
        """
        Read a backup file and set options of a module
        """
        #import pdb; pdb.set_trace()
        try:
            selectedModule = self._cmd.selectedModule

            if not selectedModule:
                raise Exception("No module selected")

            backup_file = Path(args.backup)
            permission = [os.R_OK]
            Path.access(permission, backup_file)

            print_status(f"Reading {ColorStr(backup_file).StyleBRIGHT} backup file and setting {ColorStr(selectedModule.MNAME).StyleBRIGHT} options")

            with open(backup_file, 'r') as backup:
                while setv_cmd := backup.readline():
                    setv_cmd = setv_cmd.rstrip()
                    split_setv_cmd = setv_cmd.split(' ')

                    if len(split_setv_cmd) == 4: # this options is of a pre/post attack module
                        setv, helper, option, value = split_setv_cmd
                        if helper in ["-pre", "--preattack"]:
                            if isinstance(selectedModule, Attack):
                                selectedModule.setv(option, value, pre_attack=True)
                            else:
                                print_failure(f"Unable to run {setv_cmd} command. Auxiliary modules have not PreAttack modules")

                        elif helper in ["-post", "--postattack"]:
                            if isinstance(selectedModule, Attack):
                                selectedModule.setv(option, value, post_attack=True)
                            else:
                                print_failure(f"Unable to run {setv_cmd} command. Auxiliary modules have not PostAttack modules")
                        else:
                            print_failure("Unknown helper module")

                    elif len(split_setv_cmd) == 3: # this options is of the main module
                        setv, option, value = split_setv_cmd
                        selectedModule.setv(option, value)
                    else:
                        print_failure(f"Invalid command : {setv_cmd}")

        except Exception as error:
            print_failure(error)

    use_parser = argparse.ArgumentParser()
    use_parser.add_argument('module', help="ama module")
    attack_helper = use_parser.add_mutually_exclusive_group()
    attack_helper.add_argument('-pre', '--preattack', action='store_true',
                               help='Enable selection of preattack module')
    attack_helper.add_argument('-post', '--postattack', action='store_true',
                               help='Enable selection of postattack module')

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

            #import pdb; pdb.set_trace()

            if args.preattack:
                if selectedModule := self._cmd.selectedModule:
                    possible_preattacks = self._cmd.filteredModules + [(None, pre_attack_class)
                                                                       for pre_attack_class in selectedModule.PRE_ATTACKS.values()]
                    for module_id, module_class in possible_preattacks:
                        if moduleId == module_id or moduleName == module_class.MNAME :
                            #import pdb;pdb.set_trace()
                            if module_class.MNAME not in selectedModule.PRE_ATTACKS:
                                raise Exception(f"Selected {module_class.MNAME} isn't a preattack module")

                            if attack_class := Glue.get_full_attack(preattack=module_class,
                                                                    attack=selectedModule,
                                                                    postattack=selectedModule.selected_post_attack):
                                #import pdb; pdb.set_trace()
                                selectedModule.helper_modules['pre_attack'].value = module_class.MNAME
                                selectedModule.selected_pre_attack = module_class()
                                init_options = selectedModule.get_init_options()
                                attack = attack_class(init_options)
                                #attack.selected_pre_attack = module_class()
                                self._cmd.selectedModule = attack
                                print_successful(f"Selected preattack module: {module_class.MNAME}")

                            else:
                                preattack_name = module_class.MNAME
                                postattack_name = selectedModule.selected_post_attack.mname if selectedModule.selected_post_attack else None
                                attack_name = selectedModule.mname

                                raise Exception(f"Invalid full attack combination: fullAttack(preattack={preattack_name}, attack={attack_name}, postattack={postattack_name})")

                else:
                    raise Exception("No attack module selected")

            elif args.postattack:
                if selectedModule := self._cmd.selectedModule:
                    possibles_postattacks = self._cmd.filteredModules + [(None, post_attack_class)
                                                                         for post_attack_class in selectedModule.POST_ATTACKS.values()]
                    for module_id, module_class in possibles_postattacks:
                        if moduleId == module_id or moduleName == module_class.MNAME :
                            #import pdb;pdb.set_trace()
                            if module_class.MNAME not in selectedModule.POST_ATTACKS:
                                raise Exception(f"Selected {module_class.MNAME} isn't a postattack module")

                            if attack_class := Glue.get_full_attack(preattack=selectedModule.selected_pre_attack,
                                                                    attack=selectedModule,
                                                                    postattack=module_class):
                                #import pdb; pdb.set_trace()
                                selectedModule.helper_modules['post_attack'].value = module_class.MNAME
                                selectedModule.selected_post_attack = module_class()
                                init_options = selectedModule.get_init_options()
                                attack = attack_class(init_options)
                                #attack.selected_pre_attack = module_class()
                                self._cmd.selectedModule = attack
                                print_successful(f"Selected postattack module: {module_class.MNAME}")

                            else:
                                preattack_name = selectedModule.selected_post_attack.mname if selectedModule.selected_post_attack else None
                                postattack_name = module_class.MNAME
                                attack_name = selectedModule.mname

                                raise Exception(f"Invalid full attack combination: fullAttack(preattack={preattack_name}, attack={attack_name}, postattack={postattack_name})")

                else:
                    raise Exception("No attack module selected")

            else:
                available_modules = self._cmd.filteredModules + list(self._cmd.modules.items())

                for module_id, moduleClass in available_modules:
                    if moduleId == module_id or moduleName == moduleClass.MNAME:
                        selected = True
                        self._cmd.selectedModule = moduleClass()
                        moduleType = moduleClass.MTYPE
                        moduleSubtype = moduleClass.MSUBTYPE
                        moduleName = moduleClass.NAME
                        subtype_name = ColorStr.ForeRED(f"{moduleSubtype}/{moduleName}")
                        self._cmd.prompt = f"ama {moduleType}({subtype_name}) > "
						#import pdb;pdb.set_trace()
                        self._cmd.do_setv = autocomplete_setv(self._cmd.selectedModule)
                        break

                if not selected:
                    if isinstance(module, int):
                        print_failure(f"No module available with id:  {module}")
                    else: # if module is string or other type
                        print_failure(f"No module available:  {module}")

        except Exception as error:
            print_failure(error)

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


    #setv_parser = argparse.ArgumentParser()
    setv_parser = Cmd2ArgumentParser()
    #setv_parser.add_argument("option", help="Option to set value")
    #setv_parser.add_argument("value",  completer=Cmd.path_complete, help="Value of option")

    # setv_parser.add_argument('-pre', '--preattack', action='store_true',
    #                          help="Set value to pre attack module option")
    # setv_parser.add_argument('-post', '--postattack', action='store_true',
    #                          help="Set value to post attack module option")


    #debugged - date: Feb 28 2021
    # modify (pre and post module) - date Mar 6 2021
    # NOTA: implement setv function in module base class to enable specialization of setv cmd by modules
    # Implemented setv function in 'module' class - date Apr 11 2021 (debugged Apr 11 2021)
    @with_argparser(setv_parser)
    def do_setv(self, args):
        """
        Set a value to an valid option of a module
        """

        try:
            selected_module = self._cmd.selectedModule
            if selected_module:
                print(selected_module)
            else:
                print_failure("No module was selected")

        except Exception as error:
            print_failure(error)

    def do_back(self, args):
        """
        Stop interaction with selected module
        """
        self._cmd.selectedModule = None
        self._cmd.prompt = "ama > "

    # attack_parser = argparse.ArgumentParser()
    # attack_parser.add_argument('-l', '--local', action='store_true',
    #                            help="Try to perform the attack locally")
    # attack_parser.add_argument('-q', '--quiet', action='store_true',
    #                            help="Run quietly")

    # #debugged - date: feb 27 2021
    # @with_argparser(attack_parser)
    # def do_attack(self, args):
    #     """
    #     Perform an attack with the selected module
    #     """

    #     if selectedModule := self._cmd.selectedModule:
    #         if isinstance(selectedModule, Attack):
    #             pre_attack_output = None
    #             if pre_attack := selectedModule.selected_pre_attack:
    #                 print_status(f"Running {ColorStr(pre_attack.mname).StyleBRIGHT} preattack module")
    #                 pre_attack_output = pre_attack.run(quiet=args.quiet)

    #             print_status(f"Running {ColorStr(selectedModule.mname).StyleBRIGHT} attack module")

    #             cracker_main_exec = None
    #             if self._cmd.config:
    #                 if selectedModule.CRACKER == John.MAINNAME:
    #                     cracker_main_exec = self._cmd.config['john']

    #                 elif selectedModule.CRACKER == Hashcat.MAINNAME:
    #                     cracker_main_exec = self._cmd.config['hashcat']

    #             #import pdb;pdb.set_trace()
    #             db_status = True if self._cmd.db_conn else False

    #             db_credential_file = None
    #             if self._cmd.config:
    #                 db_credential_file = self._cmd.config['db_credentials_file']

    #             attack_output = selectedModule.attack(
    #                 local = args.local,
    #                 pre_attack_output = pre_attack_output,
    #                 db_status = db_status,
    #                 workspace = self._cmd.workspace,
    #                 db_credential_file = db_credential_file,
    #                 cracker_main_exec=cracker_main_exec,
    #                 slurm_conf = self._cmd.slurm_config
    #             )


    #             if post_attack := selectedModule.selected_post_attack:
    #                 print_status(f"Running {ColorStr(post_attack.mname).StyleBRIGHT} posattack module")
    #                 post_attack.run(quiet=args.quiet, attack_output=attack_output)

    #         else: # selectedModule is an instance of Auxiliary
    #             print_failure(f"No attack method for {ColorStr(selectedModule.MNAME).StyleBRIGHT} module")
    #     else:
    #         print_failure("No module selected")

    # #debugged - data: feb 27 2021
    # auxiliary_parser = argparse.ArgumentParser()
    # auxiliary_parser.add_argument('-q', '--quiet', action='store_true',
    #                               help="Run quietly")

    # @with_argparser(auxiliary_parser)
    # def do_run(self, args):
    #     """
    #     Run the selected auxiliary module
    #     """
    #     #import pdb; pdb.set_trace()
    #     selectedModule = self._cmd.selectedModule
    #     if selectedModule:
    #         if isinstance(selectedModule, Auxiliary):
    #             print_status(f"Running {ColorStr(selectedModule.MNAME).StyleBRIGHT} module")
    #             selectedModule.run(quiet=args.quiet)
    #         else: # selectedModule is an instance of Attack
    #             print_failure(f"No run method for {ColorStr(selectedModule.MNAME).StyleBRIGHT} module")
    #     else:
    #         print_failure("No module selected")
