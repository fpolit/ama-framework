#!/usr/bin/env python3

import argparse
from configparser import ConfigParser
#from ..cracker import John, Hashcat
#from ..hpc.HPC import HPC
from ..base.FilePath import FilePath
def hattackCLIParser():
    parser = argparse.ArgumentParser(description="Hash attack manager", prog='hattack')

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
    cracker_parser.add_argument('-c', '--cracker', type=str, choices=['hc', 'jtr'],
                                required=True, help="Password Cracker")
    cracker_parser.add_argument('-a', '--attack', type=int,
                                required=True, help="Attack mode")

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

    hpc_parser.add_argument('-j', '--jobname', type=str, default="maskattack",
                        help='Slurm Job Name')

    hpc_parser.add_argument('-o', '--output', type=str, default=None,
                        help='Slurm Output File Name')

    hpc_parser.add_argument('-e', '--error', type=str, default=None,
                        help='Slurm Error File Name')

    hpc_parser.add_argument('-s', '--slurm', type=str, default="mattack.slurm",
                        help='Slurm Submit Script Name')

    hpc_parser.add_argument('-t', '--time', type=str, default=None,
                        help='Maximum time to perform the attack(HH:MM:SS)')

    return parser

def main():

    parser = hattackCLIParser()
    args = parser.parse_args()

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
            memPerCpu   = hpc.get(memPerCpu '4GB')
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
                  jobName     = jobname,
                  output      = output,
                  error       = error,
                  time        = time,
                  slurmScript = slurmScript)

        # password cracker arguments
        attackMode = args.attack
        cracker = args.cracker

    if args.cracker == "jtr":
        John.selectAttack(attackMode = attackMode,
                          hashType = hashType,
                          hashFile = hashFile,
                          wordlist = wordlist,
                          maskFile = maskFile,
                          hpc = hpc)

    elif args.cracker == "hc":
        Hashcat.selectAttack(attackMode = attackMode,
                             hashType = hashType,
                             hashFile = hashFile,
                             wordlist = wordlist,
                             maskFile = maskFile,
                             hpc = hpc)



def debugAttack():
    parser = hattackCLIParser()
    args = parser.parse_args()

    # fundamental arguments
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


    # hpc = HPC(gpus        = gpus,
    #           nodes       = nodes,
    #           ntasks      = ntasks,
    #           partition   = partition,
    #           cpusPerTask = cpusPerTask,
    #           memPerCpu   = memPerCpu,
    #           jobName     = jobname,
    #           output      = output,
    #           error       = error,
    #           time        = time,
    #           slurmScript = slurmScript)


    # password cracker arguments
    attackMode = args.attack
    cracker =  args.cracker

    print("[+] Fundamental arguments.")
    print(f"""
    masksFile = {args.masks}
    hashType = {args.hashType}
    hashFile = {args.hashFile}
    """)


    print("[+] HPC arguments.")
    print(f"""
    gpus        = {args.gpu}
    nodes       = {args.nodes}
    ntasks      = {args.ntasks}
    partition   = {args.partition}
    cpusPerTask = {args.cpusPerTask}
    memPerCpu   = {args.memPerCpu}
    jobName     = {args.jobname}
    output      = {args.output}
    error       = {args.error}
    time        = {args.time}
    slurmScript = {args.slurm}
    """)


    print("[+] Password Cracker arguments.")
    print(f"""
    attackMode = {args.attack}
    cracker =  {args.cracker}
    """)

if __name__ == "__main__":
    debugAttack()
