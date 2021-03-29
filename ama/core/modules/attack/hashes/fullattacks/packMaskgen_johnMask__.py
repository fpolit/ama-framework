#!/usr/bin/env python3
#
# mask attack using john with pack maskgen as pre attack module
#
# date: Mar 24 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import Any

from ..john_masks import JohnMasks


class PackMaskgen_JohnMasks__(JohnMasks):
    def __init__(self, init_options):
        super().__init__(**init_options)
        self.options['masks_file'].required = False
        self.fulldescription = (
            """
            Perform masks attacks against hashes
            with john using the generated masks by Pack-maskgen,
            also this parallel task can be submited in a cluster using Slurm
            """
        )

        # pre attack options
        #self.selected_pre_attack.options['output'].value = self.options['masks_file'].value


    def attack(self, local=False, force:bool = False, pre_attack_output: Any = None):
        """
        Masks attack using John the Ripper
        Args:
          local (bool): try to perform the attack locally
        """
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

