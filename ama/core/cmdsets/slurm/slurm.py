#!/usr/bin/env python3
#
# slurm commands for ama-framework (Slurm Commands Category)
#
# Status
# Maintainer: glozanoa <glozanoa@uni.pe>



import argparse
import cmd2
from cmd2 import (
    Cmd,
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
)


from ..category import CmdsetCategory as Category

@with_default_category(Category.SLURM)
class Slurm(CommandSet):
    """
    Slurm command set
    """

    def do_sinfo(self, args):
        print("Run sinfo cmd")

    def do_squeue(self, args):
        print("Run squeue cmd")

    def do_scancel(self, args):
        print("Run scancel cmd")

    def do_srun(self, args):
        print("Run srun cmd")

    def do_scontrol(self, args):
        print("Run scontrol cmd")

    def do_sbatch(self, args):
        print("Run sbatch cmd")
