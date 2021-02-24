#!/usr/bin/env python3
#
# Slurm class to manage sbatch parameters to submit parallel jobs
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from typing import List

# base imports
from ama.core.modules.base import Argument

class Slurm:
    """
    Manage sbatch parameters to submit parallel jobs
    """

    def __init__(self, *, array=None, account=None, dependecy=None, chdir=None, error=None,
                 jobName="hattack", cluster=None, distribution="block", mailType=None, mailUser=None,
                 mem=None, memPerCpu=None, nodes=1, ntasks=1, nice=None, output=None, openMode="truncate",
                 partition=None, reservation=None, time=None, testOnly=False, verbose=False,
                 nodelist=None, wait=False, exclude=None, cpusPerTask=1,
                 slurmScript="hattack.slurm"):

        # slurm parameters (core) - shortcut - arguments
        self.array = Argument(array, False, "Index of array job (e.g. 0-15 or 0,6,16-32)") # -a <e.x: 0-15 or 0,6,16-32>
        self.account = Argument(account, False, "Cluster account to submit the job") # -A <account>
        self.dependency = Argument(dependency, False, "Defer the start of this job until the specified dependencies have been satisfied completed") # -d
        self.chdir = Argument(chdir, False, "Defer the start of this job until the specified dependencies have been satisfied completed") # -D <homework directory path>
        self.error = Argument(error, False, "Error file") # -e <error file path>
        self.jobName = Argument(jobName, False, "Name for the job allocation") # -J <str>
        self.cluster = Argument(cluster, False, "") # -M <cluster name>
        self.distribution = Argument(distribution, True, "Distribution methods for remote processes (<block|cyclic|plane|arbitrary>)") # -m <block|cyclic|plane|arbitrary>
        self.mailType = Argument(mailType, False, "Event types to notify user by email(<BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>)") # NONE <BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>, PP: percent of the limit time
        self.mailUser = Argument(mailUser, False, "User email") # NONE <user email>
        self.mem = Argument(mem, False, "Memory per node (<size[units]>)") # NONE <size[units]>, units = [K|M|G|T] (memory per node)
        self.memPerCpu = Argument(memPerCpu, False, "Minimum memory required per allocated CPU (<size[units]>)") # NONE <size[units]>
        self.cpusPerTask = cpusPerTask # -c <ncpus>
        self.nodes = Argument(nodes, True, "(<minnodes[-maxnodes]>)") # -N <minnodes[-maxnodes]>
        self.ntasks = ntasks # -n <number of tasks>
        self.nice = Argument(nice, False, "Run the job with an adjusted scheduling") # NONE <adjustment>, adjustment is between +- 2147483645
        self.output = Argument(output, True, "Output file name (default: slurm-%j.out)") # -o <path>
        self.openMode = Argument(openMode, True, "Output open mode (<append|truncate>)") # NONE <append|truncate>
        self.partition = Argument(partition, True, "Partition to submit job") # -p <partition>
        self.reservation = reservation # NONE <reservation>
        self.time = Argument(time, False, "Limit of time (format: DD-HH:MM:SS)") # -t <time>
        # time formats: MM, MM:SS, HH:MM:SS, DD-HH, DD-HH:MM, DD-HH:MM:SS
        # DD:days, HH:hours, MM: minutes, SS:secconds
        self.testOnly = Argument(testOnly, True, "Validate the batch script and return an estimate of when a job would be scheduled to run. No job is actually submitted") # NONE <NO VALUE>,if testOnly=True enable this flag otherwise omit
        self.verbose = Argument(verbose, False, "Increase the verbosity of sbatch's informational messages") # -v <NO VALUE>, if verbose=True enable this flag otherwise omit
        self.nodelist = nodelist # -w <nodelist>, e.x. nodelist = hw[00-04,06,08]
        self.wait = Argument(wait, False, "Do not exit until the submitted job terminates") # -W <NO VALUE>, if wait=True enable this flag otherwise omit
        self.exclude = Argument(exclude, False, "Do not exit until the submitted job terminates") # -x <nodelist>


        # extra parameters
        self.slurmScript = Argument(slurmScript, True, "Name of generated batch script")




    def coreParameters(self):
        """
        return only core parameters (slurm)
        """

        core = {'array': self.array,
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
                 'cpus-per-task': self.cpusPerTask,
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
                 'exclude':self.exclude}

        return core


    def parameters(self):
        """
        return core and extra parameters
        """
        core  = self.coreParameters()
        extra = {'slurm-script': self.slurmScript.value}
        return [core, extra]



    @staticmethod
    def parserJob(core):
        """
        core : is the core dictonary returned by  coreParameters methods
        """
        if core["gpu"] == 0 and core["nodes"] == 1 and core["ntasks"] == 1 and core["cpus-per-task"] > 1:
            return "OMP"

        elif core["gpu"] == 0 and core["nodes"] >= 1 and core["ntasks"] >= 1 and core["cpus-per-task"] == 1:
            return "MPI"

        elif core["gpu"] > 0 and core["nodes"] == 1 and core["ntasks"] == 1 and core["cpus-per-task"] == 1:
            return "GPU"

        elif core["gpu"] > 0 and core["nodes"] >= 1 and core["ntasks"] >= 1 and core["cpus-per-task"] >= 1:
            raise HybridWorkError({'gpus': core["gpu"], 'nodes': core["nodes"],
                                   'ntasks': core["ntasks"], 'cpuPerTask': core["cpu-per-task"]})
        else:
            raise SlurmParametersError(core)



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


    def genSbatchScript(self, parallelWork: List[str] = None):
        """
        generate a slurm script to submit with sbatch using the slurm parameters(constructor parameters) and the parallelWork variable(list of task to perform)

        parallelWork (list[str]): paralell tasks to perform [task1, task2, ...]
        """

        core, extra = self.parameters()
        slurmScriptName = extra['slurm-script']


        with open(slurmScriptName, 'w') as slurmScript:
            slurmScript.write("#!/bin/bash\n")
            for flag, argument in core.items():
                if flag != "gpu" and argument != None:
                    slurmScript.write(f"#SBATCH --{flag}={argument}\n")

                else:
                    if argument > 0:
                        slurmScript.write(f"#SBATCH --gres={flag}:{argument}\n")

            if Slurm.parserJob(core) == "OMP":
                slurmScript.write("export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK\n")

            whiteLine = "\n"
            slurmScript.write(whiteLine)
            for task in parallelWork:
                slurmScript.write(f"{task}\n")


        print_status(f"Slurm script generated: {slurmScriptName}")


    @staticmethod
    def genSbatchScript(core, extra, parallelWork):
        """
        [core, extra] are the variable returned by coreParameters method
        generate a slurm script to submit with sbatch using the slurm parameters(slurm constructor parameters) and the parallelWork variable(list of task to perform)

        parallelWork (list[str]): paralell tasks to perform [task1, task2, ...]
        """
        #import pdb; pdb.set_trace()
        #slurm, extra = self.parameters()
        slurmScriptName = extra['slurm-script']


        with open(slurmScriptName, 'w') as slurmScript:
            slurmScript.write("#!/bin/bash\n")
            for flag, argument in core.items():
                if not flag == "gpu":
                    if argument:
                        slurmScript.write(f"#SBATCH --{flag}={argument}\n")

                else: # gpu flag
                    if argument > 0:
                        slurmScript.write(f"#SBATCH --gres={flag}:{argument}\n")

            if Slurm.parserJob(core) == "OMP":
                slurmScript.write("export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK\n")


            whiteLine = "\n"
            slurmScript.write(whiteLine)
            for task in parallelWork:
                slurmScript.write(f"{task}\n")

        print_status(f"Slurm script generated: {slurmScriptName}")
