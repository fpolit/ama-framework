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


from ama.utils import Argument
from .auxiliary import Auxiliary
from .module import Module


class Attack(Module):
    """
    Base class to build attack modules
    """
    def __init__(self, *,
                 mname: str, authors: List[str],
                 description: str, fulldescription: str, references: List[str],
                 attack_options: dict, exec_main_thread:bool = False,
                 pre_attack:Auxiliary = None, post_attack:Auxiliary = None):


        pre_attack_name = pre_attack.MNAME if isinstance(pre_attack, Module) else None
        post_attack_name = post_attack.MNAME if isinstance(post_attack, Module) else None

        self.helper_modules = {
            'pre_attack': Argument(pre_attack_name, False, "Pre attack module"),
            'post_attack': Argument(post_attack_name, False, "Post attack module")
        }

        init_options = {
            'mname': mname,
            'authors': authors,
            'description': description,
            'fulldescription': fulldescription,
            'references': references,
            'options': attack_options,
            'pre_module': pre_attack,
            'post_module': post_attack,
            'exec_main_thread': exec_main_thread
        }

        super().__init__(**init_options)


    def setv(self, option, value, quiet: bool=False, pre_attack: bool = False, post_attack: bool = False):
        """
        set option of attack module with supplied value
        """
        #import pdb; pdb.set_trace()
        try:
            if pre_attack:
                self.pre_module.setv(option, value, quiet=True)
                print(f"(preattack) {option.upper()} => {value}")

            elif post_attack:
                self.post_module.setv(option, value, quiet=True)
                print(f"(postattack) {option.upper()} => {value}")

            else: # set option of attack module
                super().setv(option, value)

        except Exception as error:
            print(error)



    def __repr__(self):
        pre_attack = self.pre_module
        post_attack = self.post_module

        return f"Attack(preattack={pre_attack}, attack={type(self)}, postattack={post_attack})"

    def attack(self, *args, **kwargs):
        """
        Default method to perform attack module
        """
        pass

    def check_required_options(self):
        if self.pre_attack:
            self.pre_attack.check_required_options()

        if self.post_attack:
            self.post_attack.check_required_options()

        super().check_required_options()
