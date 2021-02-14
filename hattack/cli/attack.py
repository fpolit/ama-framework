#!/usr/bin/env python3

import sys
import argparse
from argparse import RawTextHelpFormatter
from tabulate import tabulate
from configparser import ConfigParser

# cracker modules import
from ..cracker.PasswordCracker import PasswordCracker
from ..cracker.John import John
from ..cracker.Hashcat import Hashcat

# hpc modules import
from ..hpc.HPC import HPC

# base modules import
from ..base.FilePath import FilePath

# utilities modules import
from ..utilities.version import get_version

def hattackCLIParser():
    VERSION = get_version()
    parser = argparse.ArgumentParser(description=f"Hash attack manager - {VERSION}", prog='hattack',
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument('hashFile',
                            help='Hash file to crack')

    parser.add_argument('-m', '--masks', default=None,
                        help='Masks file or mask')

    parser.add_argument('-w', '--wordlist', nargs='+', default=None,
                        help='Worlist')

    parser.add_argument('-ht', '--hashType', required=True,
                        help='Hash type (john or hashcat hash)')

    parser.add_argument('-i', '--ifile', default=None,
                        help='Input arguments file')

    # parser.add_argument('-h', '--help',
    #                     help='show help')

    # parser.add_argument('-v', '--version', action='store_true', default=False,
    #                     help='show hattack version')


    # Password cracker parameters
    cracker_parser = parser.add_argument_group('Password Cracker arguments')
    cracker_parser.add_argument('-c', '--cracker', type=str, choices=PasswordCracker.crackers,
                                required=True, help="Password Cracker")

    helpAttackMode = ""

    #john attack modes
    helpAttackMode += tabulate(John.attackMode.items(), headers=["#", "john attacks"])
    helpAttackMode += "\n\n"

    #hashcat attack modes
    helpAttackMode += tabulate(Hashcat.attackMode.items(), headers=["#", "hashcat attacks"])
    helpAttackMode += "\n"

    cracker_parser.add_argument('-a', '--attack', type=int,
                                required=True,
                                help=f"{helpAttackMode}")

    cracker_parser.add_argument('--minlength', type=int, default=1,
                                help="minimum mask length(incremental mode)")

    cracker_parser.add_argument('--maxlength', type=int,
                                help="maximum mask length(incremental mode)")


    # HPC parameters
    hpc_parser = parser.add_argument_group('HPC arguments',
                                        'Options to submit a parallel task in slurm')



    hpc_parser.add_argument('-a', '--array',
                            help='array job')

    hpc_parser.add_argument('-A', '--account',
                            help='account name')

    hpc_parser.add_argument('-d', '--dependency',
                            help='dependency list')

    hpc_parser.add_argument('-D', '--chdir',
                            help='homework directory')

    hpc_parser.add_argument('-e', '--error',
                            help='error file')

    hpc_parser.add_argument('-J', '--jobName',
                            help='job name')

    hpc_parser.add_argument('-t', '--time', type=str, default=None,
                            help='Maximum time to perform the attack(HH:MM:SS)')
    hpc_parser.add_argument('-M', '--cluster',
                            help='cluster name')

    hpc_parser.add_argument('-m', '--distribution',
                            choices=['block', 'cyclic',
                                     'plane', 'arbitrary'],
                            help='distribution method')

    hpc_parser.add_argument('--mail-type',
                            choices=['BEGIN', 'END', 'FAIL',
                                     'ALL', 'TIME_LIMIT'],
                            help='email notification type')

    hpc_parser.add_argument('mail-user',
                            help='email to receive notifications')
    hpc_parser.add_argument('mem': self.mem)
    hpc_parser.add_argument('mem-per-cpu': self.memPerCpu)
    hpc_parser.add_argument('nodes': self.nodes)
    hpc_parser.add_argument('ntasks': self.ntasks)
    hpc_parser.add_argument('nice': self.nice)
    hpc_parser.add_argument('output': self.output)
    hpc_parser.add_argument('open-mode': self.openMode)
    hpc_parser.add_argument('partition': self.partition)
    hpc_parser.add_argument('reservation': self.reservation)
    hpc_parser.add_argument('time': self.time)
    hpc_parser.add_argument('test-only': self.testOnly)
    hpc_parser.add_argument('verbose': self.verbose)
    hpc_parser.add_argument('nodelist': self.nodelist)
    hpc_parser.add_argument('wait': self.wait)
    hpc_parser.add_argument('exclude':self.exclude)
    hpc_parser.add_argument('cpus-per-task': self.cpusPerTask)



    # hpc_parser.add_argument('-g', '--gpu', type=int, default=0,
    #                     help='Number of GPU nodes')

    # hpc_parser.add_argument('-N', '--nodes', type=int, default=1,
    #                     help='Number of nodes')

    # hpc_parser.add_argument('-n', '--ntasks', type=int, default=1,
    #                     help='Number of tasks(MPI process)')

    # hpc_parser.add_argument('-p', '--partition', type=str, default=None,
    #                     help='Slurm Partition')

    # hpc_parser.add_argument('-ct', '--cpusPerTask', type=int, default=1,
    #                 help='Number of tasks per CPU(OMP Threads)')

    # hpc_parser.add_argument('-mc', '--memPerCpu', type=str, default="1GB",
    #             help='Memory per CPU(node)')

    # hpc_parser.add_argument('-j', '--jobname', type=str, default="hattack",
    #                     help='Slurm Job Name')

    # hpc_parser.add_argument('-o', '--output', type=str, default=None,
    #                     help='Slurm Output File Name')

    # hpc_parser.add_argument('-e', '--error', type=str, default=None,
    #                     help='Slurm Error File Name')

    # hpc_parser.add_argument('-s', '--slurm', type=str, default="hattack.slurm",
    #                     help='Slurm Submit Script Name')

    # hpc_parser.add_argument('-t', '--time', type=str, default=None,
    #                     help='Maximum time to perform the attack(HH:MM:SS)')

    hpc_parser.add_argument('--pmix', type=str, default='pmix_v3',
                            help='pmix type')

    hpc_parser.add_argument('-s', '--slurm', type=str, default="hattack.slurm",
                        help='Slurm Submit Script Name')

    return parser

def main():

    parser = hattackCLIParser()
    args = parser.parse_args()

    # if args.version:
    #     print_status(f"hattach version: {get_version()}")
    #     sys.exit(1)

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
        pmix         = args.pmix
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
                  pmix        = pmix,
                  slurmScript = slurmScript)

        # password cracker arguments
        attackMode = args.attack
        cracker = args.cracker
        minlength = args.minlength
        maxlength = args.maxlength if args.maxlength else args.minlength

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
