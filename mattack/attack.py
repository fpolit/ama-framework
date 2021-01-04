#!/usr/bin/env python3

import argparse
from .core import MaskAttack


def main():
    parser = argparse.ArgumentParser(description="Mask Attack", prog='mattack')

    parser.add_argument('hash',
                            help='Hash file to crack')

    parser.add_argument('-m', '--masks',
                        help='Mask File to perform Mask Attack')

    parser.add_argument('-f', '--format',
                        help='Hash format (jtr or hashcat hash)')

    # parser.add_argument('-s', '--search', type=str, default=None,
    #                     help='Search by a hash format')

    # HPC parameters
    hpc_parser = parser.add_argument_group('HPC Slurm',
                                        'Options to submit a parallel task in slurm')
    
    hpc_parser.add_argument('-g', '--gpu', type=int, default=0,
                        help='Number of GPU nodes')

    hpc_parser.add_argument('-N', '--nodes', type=int, default=1,
                        help='Number of nodes')

    hpc_parser.add_argument('-n', '--ntasks', type=int, default=1,
                        help='Number of tasks(MPI process)')

    hpc_parser.add_argument('-p', '--partition', type=str, default=None,
                        help='Slurm Partition')

    hpc_parser.add_argument('-t', '--cpusPerTask', type=int, default=1,
                    help='Number of tasks per CPU(OMP Threads)')

    hpc_parser.add_argument('--memPerCpu', type=str, default="4GB",
                help='Memory per CPU(node)')

    hpc_parser.add_argument('-j', '--jobname', type=str, default="mattack",
                        help='Slurm Job Name')

    hpc_parser.add_argument('-o', '--output', type=str, default=None,
                        help='Slurm Output File Name')

    hpc_parser.add_argument('-e', '--error', type=str, default=None,
                        help='Slurm Error File Name')

    hpc_parser.add_argument('--slurm', type=str, default="mattack.slurm",
                        help='Slurm Submit Script Name')

    hpc_parser.add_argument('--time', type=str, default=None,
                        help='Maximum time to perform the attack(HH:MM:SS)')


    
    # subparser = parser.add_subparsers(help='mattack utilities')

    # # search subparse
    # search_parser = subparser.add_parser('search', help='Search by a valid hash with a given pattern')

    # search_parser.add_argument('pattern', type=str, help='pattern to search hashes', default=None)
    # password_cracker = search_parser.add_mutually_exclusive_group(required=True)
    # password_cracker.add_argument('--jtr', action='store_true')
    # password_cracker.add_argument('--hc', action='store_true')


    # # search subparse
    # check_parser = subparser.add_parser('check', help='Check status of an hash')
    # check_parser.add_argument('hash', type=str, help='Check status of the given hash', default=None)



    args = parser.parse_args()
    masksFile = args.masks
    hashType = args.format
    hashFile = args.hash
    mattack = MaskAttack(masksFile, hashType, hashFile)

    # parameters to perform a parallel mask attack
    gpus        = args.gpu
    nodes       = args.nodes
    ntasks      = args.ntasks
    partition   = args.partition
    cpusPerTask = args.cpusPerTask
    memPerCpu   = args.memPerCpu
    jobName     = args.jobname
    output      = args.output
    error       = args.error
    slurmScript = args.slurm
    time        = args.time

    # performing a parallel mask attack
    mattack.run(gpus, nodes, ntasks, partition, cpusPerTask, memPerCpu,
                jobName, output, error, slurmScript, time)
