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
from ..slurm.HPC import HPC

# base modules import
from ..base.FilePath import FilePath

# utilities modules import
from ..utilities.version import get_version

def hattackCLIParser():
    VERSION = get_version()
    parser = argparse.ArgumentParser(description=f"Hash attack manager - {VERSION}", prog='hattack',
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument('hashFile',
                        help="Hash file to crack")

    parser.add_argument('--masks', default=None,
                        help="Masks file or mask")

    parser.add_argument('-wd', '--wordlist', nargs='+', default=None,
                        help="Worlists")

    parser.add_argument('-ht', '--hashType', required=True,
                        help="Hash type (john or hashcat hash)")

    parser.add_argument('-i', '--ifile', default=None,
                        help="Input arguments file")

    # parser.add_argument('-h', '--help',
    #                     help='show help')

    # parser.add_argument('-v', '--version', action='store_true', default=False,
    #                     help='show hattack version')


    # Password cracker parameters
    cracker_parser = parser.add_argument_group("Password Cracker arguments")
    cracker_parser.add_argument('-cr', '--cracker', type=str, choices=PasswordCracker.crackers,
                                required=True, help="Password Cracker")

    helpAttackMode = ""

    #john attack modes
    helpAttackMode += tabulate(John.attackMode.items(), headers=["#", "john attacks"])
    helpAttackMode += "\n\n"

    #hashcat attack modes
    helpAttackMode += tabulate(Hashcat.attackMode.items(), headers=["#", "hashcat attacks"])
    helpAttackMode += "\n"

    cracker_parser.add_argument('--attack', type=int,
                                required=True,
                                help=f"{helpAttackMode}")

    cracker_parser.add_argument('--minlength', type=int, default=1,
                                help="minimum mask length(incremental mode)")

    cracker_parser.add_argument('--maxlength', type=int,
                                help="maximum mask length(incremental mode)")


    # slurm parameters
    slurm_parser = parser.add_argument_group("Slurm arguments",
                                        "Options to submit a parallel tasks in slurm")


    slurm_parser.add_argument('-a', '--array',
                              help="array job")

    slurm_parser.add_argument('-A', '--account',
                              help="account name")

    slurm_parser.add_argument('-d', '--dependency',
                              help="dependency list")

    slurm_parser.add_argument('-D', '--chdir',
                              help="homework directory")

    slurm_parser.add_argument('-e', '--error',
                              help="error file")

    slurm_parser.add_argument('-J', '--jobName',
                              help="job name")

    slurm_parser.add_argument('-M', '--cluster',
                              help="cluster name")

    slurm_parser.add_argument('-m', '--distribution',
                              choices=["block", "cyclic",
                                       "plane", "arbitrary"],
                              help="distribution method")

    slurm_parser.add_argument('--mailType',
                              choices=["BEGIN", "END", "FAIL",
                                       "ALL", "TIME_LIMIT"],
                              help="email notification type")

    slurm_parser.add_argument('--mailUser',
                              help="email to receive notifications")

    slurm_parser.add_argument('--mem',
                             help="memory per node (SIZE[K|M|G|T])")

    slurm_parser.add_argument('--memPerCpu',
                              help="memory per cpu (SIZE[K|M|G|T])")

    slurm_parser.add_argument('-c', '--cpusPerTask',
                              help="cpus number per task")

    slurm_parser.add_argument('-N', '--nodes',
                              help="nodes number")

    slurm_parser.add_argument('-n', '--ntasks',
                            help="tasks number")

    slurm_parser.add_argument('--nice', type=int,
                              help="adjustment of schedule priority")

    slurm_parser.add_argument('--output',
                              help="output file")

    slurm_parser.add_argument('--open-mode',
                              choices=["append", "truncate"],
                              help="open mode of output and error files")

    slurm_parser.add_argument('-p', '--partition',
                              help="slurm partition")

    slurm_parser.add_argument('-res','--reservation',
                              help="slurm reservation")

    slurm_parser.add_argument('-t', '--time',
                              help="time limit on job allocation (DD-HH:MM:SS)")

    slurm_parser.add_argument('--testOnly', action='store_true',
                              help="no submit task")

    slurm_parser.add_argument('-v', '--verbose', action='store_true',
                              help="Increase the verbosity of sbatch's informational messages")

    slurm_parser.add_argument('-w', '--nodelist',
                              help="Request a specific list of hosts")

    slurm_parser.add_argument('-W', '--wait', action='store_true',
                              help="Do  not  exit  until the submitted job terminates")

    slurm_parser.add_argument('-x','--exclude',
                              help="Explicitly exclude certain nodes")


    slurm_parser.add_argument('--pmix', type=str, default='pmix_v3',
                            help="pmix type")

    slurm_parser.add_argument('-s', '--slurm', type=str, default="hattack.slurm",
                        help="Slurm Submit Script Name")

    return parser


def parseSlurmArgs(args):
    # hpc arguments
    array = args.array # -a <e.x: 0-15 or 0,6,16-32>
    account = args.account # -A <account>
    dependency = args.dependency # -d
    chdir = args.chdir # -D <homework directory path>
    error = args.error # -e <error file path>
    jobName = args.jobName # -J <str>
    cluster = args.cluster # -M <cluster name>
    distribution = args.distribution # -m <block|cyclic|plane|arbitrary>
    mailType = args.mailType # NONE <BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>, PP: percent of the limit time
    mailUser = args.mailUser # NONE <user email>
    mem = args.mem # NONE <size[units]>, units = [K|M|G|T] (memory per node)
    memPerCpu = args.memPerCpu # NONE <size[units]>
    cpusPerTask = args.cpusPerTask # -c <ncpus>
    nodes = args.nodes # -N <minnodes[-maxnodes]>
    ntasks = args.ntasks # -n <number of tasks>
    nice = args.nice # NONE <adjustment>, adjustment is between +- 2147483645
    output = args.output # -o <path>
    openMode = args.openMode # NONE <append|truncate>
    partition = args.partition # -p <partition>
    reservation = args.reservation # NONE <reservation>
    time = args.time # -t <time>
    # time formats: MM, MM:SS, HH:MM:SS, DD-HH, DD-HH:MM, DD-HH:MM:SS
    # DD:days, HH:hours, MM: minutes, SS:secconds
    testOnly = args.testOnly # NONE <NO VALUE>,if testOnly=True enable this flag otherwise omit
    verbose = args.verbose # -v <NO VALUE>, if verbose=True enable this flag otherwise omit
    nodelist = args.nodelist # -w <nodelist>, e.x. nodelist = hw[00-04,06,08]
    wait = args.wait # -W <NO VALUE>, if wait=True enable this flag otherwise omit
    exclude = args.exclude # -x <nodelist>


    pmix = args.pmix
    slurmScript = args.slurm

    return HPC(array = array,
               account = account,
               dependency = dependency,
               chdir = chdir,
               error = error,
               jobName = jobName,
               cluster = cluster,
               distribution = distribution,
               mailType = mailType,
               mailUser = mailUser,
               mem = mem,
               memPerCpu = memPerCpu,
               cpusPerTask = cpusPerTask,
               nodes = nodes,
               ntasks = ntasks,
               nice = nice,
               output = output,
               openMode = openMode,
               partition = partition,
               reservation = reservation,
               time = time,
               testOnly = testOnly,
               verbose = verbose,
               nodelist = nodelist,
               wait = wait,
               exclude = exclude,
               pmix = pmix,
               slurmScript = slurm)


def main():

    parser = hattackCLIParser()
    args = parser.parse_args()


    # if args.ifile: # read the argument from a ini file
    #     ifile = args.ifile
    #     ifilePath = FilePath(ifile)
    #     if ifilePath.checkReadAccess():
    #         config = ConfigParser()
    #         config.read(ifilePath)

    #         # fundamental arguments
    #         if config.has_section('cracker') and config.has_section('basic'):
    #             # basic arguments
    #             basic = config['basic']

    #             masksFile = basic.get(masksFile)
    #             hashType = basic.get(hashType)
    #             hashFile = args.hashFile

    #             # password cracker arguments
    #             crack = config['crack']

    #             attackMode = crack.getint(attack, None)
    #             cracker = crack.get(cracker, None)

    #         else:
    #             raise Exception("Insufficient parameters")

    #         # hpc arguments
    #         hpc = config['hpc']
    #         gpus        = hpc.get(gpu, 0)
    #         nodes       = hpc.getint(nodes, 1)
    #         ntasks      = hpc.getint(ntasks, 1)
    #         partition   = hpc.get(partition, None)
    #         cpusPerTask = hpc.getint(cpusPerTask, 1)
    #         memPerCpu   = hpc.get(memPerCpu, '4GB')
    #         jobName     = hpc.get(jobname, 'hashAttack')
    #         output      = hpc.get(output, None)
    #         error       = hpc.get(error, None)
    #         time        = hpc.get(time, None)
    #         slurmScript = hpc.get(slurm, 'hashAttack.slurm')

    #         hpc = HPC(gpus        = gpus,
    #                   nodes       = nodes,
    #                   ntasks      = ntasks,
    #                   partition   = partition,
    #                   cpusPerTask = cpusPerTask,
    #                   memPerCpu   = memPerCpu,
    #                   jobName     = jobname,
    #                   output      = output,
    #                   error       = error,
    #                   time        = time,
    #                   slurmScript = slurmScript)

    #     else:
    #         print_failure(f"No read permission {ifilePath} file")
    #         raise PermissionError
    # else:
    # fundamental arguments
    wordlist = args.wordlist
    masksFile = args.masks
    hashType = args.hashType
    hashFile = args.hashFile

    # password cracker arguments
    attackMode = args.attack
    cracker = args.cracker
    minlength = args.minlength
    maxlength = args.maxlength if args.maxlength else args.minlength

    ## slurm arguments
    hpc = parseSlurmArgs(args)

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
