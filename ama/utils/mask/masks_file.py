#!/usr/bin/env python3

import os
from fineprint.status import print_failure


from pathlib import Path
from ama.utils.mask import Mask


class MasksFile(Path):
    def __init__(self, mask_file):
        super().__init__(mask_file)

    @staticmethod
    def is_mask_file(path_file):
        masks = MaskFile(path_file)
        with open(masks, 'r') as masks_file:
            while mask := masks_file.readline().rstrip():
                    if not Mask.is_mask(mask):
                        return False
        return True

    @staticmethod
    def get_masks(masks_file:Path):
        masks = []
        with open(masks_file, 'r') as _masks_file:
            while mask := _masks_file.readline().rstrip():
                if Mask.is_mask(mask):
                    masks.append(mask)

        return masks
