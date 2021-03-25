#!/usr/bin/env python3
#
# base class to build attack modules
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from tabulate import tabulate

from typing import (
    List,
    Any
)

# base imports
from ama.core.modules.base import Module

# table formation imports
from cmd2.table_creator import (
    Column,
    SimpleTable
)

from fineprint.status import (
    print_failure
)

# validator
from ama.core.validator import Args

class Attack(Module):
    """
    Base class to build attack modules
    """
    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldescription: str, references: List[str],
                 attack_options: dict, slurm,
                 pre_attack, post_attack):


        self.selected_pre_attack = pre_attack # Instance of selected pre attack class
        self.selected_post_attack = post_attack # Instance of selected post attack class

        init_options = {
            'mname': mname,
            'author': author,
            'description': description,
            'fulldescription': fulldescription,
            'references': references,
            'options': attack_options,
            'slurm': slurm
        }

        self.init_options = init_options

        super().__init__(**init_options)

    def attack(self, *args, **kwargs):
        """
        Default method to run attack module
        """
        pass

    # def get_init_options(self):
    #     init_options = self.init_options.copy()
    #     init_options['attack_options'] = init_options['options']
    #     del init_options['options']
    #     return init_options

    def no_empty_required_options(self, local=False):
        #import pdb; pdb.set_trace()
        required_module_options = self.required_options(local)

        required_pre_attack_options = {}
        if self.selected_pre_attack:
            required_pre_attack_options = self.selected_pre_attack.required_options(local)

        required_post_attack_options = {}
        if self.selected_post_attack:
            required_post_attack_options = self.selected_post_attack.required_options(local)

        required_args = {
            **required_module_options,
            **required_pre_attack_options,
            **required_post_attack_options
        }

        Args.no_empty_required_options(**required_args)

    def isAttackOption(self, option):
        if option in self.options:
            return True
        return False

    def info(self):
        """
        Show information about the module
        """
        # module head
        info_msg = self.info_head()

        # module options
        info_msg += self.available_options()

        # # pre attack module options
        # if selected_pre_attack := self.selected_pre_attack:
        #     info_msg += selected_pre_attack.available_options()

        # # post attack module options
        # if selected_post_attack := self.selected_post_attack:
        #     info_msg += selected_post_attack.available_options()

        # module description
        info_msg += self.fulldesciption_module()

        # module references
        info_msg += self.available_references()

        return info_msg

    def available_options(self, *, required=False, only_slurm=None, only_module=None):
        """
        Show available options of a module
        """

        import pdb; pdb.set_trace()

        options = (
            f"""
            Module: {self.mname}
            """
         )

        options_header = ["Name", "Current Setting", "Required", "Description"]

        if only_slurm and only_module:
            print_failure("No avaliable options. Select only one filter (only_slurm or only_module)")

        elif only_module: # show only module options (only_module is True)
            # module options
            module_options_table = self.module_options(required)
            module_options_table = tabulate(module_options_table, headers=options_header)
            options += f"\nOptions:\n{module_options_table}"

        elif only_slurm:
            if self.slurm:
                # slurm options
                slurm_options_table = self.slurm_options(required)
                slurm_options_table = tabulate(slurm_options_table, headers=options_header)
                options += f"\n\nSlurm Options:\n{slurm_options_table}"

        else:
            #no filters only_* was supplied, so show all the available options

            # module options
            module_options_table = self.module_options(required)
            module_options_table = tabulate(module_options_table, headers=options_header)
            options += f"\nOptions:\n{module_options_table}"

            if self.slurm:
                # slurm options
                slurm_options_table = self.slurm_options(required)
                slurm_options_table = tabulate(slurm_options_table, headers=options_header)
                options += f"\n\nSlurm Options:\n{slurm_options_table}"


        # pre attack options
        if selected_pre_attack := self.selected_pre_attack:
            options += "\n"
            options += selected_pre_attack.available_options(required = required,
                                                             only_slurm = only_slurm,
                                                             only_module = only_module)

        # post attack options
        if selected_post_attack := self.selected_post_attack:
            options += "\n"
            options += selected_post_attack.available_options(required = required,
                                                             only_slurm = only_slurm,
                                                             only_module = only_module)

        return options

