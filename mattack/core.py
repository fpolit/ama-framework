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
    crackers = ["jtr", "hc"]

    def __init__(self, masksFile, hashType, hashFile):
        self.masksFile = masksFile
        self.hashType = hashType
        self.hashFile = hashFile

    @staticmethod
    def search(search=None, *, sensitive=False, jtrFormats=False, hcFormats=False):
        if search:
            if not sensitive:
                hashPattern = re.compile(rf"\w*{search}\w*", re.IGNORECASE)
            else:
                hashPattern = re.compile(rf"\w*{search}\w*")

            if jtrFormats: # search by a jtr hash format
                print_status(f"John the Ripper posible hash formats(*{search}*):")
                #print_status("id")
                for hashFormat in MaskAttack.jtr_hashes:
                    if hashPattern.search(hashFormat):
                        print_successful(hashFormat)
            if hcFormats: # search by an hashcat hash format
                print_status(f"Hashcat posible hash formats(*{search}*):")
                print_status("id\tname")
                for hash_id, hashFormat in MaskAttack.hc_hashes.items():
                    if hashPattern.search(hashFormat['Name']):
                        print_successful(f"{hash_id}\t{hashFormat['Name']}")
        else:
            print_failure("No pattern given.")

    @staticmethod
    def statusHash(hash, cracker):
        """
            Check status of the hash (it is cracked or no)
            It hash is cracked when it is in the ~/.john/john.pot file
            otherwise it isn't cracked
        """
        #import pdb; pdb.set_trace()
        homeUser = os.path.expanduser("~")
        if cracker == "jtr":
            crackedPattern = re.compile(rf"\$(\W*|\w*)\$({hash})(\$(\W*|\w*)\$)?:(\W*|\w*|\@*)")
            potfilePath = os.path.join(homeUser, ".john/john.pot")
        elif cracker == "hc":
            crackedPattern = re.compile(rf"({hash}):(\W*|\w*)")
            potfilePath = os.path.join(homeUser, ".hashcat/hashcat.potfile")

        with open(potfilePath, 'r') as potfile:
            while   crackedHash := potfile.readline().rstrip():
                if(crackedPattern.fullmatch(crackedHash)):
                    return True
        return False
    
    @staticmethod
    def statusHashFile(hashFile, cracker=None):
        # potfile: is a file where a paswrod cracker save the cracked hashes
        # check if all the hashes in a hashFile are broken
        #import pdb; pdb.set_trace()
        if cracker in MaskAttack.crackers:
            with open(hashFile, 'r') as hashes:
                while hash := hashes.readline():
                    hash = hash.rsplit()[0]
                    hash = hash.split(":")
                    if(len(hash) > 1):
                        hash = hash[1]
                    else:
                        hash = hash[0]
                    if not MaskAttack.statusHash(hash, cracker):
                        return False
            return True
        return False


    def debug(self, gpus=None, nodes=None, ntasks=None, partition=None, cpusPerTask=1, memPerCpu=None,
        jobName="maskattack", output=None, error=None, slurmScript="maskattack.slurm", time=None):
        print(f"""
        masksFile   = {self.masksFile}
        hashType    = {self.hashType}
        hashFile    = {self.hashFile}
        gpus        = {gpus}
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

    def run(self, gpus=None, nodes=None, ntasks=None, partition=None, cpusPerTask=1, memPerCpu=None,
        jobName="maskattack", output=None, error=None, slurmScript="maskattack.slurm", time=None):
        """
            Submit a slurm task
        """
        try:

            self.debug(gpus, nodes, ntasks, partition, cpusPerTask, memPerCpu,
                        jobName, output, error, slurmScript, time)

            #import pdb; pdb.set_trace()
            if not partition:   #No partition variable is supplied(we cann't submmit this task with slurm)
                #run simply in the actual node
                if cpusPerTask>1 and ntasks>1: #no hybrid taks supported by john
                    raise Exception("No hybrid attack supported")
                
                elif gpus > 0 and (ntasks==1 and cpusPerTask==1):
                    parallelAttackinfo =    f"Parallel mask attack description" +\
                                            f"\n\tType of parallelism: CUDA/OpenCL" +\
                                            f"\n\tgpus: {gpus}" +\
                                            f"\n\tnodes: {nodes}"
                                            # ADD MORE DETAILS

                    print_status(parallelAttackinfo)
                    with open(self.masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            attack_cmd = f"hashcat -a 3 -m {self.hashType} {self.hashFile} {mask}"
                            print()
                            print_status(f"Running: {attack_cmd}")
                            Bash.exec(attack_cmd)
                            if MaskAttack.statusHashFile(self.hashFile, cracker='hc'):
                                print_successful(f"Hash File {self.hashFile} cracked sucefully.")
                                break

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
                            print_status(f"Running: {attack_cmd}")
                            Bash.exec(attack_cmd)
                            if MaskAttack.statusHashFile(self.hashFile, cracker='jtr'):
                                print_successful(f"Hash File {self.hashFile} cracked sucefully.")
                                break
                            
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
                            print_status(f"Running: {attack_cmd}")
                            Bash.exec(attack_cmd)
                            if MaskAttack.statusHashFile(self.hashFile, cracker='jtr'):
                                print_successful(f"Hash File {self.hashFile} cracked sucefully.")
                                break
                            
                else:   # serial work(canceled because parallel support is enable)
                    print_status("So boring, you will attack parallelly(ntasks>1 [MPI] or cpusPerTask>1 [OMP])")
                    sys.exit(1)
            else:   # we can summit this work with slurm
                if cpusPerTask>1 and ntasks>1: #no hybrid taks supported by john
                    raise Exception("No hybrid attack supported")
                elif cpusPerTask>=1 and ntasks>=1 and nodes>=1: #parallel work (OMP or MPI)
      
                    # generating python attack (pscript)

                    pscript =   "#!/usr/bin/env python3" +\
                                "\n\nfrom mattack.core import MaskAttack" +\
                                "\nfrom sbash.core import Bash" +\
                                "\nfrom fineprint.status import print_failure, print_status, print_successful" +\
                                f"\n\n#Description of submmited mask attack"  +\
                                f"\n#masksFile   = {self.masksFile}" +\
                                f"\n#hashType    = {self.hashType}" +\
                                f"\n#hashFile    = {self.hashFile}" +\
                                f"\n#nodes       = {nodes}" +\
                                f"\n#ntasks      = {ntasks}" +\
                                f"\n#partition   = {partition}" +\
                                f"\n#cpusPerTask = {cpusPerTask}" +\
                                f"\n#memPerCpu   = {memPerCpu}" +\
                                f"\n#jobName     = {jobName}" +\
                                f"\n#output      = {output}" +\
                                f"\n#error       = {error}" +\
                                f"\n#slurmScript = {slurmScript}" +\
                                f"\n#time        = {time}"

                    pscript +=  f"\n\n#Execution of the parallel mask attack" +\
                                f"\nif __name__=='__main__':" +\
                                f"\n\twith open('{self.masksFile}', 'r') as masks:" +\
                                f"\n\t\twhile mask := masks.readline():" +\
                                f"\n\t\t\tmask = mask.rstrip()" +\
                                f"\n\t\t\tif not MaskAttack.status('{self.hashFile}'):"
                    
                    mask = "{mask}"
                    if cpusPerTask>1 and ntasks==1 and nodes==1: #omp work in only 1 node(OpenMP isn't scalable)
                        pscript += f"\n\t\t\t\tprint_status(f'Mask Attack: srun john --mask={mask} --format={self.hashType} {self.hashFile}')"
                        pscript += f"\n\t\t\t\tBash.exec(f'srun john --mask={mask} --format={self.hashType} {self.hashFile}')"

                    if cpusPerTask==1 and ntasks>1 and nodes>=1: #mpi work(parallel scalable task)
                        pscript += f"\n\t\t\t\tprint_status(f'Mask Attack: srun mpirun john --mask={mask} --format={self.hashType} {self.hashFile}')"
                        pscript += f"\n\t\t\t\tBash.exec(f'srun mpirun john --mask={mask} --format={self.hashType} {self.hashFile}')"

                    pscript += f"\n\tprint_failure('Failed parallel mask attack against {self.hashFile} hash file')"
                    pscript += f"\n\tprint_failure('Refine you mask with PPACK to successfully crack {self.hashFile} hashes')"
                    pscript += "\n"


                    # writing generated python attack
                    pscriptName = jobName + ".py"
                    with open(pscriptName, 'w') as attackScript:   
                        attackScript.write(pscript)

                    # generating submit slurm script (sscript)
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
                    
                    if cpusPerTask>1 and ntasks==1 and nodes==1: #omp work in only 1 node(OpenMP isn't scalable)
                        sscript += "\nexport OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK"
   
                    sscript += "\n\n#parallel mask attacks to perform"
                    sscript += f"\npython3 {jobName}.py"
                    sscript += "\n"
                    
                    # writing slurm submmit script
                    with open(slurmScript, 'w') as submmitScript:
                        submmitScript.write(sscript)

                    ## mask attack info
                    infoAttack =    f"Submiting a mask attack against {self.hashType} hashes in {self.hashFile}"
                    print_status(infoAttack)
                    
                    # parallel attack info (generated script [slurm and python])
                    parallelAttackinfo =    f"Slurm submit generated: {slurmScript}"
                    print_status(parallelAttackinfo)

                    parallelAttackinfo = f"Python attack generated: {jobName}.py"
                    print_status(parallelAttackinfo)
                    
                    Bash.exec(f"sbatch {slurmScript}")

                elif cpusPerTask==1 and ntasks==1 and nodes==1:
                    print_status("You have a cluster  do not waste its power!")
                    sys.exit(1)

                else:
                    raise Exception("Invalid arguments.")

        except Exception as error:
            print_failure(error)
            sys.exit(1)
