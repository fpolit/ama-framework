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

from fineprint.status import print_failure, print_status

from ..category import CmdsetCategory as Category

@with_default_category(Category.SLURM)
class Slurm(CommandSet):
    """
    Base slurm's command set
    """

    def do_sinfo(self, args):
	    try:
		    try:
			    import pyslurm

		    except ModuleNotFoundError as error:
			    print_failure(error)
			    raise Exception("Install PySlurm using depends/pyslurm.py script")
			partitions = pyslurm.parition()

	    except Exception as error:
		    print_failure(error)

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
