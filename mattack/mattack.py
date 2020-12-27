#!/usr/bin/env python3

import re
import os
import sys
from fineprint.status import print_failure, print_status, print_successful
from sbash.core import Bash

# importing hashes of john the ripper and hashcat
from .jtrhash import jtrhashes
from .hchash import hchashes



class MaskAttack:
    """
        This class perform a mask attack
    """
    jtr_hashes = jtrhashes
    hc_hashes = hchashes

    def __init__(self, masksFile, hashType, hashFile):
        self.masksFile = masksFile
        self.hashType = hashType
        self.hashFile = hashFile

    @staticmethod
    def searchHash(search=None, *, sensitive=False):
        if search:
            if not sensitive:
                hashPattern = re.compile(rf"\w*{search}\w*", re.IGNORECASE)
            else:
                hashPattern = re.compile(rf"\w*{search}\w*")

            print_status(f"Posible hashes(*{search}*):")
            for hashFormat in MaskAttack.jtr_hashes:
                if hashPattern.search(hashFormat):
                    print_successful(hashFormat)

        else:
            print_failure("No pattern given.")

    @staticmethod
    def checkStatus(hash):
        """
            Check status of the hash (it is cracked or no)
            It hash is cracked when it is in the ~/.john/john.pot file
            otherwise it isn't cracked
        """
        import pdb; pdb.set_trace()
        crackedPattern = re.compile(rf"(\w|\W|\s)*{hash}(\w|\W|\s)*")
        homeUser = os.path.expanduser("~")
        johnPotPath = os.path.join(homeUser, ".john/john.pot")
        with open(johnPotPath, 'r') as johnPotFile:
            while   crackedHash := johnPotFile.readline().rstrip():
                if(crackedPattern.fullmatch(crackedHash)):
                    return True
        return False


    def debug(self, nodes=None, ntasks=None, partition=None, cpusPerTask=1, memPerCpu=None,
        jobName="mattack", output=None, error=None, slurmScript="mattack.slurm", time=None):
        print(f"""
        masksFile   = {self.masksFile}
        hashType    = {self.hashType}
        hashFile    = {self.hashFile}
        nodes       = {nodes}
        ntasks      = {ntasks}
        partition   = {partition}
        cpusPerTask = {cpusPerTask}
        memPerCpu   = {memPerCpu}
        jobName     = {jobName}
        output      = {output}
        error       = {error}
        slurmScript = {slurmScript}
        time        = {time}
        """)

    def run(self, nodes=None, ntasks=None, partition=None, cpusPerTask=1, memPerCpu=None,
        jobName="mattack", output=None, error=None, slurmScript="mattack.slurm", time=None):
        """
            Submit a slurm task
        """
        try:

            self.debug(nodes, ntasks, partition, cpusPerTask, memPerCpu,
                        jobName, output, error, slurmScript, time)

            #import pdb; pdb.set_trace()
            if not partition:   #No partition variable is supplied(we cann't submmit this task with slurm)
                #run simply in the actual node
                if cpusPerTask>1 and ntasks>1: #no hybrid taks supported by john
                    raise Exception("No hybrid attack supported")
                elif cpusPerTask>1 and ntasks==1: #omp work
                    #Bash.exec(f"export OMP_NUM_THREADS={cpusPerTask}")
                    parallelAttackinfo =    f"Parallel mask attack description" +\
                                            f"\n\tType of parallelism: OpenMP" +\
                                            f"\n\tnodes: {nodes}" +\
                                            f"\n\tthreads: {cpusPerTask}"
                                            # ADD MORE DETAILS

                    print_status(parallelAttackinfo)
                    with open(self.masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            attack_cmd = f"john --mask={mask} --format={self.hashType} {self.hashFile}"
                            print()
                            #Bash.exec(attack_cmd)
                            print_status(f"Running {attack_cmd}")
                elif ntasks>1 and cpusPerTask==1:  #mpi work
                    parallelAttackinfo =    f"Parallel mask attack description" +\
                                            f"\n\tType of parallelism: MPI" +\
                                            f"\n\tnodes: {nodes}" +\
                                            f"\n\tcores: {ntasks}"
                        # ADD MORE DETAILS

                    print_status(parallelAttackinfo)
                    with open(self.masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            attack_cmd = f"mpirun -n {ntasks} john --mask={mask} --format={self.hashType} {self.hashFile}"
                            print()
                            #Bash.exec(attack_cmd)
                            print_status(f"Running {attack_cmd}")
                else:   # serial work(canceled because parallel support is enable)
                    print_status("So boring, you will attack parallelly(ntasks>1 [MPI] or cpusPerTask>1 [OMP])")
                    sys.exit(1)
            else:   # we can summit this work with slurm
                if cpusPerTask>1 and ntasks>1: #no hybrid taks supported by john
                    raise Exception("No hybrid attack supported")
                elif cpusPerTask>1 and ntasks==1 and nodes==1: #omp work in only 1 node(OpenMP isn't scalable)
                    # writing slurm script (sscript)
                    sscript =   "#!/bin/bash" +\
                                f"\n#SBATCH --job-name={jobName}" +\
                                f"\n#SBATCH --nodes={nodes}"  +\
                                f"\n#SBATCH --ntasks={ntasks}"    +\
                                f"\n#SBATCH --cpus-per-task={cpusPerTask}" +\
                                f"\n#SBATCH --partition={partition}"

                    if memPerCpu:
                        sscript += f"\n#SBATCH --mem-per-cpu={memPerCpu}"

                    if time:
                        sscript += f"\n#SBATCH --time={time}"

                    if error:
                        sscript += f"\n#SBATCH --error={error}"

                    if output:
                        sscript += f"\n#SBATCH --output={output}"

                    sscript += "\n\n#parallel mask attacks to perform"
                    with open(self.masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            sscript += f"\nsrun john --mask={mask} --format={self.hashType} {self.hashFile}"

                    sscript += "\n"
                    with open(slurmScript, 'w') as submmitScript:   # writing generated slurm submmit script
                        submmitScript.write(sscript)

                    infoAttack =    f"Submiting a mask attack against {self.hashType} hashes in {self.hashFile}"

                    parallelAttackinfo =    f"Slurm submit script generated: {slurmScript}"

                    print_status(infoAttack)
                    print_status(parallelAttackinfo)
                    #Bash.exec(f"sbatch {slurmScript}")

                elif cpusPerTask==1 and ntasks>1 and nodes>=1: #mpi work(parallel scalable task)
                    # writing slurm script (sscript)
                    sscript =   "#!/bin/bash" +\
                                f"\n#SBATCH --job-name={jobName}" +\
                                f"\n#SBATCH --nodes={nodes}"  +\
                                f"\n#SBATCH --ntasks={ntasks}"    +\
                                f"\n#SBATCH --cpus-per-task={cpusPerTask}" +\
                                f"\n#SBATCH --partition={partition}"

                    if memPerCpu:
                        sscript += f"\n#SBATCH --mem-per-cpu={memPerCpu}"

                    if time:
                        sscript += f"\n#SBATCH --time={time}"

                    if error:
                        sscript += f"\n#SBATCH --error={error}"
                    if output:
                        sscript += f"\n#SBATCH --output={output}"

                    sscript += "\n\n#parallel mask attacks to perform"
                    with open(self.masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            sscript += f"\nsrun mpirun john --mask={mask} --format={self.hashType} {self.hashFile}"

                    sscript += "\n"
                    with open(slurmScript, 'w') as submmitScript:   # writing generated slurm submmit script
                        submmitScript.write(sscript)



                    infoAttack =    f"Submiting a mask attack against {self.hashType} hashes in {self.hashFile}"

                    parallelAttackinfo =    f"Slurm submit script generated: {slurmScript}"

                    print_status(infoAttack)
                    print_status(parallelAttackinfo)
                    #Bash.exec(f"sbatch {slurmScript}")

                elif cpusPerTask==1 and ntasks==1 and nodes==1:
                    print_status("You have a cluster  do not waste their power!")
                    # self.debug(nodes, ntasks, partition, cpusPerTask, memPerCpu,
                    #             jobName, output, error, slurmScript, time)
                    sys.exit(1)

                else:
                    # self.debug(nodes, ntasks, partition, cpusPerTask, memPerCpu,
                    #             jobName, output, error, slurmScript, time)
                    raise Exception("Invalid arguments.")

        except Exception as error:
            print_failure(error)
            sys.exit(1)
