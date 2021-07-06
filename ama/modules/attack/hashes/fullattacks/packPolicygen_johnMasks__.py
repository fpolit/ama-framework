#!/usr/bin/env python3
#
# mask attack using john with pack policygen as pre attack module
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any
from fineprint.status import (
    print_status,
    print_failure,
    print_successful
)

from ama.core.plugins.cracker import John


from ..john_masks import JohnMasks

from ama.core.modules.auxiliary.analysis import PackPolicygen

class PackPolicygen_JohnMasks__(JohnMasks):
    def __init__(self, init_options = None):

        if init_options is None:
            init_options = {
                "pre_attack": PackPolicygen(),
                "post_attack": None
            }

        super().__init__(**init_options)
        self.options['masks_file'].required = False
        self.fulldescription = (
            """
            Perform masks attacks against hashes
            with john using the generated masks by Pack-policygen,
            also this parallel task can be submited in a cluster using Slurm
            """
        )

        # pre attack options
        # if self.selected_pre_attack:
        #     self.selected_pre_attack['output'].value = self.options['masks_file'].value


    def attack(self, local=False, force:bool = False, pre_attack_output: Any = None):
        """
        Masks attack using John the Ripper
        Args:
          local (bool): try to perform the attack locally
        """
        import pdb;pdb.set_trace()
        try:
            if not force:
                self.no_empty_required_options(local)

            jtr = John()

            hash_types  = self.options['hash_type'].value.split(',')

            masks_file = pre_attack_output # name of masks file

            jtr.masks_attack(hash_types = hash_types,
                             hashes_file = self.options['hashes_file'].value,
                             masks_file= masks_file,
                             masks_attack_script= self.options['masks_attack'].value,
                             slurm = self.slurm,
                             local = local)

        except Exception as error:
            print_failure(error)

    def setv(self, option, value, *, pre_attack: bool = False, post_attack: bool = False):
        #import pdb; pdb.set_trace()
        super().setv(option, value, pre_attack = pre_attack, post_attack = post_attack)

        option = option.lower()

        # attack -> pre atack
        if option == "masks_file":
            if self.selected_pre_attack and not (pre_attack or post_attack):
                self.selected_pre_attack.options['output'].value = self.options['masks_file'].value

        # pre atack -> attack
        if option == "output":
            if self.selected_pre_attack and pre_attack:
                self.options['masks_file'].value = self.selected_pre_attack.options['output'].value

