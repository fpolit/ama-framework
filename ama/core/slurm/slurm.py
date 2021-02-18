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

    def __init__(self, *, array=None, account=None, dependecy=None, chdir=None, error=None,
                 jobName="hattack", cluster=None, distribution="block", mailType=None, mailUser=None,
                 mem=None, memPerCpu=None, nodes=1, ntasks=1, nice=None, output=None, openMode="truncate",
                 partition=None, reservation=None, time=None, testOnly=False, verbose=False,
                 nodelist=None, wait=False, exclude=None, cpusPerTask=1,
                 slurmScript="hattack.slurm"):

        # slurm parameters - shortcut - arguments
        self.array = array # -a <e.x: 0-15 or 0,6,16-32>
        self.account = account # -A <account>
        self.dependency = dependency # -d
        self.chdir = chdir # -D <homework directory path>
        self.error = error # -e <error file path>
        self.jobName = jobName # -J <str>
        self.cluster = cluster # -M <cluster name>
        self.distribution = distribution # -m <block|cyclic|plane|arbitrary>
        self.mailType = mailType # NONE <BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>, PP: percent of the limit time
        self.mailUser = mailUser # NONE <user email>
        self.mem = mem # NONE <size[units]>, units = [K|M|G|T] (memory per node)
        self.memPerCpu = memPerCpu # NONE <size[units]>
        self.cpusPerTask = cpusPerTask # -c <ncpus>
        self.nodes = nodes # -N <minnodes[-maxnodes]>
        self.ntasks = ntasks # -n <number of tasks>
        self.nice = nice # NONE <adjustment>, adjustment is between +- 2147483645
        self.output = output # -o <path>
        self.openMode = openMode # NONE <append|truncate>
        self.partition = partition # -p <partition>
        self.reservation = reservation # NONE <reservation>
        self.time = time # -t <time>
        # time formats: MM, MM:SS, HH:MM:SS, DD-HH, DD-HH:MM, DD-HH:MM:SS
        # DD:days, HH:hours, MM: minutes, SS:secconds
        self.testOnly = testOnly # NONE <NO VALUE>,if testOnly=True enable this flag otherwise omit
        self.verbose = verbose # -v <NO VALUE>, if verbose=True enable this flag otherwise omit
        self.nodelist = nodelist # -w <nodelist>, e.x. nodelist = hw[00-04,06,08]
        self.wait = wait # -W <NO VALUE>, if wait=True enable this flag otherwise omit
        self.exclude = exclude # -x <nodelist>



        # self.nodes = nodes
        # self.ntasks = ntasks
        # self.partition = partition
        # self.cpusPerTask = cpusPerTask
        # self.memPerCpu = memPerCpu
        # self.jobName = jobName
        # self.output = output
        # self.error = error
        # self.time = time

        # self.gpus = gpus



        # extra parameters
        self.slurmScript = slurmScript




    def slurmParameters(self):
        """
        return only slurm parameters
        """

        slurm = {'array': self.array,
                 'account': self.account,
                 'dependency': self.dependecy,
                 'chdir': self.chdir,
                 'error': self.error,
                 'jobName': self.jobName,
                 'cluster': self.cluster,
                 'distribution': self.distribution,
                 'mail-type': self.mailType,
                 'mail-user': self.mailUser,
                 'mem': self.mem,
                 'mem-per-cpu': self.memPerCpu,
                 'nodes': self.nodes,
                 'ntasks': self.ntasks,
                 'nice': self.nice,
                 'output': self.output,
                 'open-mode': self.openMode,
                 'partition': self.partition,
                 'reservation': self.reservation,
                 'time': self.time,
                 'test-only': self.testOnly,
                 'verbose': self.verbose,
                 'nodelist': self.nodelist,
                 'wait': self.wait,
                 'exclude':self.exclude,
                 'cpus-per-task': self.cpusPerTask}

        return slurm


    def parameters(self):
        """
        return slurm and extra parameters
        """
        slurm  = self.slurmParameters()
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
            raise HybridWorkError({'gpus': slurm["gpu"], 'nodes': slurm["nodes"],
                                   'ntasks': slurm["ntasks"], 'cpuPerTask': slurm["cpu-per-task"]})
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
            raise HybridWorkError({'gpus': self.gpus, 'nodes': self.nodes,
                                   'ntasks': self.ntasks, 'cpuPerTask': self.cpuPerTask})
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
