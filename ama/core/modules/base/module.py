#!/usr/bin/env python3
#
# base class to build ama modules
#
# Module class implementation - date: Feb 28 2021
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from tabulate import tabulate

from typing import (
    List,
    Any
)

# fineprint imports
from fineprint.status import (
    print_status,
    print_failure,
    print_successful
)

# validator import
from ama.core.validator import Args

class Module:
    """
    base class to build ama modules
    """

    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldescription: str,
                 options: dict, slurm):

        self.mname = mname
        self.author = author
        self.description = description
        self.fulldesciption = fulldescription
        self.options = options
        self.slurm = slurm


    def info(self):
        """
        Show information about the module
        """
        info_msg = \
            f"""
   Name : {self.description}
 Module : {self.mname}
License : GPLv3

  Author:
            """
        for author in self.author:
            info_msg += f"{author}\n"

        info_msg += self.available_options()

        # description module
        info_msg += f"\n\nDescription:\n{self.fulldesciption}"

        return info_msg


    def available_options(self, *, required=False, only_slurm=None, only_module=None):
        """
        Show available options of a module
        """

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

        return options


    def module_options(self, required=False):
        if required:
            module_options_table = [[name.upper(), *option.get_attributes()]
                                    for name, option in self.options.items() if option.required]
        else:
            module_options_table = [[name.upper(), *option.get_attributes()]
                                    for name, option in self.options.items()]

        return module_options_table



    def slurm_options(self, required=False):
        slurm_options_table = []
        if self.slurm:
            slurm_options = self.slurm.options
            if required:
                slurm_options_table = [[name.upper(), *option.get_attributes()]
                                       for name, option in slurm_options.items() if option.required]
            else:
                slurm_options_table = [[name.upper(), *option.get_attributes()]
                                       for name, option in slurm_options.items()]

        return slurm_options_table


    def no_empty_required_options():
        import pdb; pdb.set_trace()
        required_module_args = {name: option
                                for name, options in self.options if option.required}

        required_slurm_args = {}
        if self.slurm:
            required_slurm_args = {name: option
                                   for name, options in self.slurm.options if option.required}


        required_args = {**required_module_args, **required_slurm_args}

        Args.no_empty_required_options(**required_args)

    def isModuleOption(self, option):
        if option in self.options:
            return True
        return False

    def isOption(self, option):
        if self.slurm: #module that support slurm
            if option in self.options or \
               option in self.slurm.options:
                return True
        else: #module that doesn't support slurm
            if option in self.options:
                return True

        return False

    def isSlurmOption(self, option):
        if self.slurm:
            if option in self.slurm.options:
                return True
        return False
