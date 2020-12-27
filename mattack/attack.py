#!/usr/bin/env python3

from sbash.core import Bash
import argparse
from fineprint.status import print_status, print_successful, print_failure
import re
import sys
import os
from os.path import dirname, join
import json

from mattack import MaskAttack


def main():
    parser = argparse.ArgumentParser(description="Mask Attack", prog='mattack', usage='%(prog)s [-h] [-m MASKS] [-f HASH_TYPE] hash')
# run(self,memPerCpu=None,
#jobName="slurmJob", slurmScript="mattack"):

    parser.add_argument('-m', '--masks',
                        help='Mask File to perform Mask Attack')

    parser.add_argument('-f', '--format',
                        help='John The Ripper\'s  hash format')

    parser.add_argument('hash',
                        help='hash file to crack')

    parser.add_argument('-s', '--search', type=str, default=None,
                        help='Search by a hash format')

    # HPC parameters
    parser.add_argument('-N', '--nodes', type=int, default=1,
                        help='Number of nodes')

    parser.add_argument('-n', '--ntasks', type=int, default=1,
                        help='Number of tasks(MPI process)')

    parser.add_argument('-p', '--partition', type=str, default=None,
                        help='Slurm Partition')

    parser.add_argument('-t', '--cpusPerTask', type=int, default=1,
                    help='Number of tasks per CPU(OMP Threads)')

    parser.add_argument('--menPerCpu', type=str, default="4GB",
                help='Memory per CPU(node)')

    parser.add_argument('-j', '--jobname', type=str, default="mattack",
                        help='Slurm Job Name')

    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Slurm Output File Name')

    parser.add_argument('-e', '--error', type=str, default=None,
                        help='Slurm Error File Name')

    parser.add_argument('--slurm', type=str, default="mattack.slurm",
                        help='Slurm Submit Script Name')

    parser.add_argument('--time', type=str, default=None,
                        help='Maximum time to perform the attack(HH:MM:SS)')


    args = parser.parse_args()
        masksFile = args.masks
        hashType = args.format
        hashFile = args.hash
        mattack = MaskAttack(masksFile, hashType, hashFile)

        # parameters to perform a parallel mask attack
        nodes = args.nodes
        ntasks = args.ntasks
        partition = args.partition
        cpusPerTask = args.cpusPerTask
        memPerCpu = args.menPerCpu
        jobName = args.jobname
        output = args.output
        error = args.error
        slurmScript = args.slurm
        time = args.time

        # performing a parallel mask attack
        mattack.run(nodes, ntasks, partition, cpusPerTask, memPerCpu,
                    jobName, output, error, slurmScript, time)
