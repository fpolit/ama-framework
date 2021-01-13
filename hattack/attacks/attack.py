#!/usr/bin/env python3

import argparse
from argparse import RawTextHelpFormatter

from configparser import ConfigParser

# cracker modules import
from ..cracker.PasswordCracker import PasswordCracker
from ..cracker.John import John
from ..cracker.Hashcat import Hashcat

# hpc modules import
from ..hpc.HPC import HPC

# base modules import
from ..base.FilePath import FilePath


def hattackCLIParser():
    parser = argparse.ArgumentParser(description="Hash attack manager", prog='hattack',
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument('hashFile',
                            help='Hash file to crack')

    parser.add_argument('-m', '--masks', default=None,
                        help='Mask File to perform Mask Attack')

    parser.add_argument('-w', '--wordlist', nargs='?', default=None,
                        help='Worlist')

    parser.add_argument('-ht', '--hashType', required=True,
                        help='Hash type (john or hashcat hash type)')

    parser.add_argument('-i', '--ifile', default=None,
                        help='input arguments file')

    # Password cracker parameters
    cracker_parser = parser.add_argument_group('Password Cracker arguments')
    cracker_parser.add_argument('-c', '--cracker', type=str, choices=PasswordCracker.crackers,
                                required=True, help="Password Cracker")

    #import pdb; pdb.set_
    attackModes = {'john': John.attackMode,
                   'hashcat': Hashcat.attackMode}
    helpAttackMode = ""
    for cracker, attackMode in attackModes.items():
        helpAttackMode += f" # | {cracker}\n"
        helpAttackMode +=  "------------\n"
        for attackId, attackInfo in attackMode.items():
            helpAttackMode += f" {attackId} | {attackInfo}\n"
        helpAttackMode += "\n"
    #print(f"helpAttack: {helpAttackMode}")

    cracker_parser.add_argument('-a', '--attack', type=int,
                                required=True,
                                help=f"Attack Mode.\n{helpAttackMode}")

    # HPC parameters
    hpc_parser = parser.add_argument_group('HPC arguments',
                                        'Options to submit a parallel task in slurm')
    hpc_parser.add_argument('-g', '--gpu', type=int, default=0,
                        help='Number of GPU nodes')

    hpc_parser.add_argument('-N', '--nodes', type=int, default=1,
                        help='Number of nodes')

    hpc_parser.add_argument('-n', '--ntasks', type=int, default=1,
                        help='Number of tasks(MPI process)')

    hpc_parser.add_argument('-p', '--partition', type=str, default=None,
                        help='Slurm Partition')

    hpc_parser.add_argument('-ct', '--cpusPerTask', type=int, default=1,
                    help='Number of tasks per CPU(OMP Threads)')

    hpc_parser.add_argument('-mc', '--memPerCpu', type=str, default="4GB",
                help='Memory per CPU(node)')

    hpc_parser.add_argument('-j', '--jobname', type=str, default="hashattack",
                        help='Slurm Job Name')

    hpc_parser.add_argument('-o', '--output', type=str, default=None,
                        help='Slurm Output File Name')

    hpc_parser.add_argument('-e', '--error', type=str, default=None,
                        help='Slurm Error File Name')

    hpc_parser.add_argument('-s', '--slurm', type=str, default="hashattack.slurm",
                        help='Slurm Submit Script Name')

    hpc_parser.add_argument('-t', '--time', type=str, default=None,
                        help='Maximum time to perform the attack(HH:MM:SS)')


    # help arguments
    # help_parser = parser.add_argument_group('Help arguments',
    #                                     'Options to get help')

    # help_parser.add_argument('-gh', '--getHelp', choices=['attack', 'examples'],
    #                          help='Get help of specific arguments')
    return parser

def main():

    parser = hattackCLIParser()
    args = parser.parse_args()

    # help_parser
    # if args.getHelp:
    #     helpme = args.getHelp
    #     if helpme == 'attack':
    #         attackModes = {'john': John.attackMode,
    #                        'hashcat': Hashcat.attackMode}


    #             print("\n")

    #     elif helpme == 'examples':
    #         pass


    if args.ifile: # read the argument from a ini file
        ifile = args.ifile
        ifilePath = FilePath(ifile)
        if ifilePath.checkReadAccess():
            config = ConfigParser()
            config.read(ifilePath)

            # fundamental arguments
            if config.has_section('cracker') and config.has_section('basic'):
                # basic arguments
                basic = config['basic']

                masksFile = basic.get(masksFile)
                hashType = basic.get(hashType)
                hashFile = args.hashFile

                # password cracker arguments
                crack = config['crack']

                attackMode = crack.getint(attack, None)
                cracker = crack.get(cracker, None)

            else:
                raise Exception("Insufficient parameters")

            # hpc arguments
            hpc = config['hpc']
            gpus        = hpc.get(gpu, 0)
            nodes       = hpc.getint(nodes, 1)
            ntasks      = hpc.getint(ntasks, 1)
            partition   = hpc.get(partition, None)
            cpusPerTask = hpc.getint(cpusPerTask, 1)
            memPerCpu   = hpc.get(memPerCpu, '4GB')
            jobName     = hpc.get(jobname, 'hashAttack')
            output      = hpc.get(output, None)
            error       = hpc.get(error, None)
            time        = hpc.get(time, None)
            slurmScript = hpc.get(slurm, 'hashAttack.slurm')

            hpc = HPC(gpus        = gpus,
                      nodes       = nodes,
                      ntasks      = ntasks,
                      partition   = partition,
                      cpusPerTask = cpusPerTask,
                      memPerCpu   = memPerCpu,
                      jobName     = jobname,
                      output      = output,
                      error       = error,
                      time        = time,
                      slurmScript = slurmScript)

        else:
            print_failure(f"No read permission {ifilePath} file")
            raise PermissionError
    else:
        # fundamental arguments
        wordlist = args.wordlist
        masksFile = args.masks
        hashType = args.hashType
        hashFile = args.hashFile

        # hpc arguments
        gpus        = args.gpu
        nodes       = args.nodes
        ntasks      = args.ntasks
        partition   = args.partition
        cpusPerTask = args.cpusPerTask
        memPerCpu   = args.memPerCpu
        jobName     = args.jobname
        output      = args.output
        error       = args.error
        time        = args.time
        slurmScript = args.slurm

        hpc = HPC(gpus        = gpus,
                  nodes       = nodes,
                  ntasks      = ntasks,
                  partition   = partition,
                  cpusPerTask = cpusPerTask,
                  memPerCpu   = memPerCpu,
                  jobName     = jobName,
                  output      = output,
                  error       = error,
                  time        = time,
                  slurmScript = slurmScript)

        # password cracker arguments
        attackMode = args.attack
        cracker = args.cracker

    if args.cracker in ["john", "jtr"]:
        John.selectAttack(attackMode = attackMode,
                          hashType = hashType,
                          hashFile = hashFile,
                          wordlist = wordlist,
                          masksFile = masksFile,
                          hpc = hpc)

    elif args.cracker in ["hashcat", "hc"]:
        Hashcat.selectAttack(attackMode = attackMode,
                             hashType = hashType,
                             hashFile = hashFile,
                             wordlist = wordlist,
                             masksFile = masksFile,
                             hpc = hpc)
