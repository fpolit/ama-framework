#!/usr/bin/env python3
#
# base class to build pre attack  modules
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


from .auxiliary import Auxiliary


class PreAttack(Auxiliary):
    """
    Base class to build pre attack modules
    """
    def __init__(self, *,
                 mname: str, author: List[str],
                 description: str, fulldescription: str, references: List[str],
                 pre_attack_options: dict, slurm):

        init_options = {
            'mname': mname,
            'author': author,
            'description': description,
            'fulldescription': fulldescription,
            'references': references,
            'auxiliary_options': pre_attack_options,
            'slurm': slurm
        }

        super().__init__(**init_options)

        def run(self, *args, **kwargs):
        """
        Default method to run pre attack module
        """
        pass
