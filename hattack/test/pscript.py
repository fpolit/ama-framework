#!/usr/bin/env python3
from mattack.mattack import MaskAttack
from sbash.core import Bash
#Description of submmited mask attack
#masksFile   = {self.masksFile}
#hashType    = {self.hashType}
#hashFile    = {self.hashFile}
#nodes       = {nodes}
#ntasks      = {ntasks}
#partition   = {partition}
#cpusPerTask = {cpusPerTask}
#memPerCpu   = {memPerCpu}
#jobName     = {jobName}
#output      = {output}
#error       = {error}
#slurmScript = {slurmScript}
#time        = {time}

#Execution of the parallel mask attack
if __name__=='__main__':
        with open(self.masksFile, 'r') as masks:
            while mask := masks.readline():
                mask = mask.rstrip()
                if not MaskAttack.status(self.hashFile):
                    Bash.exec(f"srun mpirun john --mask={mask} --format={self.hashType} {self.hashFile}")