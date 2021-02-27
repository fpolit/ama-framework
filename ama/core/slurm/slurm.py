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

    def __init__(self, *, array=None, account=None, dependency=None, chdir=None, error=None,
                 job_name="attack", cluster=None, distribution="block", mail_type=None, mail_user=None,
                 mem=None, mem_per_cpu=None, nodes=1, ntasks=1, nice=None, output=None, open_mode="truncate",
                 partition=None, reservation=None, time=None, test_only=False, verbose=False,
                 nodelist=None, wait=False, exclude=None, cpus_per_task=1,
                 slurm_script="attack.sh"):

        # slurm parameters (core) - shortcut - arguments
        self.array = Argument(array, False, "Index of array job (e.g. 0-15 or 0,6,16-32)") # -a <e.x: 0-15 or 0,6,16-32>
        self.account = Argument(account, False, "Cluster account to submit the job") # -A <account>
        self.dependency = Argument(dependency, False, "Defer the start of this job until the specified dependencies have been satisfied completed") # -d
        self.chdir = Argument(chdir, False, "Working directory path") # -D <working directory path>
        self.error = Argument(error, False, "Error file") # -e <error file path>
        self.job_name = Argument(job_name, False, "Name for the job allocation") # -J <str>
        self.cluster = Argument(cluster, False, "") # -M <cluster name>
        self.distribution = Argument(distribution, True, "Distribution methods for remote processes (<block|cyclic|plane|arbitrary>)") # -m <block|cyclic|plane|arbitrary>
        self.mai_type = Argument(mail_type, False, "Event types to notify user by email(<BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>)") # NONE <BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>, PP: percent of the limit time
        self.mail_user = Argument(mail_user, False, "User email") # NONE <user email>
        self.mem = Argument(mem, False, "Memory per node (<size[units]>)") # NONE <size[units]>, units = [K|M|G|T] (memory per node)
        self.mem_per_cpu = Argument(mem_per_cpu, False, "Minimum memory required per allocated CPU (<size[units]>)") # NONE <size[units]>
        self.cpus_per_task = Argument(cpus_per_task, True, "Number of processors per task") # -c <ncpus>
        self.nodes = Argument(nodes, True, "(<minnodes[-maxnodes]>)") # -N <minnodes[-maxnodes]>
        self.ntasks = Argument(ntasks, True, "Number of tasks") # -n <number of tasks>
        self.nice = Argument(nice, False, "Run the job with an adjusted scheduling") # NONE <adjustment>, adjustment is between +- 2147483645
        self.output = Argument(output, True, "Output file name (default: slurm-%j.out)") # -o <path>
        self.open_mode = Argument(open_mode, True, "Output open mode (<append|truncate>)") # NONE <append|truncate>
        self.partition = Argument(partition, True, "Partition to submit job") # -p <partition>
        self.reservation = Argument(reservation, False, "Resource reservation name") # NONE <reservation>
        self.time = Argument(time, False, "Limit of time (format: DD-HH:MM:SS)") # -t <time>
        # time formats: MM, MM:SS, HH:MM:SS, DD-HH, DD-HH:MM, DD-HH:MM:SS
        # DD:days, HH:hours, MM: minutes, SS:secconds
        self.test_only = Argument(test_only, True, "Validate the batch script and return an estimate of when a job would be scheduled to run. No job is actually submitted") # NONE <NO VALUE>,if testOnly=True enable this flag otherwise omit
        self.verbose = Argument(verbose, True, "Increase the verbosity of sbatch's informational messages") # -v <NO VALUE>, if verbose=True enable this flag otherwise omit
        self.nodelist = Argument(nodelist, False, "Nodelist") # -w <nodelist>, e.x. nodelist = hw[00-04,06,08]
        self.wait = Argument(wait, True, "Do not exit until the submitted job terminates") # -W <NO VALUE>, if wait=True enable this flag otherwise omit
        self.exclude = Argument(exclude, False, "Do not exit until the submitted job terminates") # -x <nodelist>


        # extra parameters
        self.slurm_script = Argument(slurm_script, True, "Name for the generated batch script")




    def coreParameters(self):
        """
        return only core parameters (slurm)
        """

        core = {
            'array': self.array.value,
            'account': self.account.value,
            'dependency': self.dependency.value,
            'chdir': self.chdir.value,
            'error': self.error.value,
            'job_name': self.jobName.value,
            'cluster': self.cluster.value,
            'distribution': self.distribution.value,
            'mail_type': self.mailType.value,
            'mail_user': self.mailUser.value,
            'mem': self.mem.value,
            'mem_per_cpu': self.memPerCpu.value,
            'cpus_per_task': self.cpusPerTask.value,
            'nodes': self.nodes.value,
            'ntasks': self.ntasks.value,
            'nice': self.nice.value,
            'output': self.output.value,
            'open_mode': self.openMode.value,
            'partition': self.partition.value,
            'reservation': self.reservation.value,
            'time': self.time.value,
            'test_only': self.testOnly.value,
            'verbose': self.verbose.value,
            'nodelist': self.nodelist.value,
            'wait': self.wait.value,
            'exclude':self.exclude.value
        }

        return core


    def parameters(self):
        """
        return core and extra parameters
        """
        core  = self.coreParameters()
        extra = {'slurm_script': self.slurmScript.value}
        return [core, extra]


    def options(self):
        core = {'array': self.array,
                'account': self.account,
                'dependency': self.dependency,
                'chdir': self.chdir,
                'error': self.error,
                'job_name': self.job_name,
                'cluster': self.cluster,
                'distribution': self.distribution,
                'mail_type': self.mail_type,
                'mail_user': self.mail-user,
                'mem': self.mem,
                'mem_per_cpu': self.mem_per_cpu,
                'cpus_per_task': self.cpus_per_task,
                'nodes': self.nodes,
                'ntasks': self.ntasks,
                'nice': self.nice,
                'output': self.output,
                'open_mode': self.open_mode,
                'partition': self.partition,
                'reservation': self.reservation,
                'time': self.time,
                'test_only': self.test_only,
                'verbose': self.verbose,
                'nodelist': self.nodelist,
                'wait': self.wait,
                'exclude':self.exclude}

        extra = {'slurm_script': self.slurm_script}
        return {**core, **extra}

    @staticmethod
    def parserJob(core):
        """
        core : is the core dictonary returned by  coreParameters methods
        """
        if core["gpu"] == 0 and core["nodes"] == 1 and core["ntasks"] == 1 and core["cpus_per_task"] > 1:
            return "OMP"

        elif core["gpu"] == 0 and core["nodes"] >= 1 and core["ntasks"] >= 1 and core["cpus_per_task"] == 1:
            return "MPI"

        elif core["gpu"] > 0 and core["nodes"] == 1 and core["ntasks"] == 1 and core["cpus_per_task"] == 1:
            return "GPU"

        elif core["gpu"] > 0 and core["nodes"] >= 1 and core["ntasks"] >= 1 and core["cpus_per_task"] >= 1:
            raise HybridWorkError({'gpus': core['gpu'], 'nodes': core['nodes'],
                                   'ntasks': core["ntasks"], 'cpu_per_task': core['cpu_per_task']})
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
                                   'ntasks': self.ntasks, 'cpu_per_task': self.cpu_per_task})
        else:
            invalidParameters = self.parameters()
            raise SlurmParametersError(invalidParameters)


    def genSbatchScript(self, parallelWork: List[str] = None):
        """
        generate a slurm script to submit with sbatch using the slurm parameters(constructor parameters) and the parallelWork variable(list of task to perform)

        parallelWork (list[str]): paralell tasks to perform [task1, task2, ...]
        """

        core, extra = self.parameters()
        slurmScriptName = extra['slurm_script']


        with open(slurmScriptName, 'w') as slurmScript:
            slurmScript.write("#!/bin/bash\n")
            for flag, argument in core.items():
                if flag != "gpu" and (argument is not None):
                    flag = flag.replace("_", "-")
                    slurmScript.write(f"#SBATCH --{flag}={argument}\n")

                else:
                    if argument > 0:
                        flag = flag.replace("_", "-")
                        slurmScript.write(f"#SBATCH --gres={flag}:{argument}\n")

            if Slurm.parserJob(core) == "OMP":
                slurmScript.write("export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK\n")

            whiteLine = "\n"
            slurmScript.write(whiteLine)
            for task in parallelWork:
                slurmScript.write(f"{task}\n")


        print_status(f"Batch script generated: {slurmScriptName}")


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
                if not flag == "gpu" and (argument is not None):
                    flag = flag.replace("_", "-")
                    slurmScript.write(f"#SBATCH --{flag}={argument}\n")

                else: # gpu flag
                    if argument > 0:
                        flag = flag.replace("_", "-")
                        slurmScript.write(f"#SBATCH --gres={flag}:{argument}\n")

            if Slurm.parserJob(core) == "OMP":
                slurmScript.write("export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK\n")


            whiteLine = "\n"
            slurmScript.write(whiteLine)
            for task in parallelWork:
                slurmScript.write(f"{task}\n")

        print_status(f"Slurm script generated: {slurmScriptName}")
