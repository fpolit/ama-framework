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

from ama.core.slurm import Slurm

class Module:
    """
    base class to build ama modules
    """

    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldescription: str, references: List[str],
                 options: dict, slurm):

        self.mname = mname
        self.author = author
        self.description = description
        self.fulldesciption = fulldescription
        self.options = options
        self.references = references
        self.slurm = slurm


    def setv(self, option, value, quiet: bool = False):
        """
        set option of a module with supplied value
        """
        try:
            option = option.lower()

            try:
                value = int(value)

            except ValueError: # value is a string
                if value in ["True", "False"]:
                    if value == "True":
                        value = True
                    else:
                        value = False

            #import pdb; pdb.set_trace()
            if self.isOption(option):
                if self.isModuleOption(option):
                    self.options[option].value = value

                else: # option is a slurm option
                    if isinstance(self.slurm, Slurm):
                        self.slurm.set_option(option, value)
                    else:
                        raise Exception(f"{self.mname} doesn't support slurm")

                if not quiet:
                    print(f"{option.upper()} => {value}")
            else:
                raise Exception(f"{self.mname} module hasn't {option.upper()} option.")

        except Exception as error:
            print_failure(error)


    def info(self):
        """
        Show information about the module
        """
        # module head
        info_msg = self.info_head()

        # module options
        info_msg += self.available_options()

        # module description
        info_msg += self.fulldesciption_module()

        # module references
        info_msg += self.available_references()

        return info_msg


    def fulldesciption_module(self):
        fulldescription = f"\n\nDescription:\n{self.fulldesciption}"
        return fulldescription

    def info_head(self):
        head = f"""
   Name : {self.description}
 Module : {self.mname}
License : GPLv3

  Author:
            """
        for author in self.author:
            head += f"{author}\n"

        return head


    def available_references(self):
        """
        Return a formatted string with all the supplied references
        """
        references_msg = ""
        if self.references:
            for reference in self.references:
                references_msg += f"\t{reference}\n"

            references_msg = f"\nReferences:\n{references_msg}"

        return references_msg

    def available_options(self, *, required=False, only_slurm=None, only_module=None):
        """
        Show available options of a module
        """

        #import pdb; pdb.set_trace()
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

    def get_no_empty_options(self, required:bool = False):

        module_no_empty_options = {}
        if required:
            module_no_empty_options =  {name: argument.value
                                        for name, argument in self.options.items()
                                        if argument.value is not None and argument.required}
        else:
            module_no_empty_options =  {name: argument.value
                                        for name, argument in self.options.items() if argument.value is not None}

        slurm_no_empty_options = {}
        if self.slurm:
            if required:
                slurm_no_empty_options = {name: argument.value
                                          for name,  argument in self.slurm.options.items()
                                          if argument.value is not None and argument.required}
            else:
                slurm_no_empty_options = {name: argument.value
                                          for name,  argument in self.slurm.options.items() if argument.value is not None}

        return {**module_no_empty_options, **slurm_no_empty_options}


    def required_options(self, local=False):
        #import pdb; pdb.set_trace()
        required_module_args = {name: option
                                for name, option in self.options.items() if option.required}

        required_slurm_args = {}
        if not local:
            if self.slurm:
                required_slurm_args = {name: option
                                       for name, option in self.slurm.options.items() if option.required}

        required_args = {**required_module_args, **required_slurm_args}

        return required_args

    # debugged - date : Mar 1 2021
    def no_empty_required_options(self, local=False):
        #import pdb; pdb.set_trace()

        required_args = self.required_options()

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
