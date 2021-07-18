#!/usr/bin/env python3
#
# Base class to build ama modules
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from tabulate import tabulate

from typing import (
    List,
    Any
)

from ama.utils import (
	Argument,
	with_argparser
)

from cmd2 import Cmd

class Module:
    """
    base class to build ama modules
    """

    def __init__(self, *,
                 mname: str, authors: List[str],
                 description: str, fulldescription: str, references: List[str],
                 options: dict, exec_main_thread = False,
                 pre_module = None, post_module = None):
        self.mname = mname
        self.authors = authors
        self.description = description
        self.fulldesciption = fulldescription
        self.options = options
        self.references = references
        self.pre_module = pre_module
        self.post_module = post_module
        self.exec_main_thread = exec_main_thread

    def execute(self, *args, **kwargs):
        """
        Default method to run module
        """
        pass

    def check_required_options(self):
        """
        Check if there is'nt a required option with a empty value,
        otherwise raise a exception
        """
        pass



    def setv(self, option:str, value, quiet:bool = False,
	     pre_module:bool=False, post_module:bool=False):
        """
        Set an option of a module with the supplied value
        """
        try:
            #import pdb; pdb.set_trace()
            if pre_module:
                self.pre_module.setv(option, value, quiet=True)
                print(f"(pre module) {option} => {value}")

            elif post_module:
                self.pre_module.setv(option, value, quiet=True)
                print(f"(post module) {option} => {value}")

            else:
                if self.has_option(option):
                    self.options[option].set_value(value)

                if not quiet:
                    print(f"{option} => {value}")
                else:
                    raise Exception(f"{self.mname} module hasn't {option} option.")

        except Exception as error:
            print(error)


    def get_info(self):
        """
        Show information about the module
        """
        # module head
        info_msg = self.get_info_header()

        # module options
        info_msg += self.options2table()

        # module description
        info_msg += self.get_fulldesciption()

        # module references
        info_msg += self.get_references()

        return info_msg


    def get_fulldesciption(self):
        fulldescription = f"\n\nDescription:\n{self.fulldesciption}"
        return fulldescription

    def get_info_header(self):
        head = f"""
   Name : {self.description}
 Module : {self.mname}
License : GPLv3

 Authors:
            """
        for author in self.authors:
            head += f"{author}\n"

        return head


    def get_references(self):
        """
        Return a formatted string with all the references of the module
        """
        references_msg = ""
        if self.references:
            for reference in self.references:
                references_msg += f"\t{reference}\n"

            references_msg = f"\nReferences:\n{references_msg}"

        return references_msg

    def options2table(self, only_required=False):
        table = ""

        if only_required:
            module_options = [[name, *option.get_attributes()]
                                for name, option in self.options.items() if option.required]
        else:
            module_options = [[name, *option.get_attributes()]
                                for name, option in self.options.items()]

        module_options = tabulate(module_options, headers=["Name", "Current Setting", "Required", "Description"])

        helper_modules ={
            'premodule': None,
            'postmodule': None
        }

        pre_module_options = None
        if self.pre_module:
            pre_module_options = self.pre_module.options2table(only_required)
            helper_modules['premodule'] = self.pre_module.MNAME

        post_module_options = None
        if self.post_module:
            post_module_options = self.post_module.options2table(only_required)
            helper_modules['premodule'] = self.pre_module.MNAME


        table = f"""
Options {self.MNAME} module:

{module_options}
        """

        if self.pre_module or self.post_module:
            helper_modules_table = tabulate(helper_modules.items(), headers=['Type', 'Module'], )


        if pre_module_options:
            table += f"""

Options {self.pre_module.MNAME} module:

{pre_module_options}
            """


        if post_module_options:
            table += f"""

Options {self.post_module.MNAME} module:

{post_module_options}
            """

        return table



    def get_options(self, only_required:bool = False):
        options = {
            'module': {},
            'pre_module': {},
            'post_module': {}
        }

        if only_required:
            options['module'] = {name: option
                                 for name, option in self.options.items() if option.required}
            if self.pre_module:
                options['pre_module'] = {name: option
                                         for name, option in self.pre_module.options.items() if option.required}

            if self.post_module:
                options['post_module'] = {name: option
                                          for name, option in self.post_module.options.items() if option.required}
        else:
            options['module'] = self.options
            if self.pre_module:
                options['pre_module'] = self.pre_module.options

            if self.post_module:
                options['post_module'] = self.post_module.options

        return options

    def has_option(self, option):
        return option in self.options



    # def available_options(self, *, required=False, only_slurm=None, only_module=None):
    #     """
    #     Show available options of a module
    #     """

    #     #import pdb; pdb.set_trace()
    #     options = (
    #         f"""
    #         Module: {self.mname}
    #         """
    #      )

    #     options_header = ["Name", "Current Setting", "Required", "Description"]

    #     if only_slurm and only_module:
    #         print_failure("No avaliable options. Select only one filter (only_slurm or only_module)")

    #     elif only_module: # show only module options (only_module is True)
    #         # module options
    #         module_options_table = self.module_options(required)
    #         module_options_table = tabulate(module_options_table, headers=options_header)
    #         options += f"\nOptions:\n{module_options_table}"

    #     elif only_slurm:
    #         if self.slurm:
    #             # slurm options
    #             slurm_options_table = self.slurm_options(required)
    #             slurm_options_table = tabulate(slurm_options_table, headers=options_header)
    #             options += f"\n\nSlurm Options:\n{slurm_options_table}"

    #     else:
    #         #no filters only_* was supplied, so show all the available options

    #         # module options
    #         module_options_table = self.module_options(required)
    #         module_options_table = tabulate(module_options_table, headers=options_header)
    #         options += f"\nOptions:\n{module_options_table}"

    #         if self.slurm:
    #             # slurm options
    #             slurm_options_table = self.slurm_options(required)
    #             slurm_options_table = tabulate(slurm_options_table, headers=options_header)
    #             options += f"\n\nSlurm Options:\n{slurm_options_table}"

    #     return options



    # def slurm_options(self, required=False):
    #     slurm_options_table = []
    #     if self.slurm:
    #         slurm_options = self.slurm.options
    #         if required:
    #             slurm_options_table = [[name.upper(), *option.get_attributes()]
    #                                    for name, option in slurm_options.items() if option.required]
    #         else:
    #             slurm_options_table = [[name.upper(), *option.get_attributes()]
    #                                    for name, option in slurm_options.items()]

    #     return slurm_options_table

    # def get_no_empty_options(self, required:bool = False):

    #     module_no_empty_options = {}
    #     if required:
    #         module_no_empty_options =  {name: argument.value
    #                                     for name, argument in self.options.items()
    #                                     if argument.value is not None and argument.required}
    #     else:
    #         module_no_empty_options =  {name: argument.value
    #                                     for name, argument in self.options.items() if argument.value is not None}

    #     slurm_no_empty_options = {}
    #     if self.slurm:
    #         if required:
    #             slurm_no_empty_options = {name: argument.value
    #                                       for name,  argument in self.slurm.options.items()
    #                                       if argument.value is not None and argument.required}
    #         else:
    #             slurm_no_empty_options = {name: argument.value
    #                                       for name,  argument in self.slurm.options.items() if argument.value is not None}
