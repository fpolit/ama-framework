#!/usr/bin/env python3

import sys

from cement import Controller, ex
from cement.utils.version import get_version_banner

from sbash.core import Bash
from fineprint.status import print_status, print_failure, print_successful

class Attack(Controller):
    class Meta:
        label='attack'
        arguments = [
                    # basic parameters
                    (['-m', '--masks'],
                    {'help' : 'Mask File to perform Mask Attack',
                     'required' : 'True'}),
                    (['-f', '--format'],
                    {'help' : 'John The Ripper hash format',
                     'required' : 'True'}),
                    (['hash'],
                    {'help' : 'hash file to crack'}),
                    # HPC parameters
                    (['-N', '--nodes'],
                    {'help' : 'Number of nodes',
                    'default' : '1'}),
                    (['-n', '--ntasks'],
                    {'help' : 'Number of tasks(MPI process)',
                    'default' : '1'}),
                    (['-p', '--partition'],
                    {'help' : 'Slurm Partition',
                    'default' : '1'}),
                    (['-t', '--cpusPerTask'],
                    {'help' : 'Number of tasks per CPU(OMP Threads)',
                    'default' : '1'}),
                    (['--menPerCpu'],
                    {'help' : 'Memory per CPU(node)',
                    'default' : '4GB'}),
                    (['-j', '--jobname'],
                    {'help' : 'Slurm Job Name',
                    'default' : 'mattack'}),
                    (['-o', '--output'],
                    {'help' : 'Slurm Output File Name'}),
                    (['-e', '--error'],
                    {'help' : 'Slurm Error File Name'}),
                    (['-s', '--slurm'],
                    {'help' : 'Slurm Submit Script Name',
                    'default' : 'mattack.slurm'}),
                    (['--time'],
                    {'help' : 'Maximum time to perform the attack(HH:MM:SS)'}),
                ]     
    
    @ex(hide=True)
    def _default(self):
    # def run(self, nodes=None, ntasks=None, partition=None, cpusPerTask=1, memPerCpu=None, 
    #         jobName="mattack", output=None, error=None, slurmScript="mattack.sh", time=None):
        """
            Submit a slurm task
        """
        try:
            # elemental parameter to perform a mask attack
            masksFile       = self.app.pargs.masks
            hashType        = self.app.pargs.format
            hashFile        = self.app.pargs.hash

            # parameters to perform a parallel mask attack
            nodes           = self.app.pargs.nodes
            ntasks          = self.app.pargs.ntasks
            partition       = self.app.pargs.partition
            cpusPerTask     = self.app.pargs.cpusPerTask
            memPerCpu       = self.app.pargs.menPerCpu
            jobName         = self.app.pargs.jobname
            output          = self.app.pargs.output
            error           = self.app.pargs.error
            slurmScript     = self.app.pargs.slurm
            time            = self.app.pargs.time


            #import pdb; pdb.set_trace()
            if not partition:   #No partition variable is supplied(we cann't submmit this task with slurm)
                #run simply in the actual node
                if cpusPerTask>1 and ntasks>1: #no hybrid taks supported by john
                    raise Exception("No hybrid execution supported")
                elif cpusPerTask>1 and ntasks==1: #omp work
                    Bash.exec(f"export OMP_NUM_THREADS={cpusPerTask}")
                    with open(masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            attack_cmd = f"john --mask={mask} --format={hashType} {hashFile}"
                            print()
                            Bash.exec(attack_cmd)
                            print_status(f"Running {attack_cmd}")
                elif ntasks>1 and not cpusPerTask==1:  #mpi work
                    with open(masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            attack_cmd = f"mpirun -n {ntasks} john --mask={mask} --format={hashType} {hashFile}"
                            print()
                            Bash.exec(attack_cmd)
                            print_status(f"Running {attack_cmd}")
                else:   # serial work(canceled because parallel support is enable)
                    print_failure("You will run john parallelly(ntasks>1)")
                    sys.exit(1)
            else:   # we can summit this work with slurm
                if cpusPerTask>1 and ntasks>1: #no hybrid taks supported by john
                    raise Exception("No hybrid execution supported")
                elif cpusPerTask>1 and ntasks==1 and nodes==1: #omp work in only 1 node(OpenMP isn't scalable)
                    # writing slurm script (sscript)
                    sscript =   "#!/bin/bash" +\
                                f"#\nSBATCH --job-name={jobName}" +\
                                f"#\nSBATCH --nodes={nodes}"  +\
                                f"#\nSBATCH --ntasks={ntasks}"    +\
                                f"#\nSBATCH --cpus-per-task={cpusPerTask}"
                    
                    if time:
                        sscript += f"\n#SBATCH --time={time}\n" 
                    
                    sscript += "\n\n#Performing a parallel mask attack"
                    with open(masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            sscript += f"\nsrun john --mask={mask} --format={hashType} {hashFile}"

                    with open(slurmScript, 'w') as submmitScript:   # writing generated slurm submmit script
                        submmitScript.write(sscript)

                    infoAttack =    f"Performing a mask attack against of {hashType} hash in {hashFile}" +\
                                    f"\n\tmaskFile: {masksFile}"
                                
                    parallelAttackinfo =    f"Parallel attack desciption:" +\
                                            f"\n\tnodes: {nodes}" +\
                                            f"\n\tntasks: {ntasks}" +\
                                            f"\n\tpartition: {partition}\n"
                                            # ADD MORE DETAILS
                    print_status(infoAttack)
                    print_status(parallelAttackinfo)
                    #Bash.exec(f"sbatch {slurmScript}")

                elif cpusPerTask==1 and ntasks>1 and nodes>=1: #mpi work(parallel scalable task)
                    # writing slurm script (sscript)
                    sscript =   "#!/bin/bash" +\
                                f"\n#SBATCH --job-name={jobName}" +\
                                f"\n#SBATCH --nodes={nodes}"  +\
                                f"\n#SBATCH --ntasks={ntasks}"    +\
                                f"\n#SBATCH --cpus-per-task={cpusPerTask}"
                    
                    if memPerCpu:
                        sscript += f"\n#SBATCH --mem-per-cpu={memPerCpu}\n"

                    if time:
                        sscript += f"\n#SBATCH --time={time}\n" 
                    
                    if error:
                        sscript += f"\n#SBATCH --error={error}\n"
                    if output:
                        sscript += f"\n#SBATCH --output={output}\n"
                        
                    sscript += "\n\n#Performing several parallel mask attacks"
                    with open(masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            sscript += f"\nsrun mpirun john --mask={mask} --format={hashType} {hashFile}"

                    with open(slurmScript, 'w') as submmitScript:   # writing generated slurm submmit script
                        submmitScript.write(sscript)



                    infoAttack =    f"Performing a mask attack against of {hashType} hash in {hashFile}" +\
                                    f"\n\tmaskFile: {masksFile}"
                                
                    parallelAttackinfo =    f"Parallel attack desciption:" +\
                                            f"\n\tnodes: {nodes}" +\
                                            f"\n\tntasks: {ntasks}" +\
                                            f"\n\tpartition: {partition}\n"
                                            # ADD MORE DETAILS
                    print_status(infoAttack)
                    print_status(parallelAttackinfo)
                    Bash.exec(f"sbatch {slurmScript}")
                
                else:
                    raise Exception("Invalid arguments.")

        except Exception as error:
            print_failure(error)
            self.app.args.print_help()
            sys.exit(1)