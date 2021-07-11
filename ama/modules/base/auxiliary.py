#!/usr/bin/env python3
#
# base class to build auxiliary  modules
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


class Auxiliary(Module):
    """
    Base class to build auxiliary modules
    """
    def __init__(self, *,
                 mname: str, authors: List[str],
                 description: str, fulldescription: str, references: List[str],
                 auxiliary_options: dict,
				 pre_module:Module = None, post_module:Module = None):

        init_options = {
            'mname': mname,
            'authors': authors,
            'description': description,
            'fulldescription': fulldescription,
            'references': references,
            'options': auxiliary_options,
			'pre_module': pre_module,
			'post_module': post_module
        }

        super().__init__(**init_options)

    def run(self, *args, **kwargs):
        """
        Default method to run auxiliary module
        """
        pass

	execute = run
