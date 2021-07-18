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
from pathlib import Path
import argcomplete

# version import


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


from ama.version import get_version
from ama.modules.base import (
    Attack,
    Auxiliary,
    Module
)
#from ama.utils.autocomplete import autocomplete_setv
from ama.utils.validator import Answer
from ama.utils.color import ColorStr
from ama.utils.fineprint import (
    print_failure,
    print_status,
    print_successful
)

# crackers
# from ama.plugins.cracker import (
#     John,
#     Hashcat
# )

#from ama.data.modules import Glue


@with_default_category(Category.MODULE)
class Interaction(CommandSet):
    """
    Module command set category related to interaction with ama modules
    commands set: use, setv, back, attack
    """

    def __init__(self):
        super().__init__()



    bkp_parser = Cmd2ArgumentParser()
    bkp_parser.add_argument('backup', completer=Cmd.path_complete,
                            help="Backup file")

    bkp_parser.add_argument('-r', '--required', action='store_true',
                            help="Backup only required options")

    bkp_parser.add_argument('--load', action='store_true',
                            help="Restore backup file")


    @with_argparser(bkp_parser)
    def do_bkp(self, args):
        """
        Perform a backup of the module options to enable restore them
        """
        #import pdb; pdb.set_trace()
        try:
            selected_module = self._cmd.selectedModule
            if selected_module is None:
                raise Exception("No module was selected")


            if args.load:
                with open(args.backup, 'r') as backup:
                    for line in backup:
                        backup_line = line.split()
                        if len(backup_line) == 3: #module option
                            cmd, name, value = backup_line
                            selected_module.setv(name, value)
                        elif len(backup_line) == 4:
                            cmd, flag, name, value = backup_line
                            if flag in ['-pre', '--pre-module']:
                                selected_module.setv(name, value, pre_module=True)
                            elif flag in ['-post', '--post-module']:
                                selected_module.setv(name, value, post_module=True)
                            else:
                                print(f"Invalid flag for setv: {flag}")
                        else:
                            raise Exception(f"Invalid size of setv command: {backup_line}")
            else:
                options = selected_module.get_options(only_required=args.required)

                with open(args.backup, 'w') as output:
                    print("[*] Backup module options")
                    module_options = options.get('module', {})
                    for name, option in module_options.items():
                        if option.value is not None:
                            output.write(f'setv {name} {option.value}\n')

                    print("[*] Backup pre-module options")
                    pre_module_options = options.get('pre_module', {})
                    for name, option in pre_module_options.items():
                        if option.value is not None:
                            output.write(f'setv --pre-module {name} {option.value}\n')

                    print("[*] Backup post-module options")
                    post_module_options = options.get('post_module', {})
                    for name, option in post_module_options.items():
                        if option.value is not None:
                            output.write(f'setv --post-module {name} {option.value}\n')


        except Exception as error:
            print(error)


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
                        #self._cmd.do_setv = self._module_setv(self._cmd.selectedModule)
                        break

                if not selected:
                    if isinstance(module, int):
                        print(f"No module available with id:  {module}")
                    else: # if module is string or other type
                        print(f"No module available:  {module}")

        except Exception as error:
            print(error)

    # unset_parser = argparse.ArgumentParser()
    # unset_parser.add_argument('option', help='Option to unset value')

    # @with_argparser(unset_parser)
    # def do_unset(self, args):
    #     """
    #     Unset value of an option
    #     """
    #     selectedModule = self._cmd.selectedModule

    #     if selectedModule:
    #         option = args.option.lower()
    #         if selectedModule.isOption(option):
    #             if selectedModule.isModuleOption(option):
    #                 selectedModule.options[option].value = None
    #             else: #is a valid slurm option
    #                 selectedModule.slurm.options[option].value = None
    #                 setattr(selectedModule.slurm, option, None)
    #         else:
    #             print_failure(f"No {option.upper()} option in {selectedModule.mname} module")

    #     else:
    #         print_failure("No module selected")


    # unsetg_parser = argparse.ArgumentParser()
    # unsetg_parser.add_argument('option', help='Option to unset value')
    # @with_argparser(unsetg_parser)
    # def do_unsetg(self, args):
    #     """
    #     Unset global value of an option
    #     """
    #     selectedModule = self._cmd.selectedModule

    #     if selectedModule:
    #         option = args.option.lower()
    #         if selectedModule.isOption(option):
    #             if selectedModule.isModuleOption(option):
    #                 selectedModule.options[option].value = None
    #             else: #is a valid slurm option
    #                 selectedModule.slurm.options[option].value = None
    #                 setattr(selectedModule.slurm, option, None)

    #             #delete option:value from global values
    #             if option in self._cmd.gvalues:
    #                 del self._cmd.gvalues[option]
    #             else:
    #                 print_status("{option.upper()} value is not a global value")

    #         else:
    #             print_failure(f"No {option.upper()} option in {selectedModule.mname} module")

    #     else:
    #         print_failure("No module selected")


    # setvg_parser = argparse.ArgumentParser()
    # setvg_parser.add_argument("option", help="Option to set value")
    # setvg_parser.add_argument("value", help="Value of option")

    # @with_argparser(setvg_parser)
    # def do_setvg(self, args):
    #     """
    #     Set globally a value to an valid option
    #     """
    #     #import pdb; pdb.set_trace()

    #     selectedModule = self._cmd.selectedModule

    #     if selectedModule:
    #         option = args.option.lower()
    #         value = args.value

    #         try:
    #             value = int(value)

    #         except ValueError: # value is a string
    #             if value in ["True", "False"]:
    #                 if value == "True":
    #                     value = True
    #                 else:
    #                     value = False

    #         if selectedModule.isOption(option):
    #             if selectedModule.isModuleOption(option): #option is a valid module option
    #                 selectedModule.options[option].value = value

    #             else: #option is a valid slurm option
    #                 argument = selectedModule.slurm.options.get(option)
    #                 argument.value = value
    #                 selectedModule.slurm.options[option] = argument
    #                 setattr(selectedModule.slurm, option, value)

    #             self._cmd.selectedModule = selectedModule
    #             self._cmd.gvalues[option] = value
    #         else:
    #             print_failure(f"No {option.upper()} option in {selectedModule.mname} module")

    #     else:
    #         print_failure("No module selected")


    #setv_parser = argparse.ArgumentParser()
    setv_parser = Cmd2ArgumentParser()
    setv_parser.add_argument("option", help="Option to set value")
    setv_parser.add_argument("value",  completer=Cmd.path_complete, help="Value of option")
    setv_parser.add_argument('-q', '--quiet', action='store_true', help="Set value quietly")
    setv_parser.add_argument('-pre', '--pre-module', dest='pre_module', action='store_true',
                                help="Set value to pre attack module option")
    setv_parser.add_argument('-post', '--post-module', dest='post_module', action='store_true',
                                help="Set value to post attack module option")


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
            if self._cmd.selectedModule:
                if isinstance(self._cmd.selectedModule, Auxiliary):
                    self._cmd.selectedModule.setv(args.option, args.value, args.quiet,
				                  pre_module = args.pre_module,
				                  post_module = args.post_module)
                else:
                    self._cmd.selectedModule.setv(args.option, args.value, args.quiet,
				                  pre_attack = args.pre_module,
				                  post_attack = args.post_module)
            else:
                print("No module was selected") # failure

        except Exception as error:
            print(error) # failure

    def _module_setv(self, selected_module: Module):

        setv_parser = Cmd2ArgumentParser()
        module_options = selected_module.options.keys()
        setv_parser.add_argument("option", choices=module_options,
                                 help="Option to set value")

        # def choice_values(prefix, parsed_args):
        #     choices = selected_module.options[parsed_args.option].choices
        #     if choices:
        #         return (choice for choice in choices if choice.startwith(prefix))
        #     else:
        #         return []

        #setv_parser.add_argument("value", completer=Cmd.path_complete, help="Value of option")#.completer = choice_values

        # #parsed_args = setv_parser.parse_known_args()
        # #print(f"Parsed args: {parsed_args}")
        # selected_option = selected_module.options[parsed_args.option]

        # if selected_option.choices:
        #     setv_parser.add_argument("value", choices=selected_module.choices,
        #                              help="Value of option")
        # else:

        setv_parser.add_argument("value",  completer=Cmd.path_complete, help="Value of option")

        setv_parser.add_argument('-q', '--quiet', action='store_true', help="Set value quietly")
        setv_parser.add_argument('-pre', '--pre-module', dest='pre_module', action='store_true',
                                 help="Set value to pre attack module option")
        setv_parser.add_argument('-post', '--post-module', dest='post_module', action='store_true',
                                 help="Set value to post attack module option")

        #argcomplete.autocomplete(setv_parser)

        @with_argparser(setv_parser)
        def do_setv(cmd2_app:Cmd, args):
            try:
                if cmd2_app.selectedModule:
                    cmd2_app.selectedModule.setv(args.option, args.value,
                                                  args.quiet,
        	                                  pre_module = args.pre_module,
        			                  post_module = args.post_module)
                else:
                    print("No module was selected") #print_failure

            except Exception as error:
                print(error) #print_failure


        return do_setv


    def do_back(self, args):
        """
        Stop interaction with selected module
        """
        self._cmd.selectedModule = None
        self._cmd.prompt = "ama > "
        #self._cmd.do_setv = do_setv

    attack_parser = argparse.ArgumentParser()
    attack_parser.add_argument('-d', '--depends', nargs='*', default=[],
                               help="Process dependency")
    attack_parser.add_argument('-m', '--main-thread', dest='main_thread',
                               action='store_true',
                               help="Run in the main thread (Interactive process)")
    attack_parser.add_argument('-q', '--quiet', action='store_true',
                               help="Run quietly")

    #debugged - date: feb 27 2021
    @with_argparser(attack_parser)
    def do_attack(self, args):
        """
        Perform an attack with the selected attack module
        """
        try:
            #import pdb; pdb.set_trace()
            selectedModule = self._cmd.selectedModule
            if selectedModule is None:
                raise Exception("No module selected")

            if isinstance(selectedModule, Attack):
                if args.main_thread:
                    if not selectedModule.exec_main_thread:
                        print(f"[*] Default execution mode of {selectedModule.MNAME} module: exec_main_thread=False")

                    pre_module_output = None
                    if selectedModule.pre_module:
                        pre_module_output = selectedModule.pre_module.run(quiet=args.quiet)

                    attack_output = selectedModule.attack(quiet=args.quiet, pre_attack_output = pre_module_output)

                    if selectedModule.post_module:
                        selectedModule.post_module.run(quiet=args.quiet)

                else:
                    pre_attack_id = None
                    if selectedModule.pre_module:
                        pre_attack_output = selectedModule.pre_module.options['ROUTPUT'].value
                        pre_attack_name = selectedModule.pre_module.options['JOB_NAME'].value
                        pre_attack_id = self._cmd.manager.submit(target=selectedModule.pre_module.run,
                                                                 args=(args.quiet,), name=pre_attack_name,
                                                                 depends=args.depends, output=pre_attack_output)


                    attack_depends = []
                    if pre_attack_id:
                        attack_depends += [pre_attack_id]

                    attack_output = selectedModule.options['ROUTPUT'].value
                    attack_name = selectedModule.options['JOB_NAME'].value
                    attack_id = self._cmd.manager.submit(target=selectedModule.attack,
                                                         args=(args.quiet,), name=attack_name,
                                                         depends=attack_depends, output=attack_output)


                    if selectedModule.post_module:
                        post_attack_output = selectedModule.post_module.options['ROUTPUT'].value
                        post_attack_name = selectedModule.post_module.options['JOB_NAME'].value
                        self._cmd.manager.submit(target=selectedModule.post_module.run,
                                                 args=(args.quiet,), name=post_attack_name,
                                                 depends=[attack_id], output=post_attack_output)


            else: # selectedModule is an instance of Attack
                print_failure(f"No attack method for {ColorStr(selectedModule.MNAME).StyleBRIGHT} module")
                if isinstance(selectedModule, Auxiliary):
                    print_status(f"Try with {ColorStr('run').StyleBRIGHT} command")

        except Exception as error:
            print(error)


    # #debugged - data: feb 27 2021
    auxiliary_parser = argparse.ArgumentParser()
    auxiliary_parser.add_argument('-q', '--quiet', action='store_true',
                                  help="Run quietly")

    auxiliary_parser.add_argument('-d', '--depends', nargs='*', default=[],
                                  help="Process dependency")
    auxiliary_parser.add_argument('-m', '--main-thread', dest='main_thread',
                                  action='store_true',
                                  help="Run in the main thread (Interactive process)")

    @with_argparser(auxiliary_parser)
    def do_run(self, args):
        """
        Run the selected auxiliary module
        """
        #import pdb; pdb.set_trace()
        try:
            selectedModule = self._cmd.selectedModule
            if selectedModule is None:
                raise Exception("No module selected")

            if isinstance(selectedModule, Auxiliary):
                if args.main_thread:
                    if not selectedModule.exec_main_thread:
                        print(f"[*] Default execution mode of {selectedModule.MNAME} module: exec_main_thread=False")
                    selectedModule.run(quiet=args.quiet)

                else:
                    output = selectedModule.options['ROUTPUT'].value
                    name = selectedModule.options['JOB_NAME'].value
                    self._cmd.manager.submit(target=selectedModule.run, args=(args.quiet,), name=name,
                                         depends=args.depends, output=output)
            else: # selectedModule is an instance of Attack
                print_failure(f"No run method for {ColorStr(selectedModule.MNAME).StyleBRIGHT} module")
                if isinstance(selectedModule, Attack):
                    print_status(f"Try with {ColorStr('attack').StyleBRIGHT} command")

        except Exception as error:
            print(error)
