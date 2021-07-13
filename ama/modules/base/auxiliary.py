#!/usr/bin/env python3
#
# base class to build auxiliary  modules
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


from typing import (
    List,
    Any
)


from ama.modules.base import Module

class Auxiliary(Module):
    """
    Base class to build auxiliary modules
    """
    def __init__(self, *,
                 mname: str, authors: List[str],
                 description: str, fulldescription: str, references: List[str],
                 auxiliary_options: dict, exec_main_thread:bool = False,
		 pre_module:Module = None, post_module:Module = None):

        init_options = {
            'mname': mname,
            'authors': authors,
            'description': description,
            'fulldescription': fulldescription,
            'references': references,
            'options': auxiliary_options,
	    'pre_module': pre_module,
	    'post_module': post_module,
            'exec_main_thread': exec_main_thread
        }

        super().__init__(**init_options)

    def run(self, *args, **kwargs):
        """
        Default method to run auxiliary module
        """
        pass

    execute = run
