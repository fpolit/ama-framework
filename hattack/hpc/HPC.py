#!/usr/bin/env python3

from fineprint.status import print_status

# hpc exceptions
from .HPCExceptions import HybridWorkError
from .HPCExceptions import SlurmParametersError
#from .HPCExceptions import ParallelWorkError

class HPC:
    """
    HPC hold the necesary parameter to submit a parallel task (with slurm)
    """

    def __init__(self, *, gpus=None, nodes=None, ntasks=None, partition=None, cpusPerTask=1, memPerCpu=None,
                 jobName="crack", output=None, error=None, time=None, slurmScript="hashattack.slurm"):
        # slurm parameters
        self.gpus = gpus
        self.nodes = nodes
        self.ntasks = ntasks
        self.partition = partition
        self.cpusPerTask = cpusPerTask
        self.memPerCpu = memPerCpu
        self.jobName = jobName
        self.output = output
        self.error = error
        self.time = time

        # extra parameters
        self.slurmScript = slurmScript




    def slurmParameters(self):
        """
        return only slurm parameters
        """
        slurm  = {'gpu': self.gpus,
                  'nodes': self.nodes,
                  'ntasks': self.ntasks,
                  'partition': self.partition,
                  'cpus-per-task': self.cpusPerTask,
                  'mem-per-cpu': self.memPerCpu,
                  'job-name': self.jobName,
                  'output': self.output,
                  'error': self.error,
                  'time': self.time}

        return slurm


    def parameters(self):
        """
        return slurm and extra parameters
        """
        slurm  = {'gpu': self.gpus,
                  'nodes': self.nodes,
                  'ntasks': self.ntasks,
                  'partition': self.partition,
                  'cpus-per-task': self.cpusPerTask,
                  'mem-per-cpu': self.memPerCpu,
                  'job-name': self.jobName,
                  'output': self.output,
                  'error': self.error,
                  'time': self.time}
        extra = {'slurm-script': self.slurmScript}
        return [slurm, extra]



    @staticmethod
    def parserJob(slurm):
        """
        slurm : is the slurm dictonary returned parameters or slurmParameters methods
        """
        if slurm["gpu"] == 0 and slurm["nodes"] == 1 and slurm["ntasks"] == 1 and slurm["cpus-per-task"] > 1:
            return "OMP"

        elif slurm["gpu"] == 0 and slurm["nodes"] >= 1 and slurm["ntasks"] >= 1 and slurm["cpus-per-task"] == 1:
            return "MPI"

        elif slurm["gpu"] > 0 and slurm["nodes"] == 1 and slurm["ntasks"] == 1 and slurm["cpus-per-task"] == 1:
            return "GPU"

        elif slurm["gpu"] > 0 and slurm["nodes"] >= 1 and slurm["ntasks"] >= 1 and slurm["cpus-per-task"] >= 1:
            raise HybridWorkError({'gpus': slurm["gpu"], 'nodes': slurm["nodes"], 'ntasks': slurm["ntasks"], 'cpuPerTask': slurm["cpu-per-task"]})
        else:
            raise SlurmParametersError(slurm)



    def parserParallelJob(self):
        """
        parser the slurm parameters and return the type of parallel job (OMP, MPI, GPU[CUDA-OPENCL])

        return
        parallel job type : OMP or MPI or GPU
        """

        if self.gpus == 0 and self.nodes == 1 and self.ntasks == 1 and self.cpusPerTask > 1:
            return "OMP"

        elif self.gpus == 0 and self.nodes >= 1 and self.ntasks >= 1 and self.cpusPerTask == 1:
            return "MPI"

        elif self.gpus > 0 and self.nodes == 1 and self.ntasks == 1 and self.cpusPerTask == 1:
            return "GPU"

        elif self.gpus > 0 and self.nodes >= 1 and self.ntasks >= 1 and self.cpusPerTask >= 1:
            raise HybridWorkError({'gpus': self.gpus, 'nodes': self.nodes, 'ntasks': self.ntasks, 'cpuPerTask': self.cpuPerTask})
        else:
            invalidParameters = self.parameters()
            raise SlurmParametersError(invalidParameters)


    def genScript(self, parallelWork):
        """
        generate a slurm script to submit with sbatch using the slurm parameters(constructor parameters) and the parallelWork variable(list of task to perform)

        parallelWork (list[str]): paralell tasks to perform [task1, task2, ...]
        """

        slurm, extra = self.parameters()
        slurmScriptName = extra['slurm-script']


        with open(slurmScriptName, 'w') as slurmScript:
            slurmScript.write("#!/bin/bash\n")
            for flag, argument in slurm.items():
                if flag != "gpu" and argument != None:
                    slurmScript.write(f"#SBATCH --{flag}={argument}\n")

                else:
                    if argument > 0:
                        slurmScript.write(f"#SBATCH --gres={flag}:{argument}\n")

            if HPC.parserJob(slurm) == "OMP":
                slurmScript.write("export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK\n")

            whiteLine = "\n"
            slurmScript.write(whiteLine)
            for task in parallelWork:
                slurmScript.write(f"{task}\n")


        print_status(f"Slurm script generated: {slurmScriptName}")


    @staticmethod
    def genScript(slurm, extra, parallelWork):
        """
        [slurm, extra] are the variable returned by parameters method
        generate a slurm script to submit with sbatch using the slurm parameters(slurm constructor parameters) and the parallelWork variable(list of task to perform)

        parallelWork (list[str]): paralell tasks to perform [task1, task2, ...]
        """
        #import pdb; pdb.set_trace()
        #slurm, extra = self.parameters()
        slurmScriptName = extra['slurm-script']


        with open(slurmScriptName, 'w') as slurmScript:
            slurmScript.write("#!/bin/bash\n")
            for flag, argument in slurm.items():
                if not flag == "gpu":
                    if argument:
                        slurmScript.write(f"#SBATCH --{flag}={argument}\n")

                else: # gpu flag
                    if argument > 0:
                        slurmScript.write(f"#SBATCH --gres={flag}:{argument}\n")

            if HPC.parserJob(slurm) == "OMP":
                slurmScript.write("export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK\n")


            whiteLine = "\n"
            slurmScript.write(whiteLine)
            for task in parallelWork:
                slurmScript.write(f"{task}\n")

        print_status(f"Slurm script generated: {slurmScriptName}")
