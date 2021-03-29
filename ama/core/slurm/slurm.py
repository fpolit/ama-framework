#!/usr/bin/env python3
#
# Slurm class to manage sbatch parameters to submit parallel jobs
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from typing import List

#finprint imports
from fineprint.status import (
    print_successful,
    print_status
)

# base imports
from ama.core.modules.base import Argument

class Slurm:
    """
    Manage sbatch parameters to submit parallel jobs
    """

    SBATCH_OPTIONS = [
        "array",
        "account",
        "dependency",
        "chdir",
        "error",
        "job_name",
        "cluster",
        "distribution",
        "mail_type",
        "main_user",
        "mem",
        "mem_per_cpu",
        "cpus_per_task",
        "nodes",
        "ntasks",
        "nice",
        "output",
        "open_mode",
        "partition",
        "reservation",
        "time",
        "test_only",
        "verbose",
        "nodelist",
        "wait",
        "exclude",
        "gpu"
    ]

    EXTRA_OPTIONS = [
        "batch_script",
        "pmix"
    ]

    OPTIONS = [*SBATCH_OPTIONS, *EXTRA_OPTIONS]
    # def __init__(self, *, array=None, account=None, dependency=None, chdir=None, error=None,
    #              job_name="attack", cluster=None, distribution="block", mail_type=None, mail_user=None,
    #              mem=None, mem_per_cpu=None, nodes=1, ntasks=1, nice=None, output=None, open_mode="truncate",
    #              partition=None, reservation=None, time=None, test_only=False, verbose=False,
    #              nodelist=None, wait=False, exclude=None, cpus_per_task=1, gpus=0,
    #              batch_script="attack.sh"):

    def __init__(self, **kwargs): # kwargs = {OPTION_NAME: Argument instance, ...}
        self.options = {}
        self.sbatch = {}
        self.extra = {}
        for name, arg in kwargs.items():
            if name in Slurm.OPTIONS:
                setattr(self, name, arg.value)
                self.options[name] = arg
                if name in Slurm.SBATCH_OPTIONS:
                    self.sbatch[name] = arg
                else: #name in Slurm.EXTRA_OPTIONS
                    self.extra[name] = arg

        # slurm parameters (core) - shortcut - arguments
        # self.array = Argument(array, False, "Index of array job (e.g. 0-15 or 0,6,16-32)") # -a <e.x: 0-15 or 0,6,16-32>
        # self.account = Argument(account, False, "Cluster account to submit the job") # -A <account>
        # self.dependency = Argument(dependency, False, "Defer the start of this job until the specified dependencies have been satisfied completed") # -d
        # self.chdir = Argument(chdir, False, "Working directory path") # -D <working directory path>
        # self.error = Argument(error, False, "Error file") # -e <error file path>
        # self.job_name = Argument(job_name, False, "Name for the job allocation") # -J <str>
        # self.cluster = Argument(cluster, False, "") # -M <cluster name>
        # self.distribution = Argument(distribution, True, "Distribution methods for remote processes (<block|cyclic|plane|arbitrary>)") # -m <block|cyclic|plane|arbitrary>
        # self.mail_type = Argument(mail_type, False, "Event types to notify user by email(<BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>)") # NONE <BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>, PP: percent of the limit time
        # self.mail_user = Argument(mail_user, False, "User email") # NONE <user email>
        # self.mem = Argument(mem, False, "Memory per node (<size[units]>)") # NONE <size[units]>, units = [K|M|G|T] (memory per node)
        # self.mem_per_cpu = Argument(mem_per_cpu, False, "Minimum memory required per allocated CPU (<size[units]>)") # NONE <size[units]>
        # self.cpus_per_task = Argument(cpus_per_task, True, "Number of processors per task") # -c <ncpus>
        # self.nodes = Argument(nodes, True, "(<minnodes[-maxnodes]>)") # -N <minnodes[-maxnodes]>
        # self.ntasks = Argument(ntasks, True, "Number of tasks") # -n <number of tasks>
        # self.nice = Argument(nice, False, "Run the job with an adjusted scheduling") # NONE <adjustment>, adjustment is between +- 2147483645
        # self.output = Argument(output, True, "Output file name (default: slurm-%j.out)") # -o <path>
        # self.open_mode = Argument(open_mode, True, "Output open mode (<append|truncate>)") # NONE <append|truncate>
        # self.partition = Argument(partition, True, "Partition to submit job") # -p <partition>
        # self.reservation = Argument(reservation, False, "Resource reservation name") # NONE <reservation>
        # self.time = Argument(time, False, "Limit of time (format: DD-HH:MM:SS)") # -t <time>
        # # time formats: MM, MM:SS, HH:MM:SS, DD-HH, DD-HH:MM, DD-HH:MM:SS
        # # DD:days, HH:hours, MM: minutes, SS:secconds
        # self.test_only = Argument(test_only, True, "Validate the batch script and return an estimate of when a job would be scheduled to run. No job is actually submitted") # NONE <NO VALUE>,if testOnly=True enable this flag otherwise omit
        # self.verbose = Argument(verbose, True, "Increase the verbosity of sbatch's informational messages") # -v <NO VALUE>, if verbose=True enable this flag otherwise omit
        # self.nodelist = Argument(nodelist, False, "Nodelist") # -w <nodelist>, e.x. nodelist = hw[00-04,06,08]
        # self.wait = Argument(wait, True, "Do not exit until the submitted job terminates") # -W <NO VALUE>, if wait=True enable this flag otherwise omit
        # self.exclude = Argument(exclude, False, "Do not exit until the submitted job terminates") # -x <nodelist>
        # self.gpu = Argument(gpu, False, "Number of GPUS")

        # # extra parameters
        # self.slurm_script = Argument(slurm_script, True, "Name for the generated batch script")

    # @staticmethod
    # def parserJob(core):
    #     """
    #     core : is the core dictonary returned by  coreParameters methods
    #     """
    #     if core["gpus"] == 0 and core["nodes"] == 1 and core["ntasks"] == 1 and core["cpus_per_task"] > 1:
    #         return "OMP"

    #     elif core["gpus"] == 0 and core["nodes"] >= 1 and core["ntasks"] >= 1 and core["cpus_per_task"] == 1:
    #         return "MPI"

    #     elif core["gpus"] > 0 and core["nodes"] == 1 and core["ntasks"] == 1 and core["cpus_per_task"] == 1:
    #         return "GPU"

    #     elif core["gpus"] > 0 and core["nodes"] >= 1 and core["ntasks"] >= 1 and core["cpus_per_task"] >= 1:
    #         raise HybridWorkError({'gpus': core['gpus'], 'nodes': core['nodes'],
    #                                'ntasks': core["ntasks"], 'cpu_per_task': core['cpu_per_task']})
    #     else:
    #         raise SlurmParametersError(core)



    def parallel_job_parser(self):
        """
        Parser the sbatch options and return the type of parallel job (OMP, MPI, GPU[CUDA-OPENCL])

        Return
          parallel job type : OMP or MPI or GPU
        """
        #import pdb; pdb.set_trace()
        gpus = self.sbatch.get('gpu', 0)
        nodes = self.sbatch.get('nodes', 1)
        ntasks = self.sbatch.get('ntasks', 1)
        cpus_per_task = self.sbatch.get('cpus_per_task', 1)

        if gpus == 0 and nodes == 1 and ntasks == 1 and cpus_per_task > 1:
            return "OMP"

        elif gpus == 0 and nodes >= 1 and ntasks >= 1 and cpus_per_task == 1:
            return "MPI"

        elif gpus > 0 and nodes == 1 and ntasks == 1 and cpus_per_task == 1:
            return "GPU"

        elif gpus > 0 and nodes >= 1 and ntasks >= 1 and cpus_per_task >= 1:
            raise HybridWorkError({'gpus': gpus, 'nodes': nodes,
                                   'ntasks': ntasks, 'cpu_per_task': cpu_per_task})
        else:
            invalid_parameters = self.options
            raise SlurmParametersError(invalid_parameters)


    def gen_batch_script(self, parallel_work: List[str] = None):
        """
        generate a slurm script to submit with sbatch using the slurm parameters(constructor parameters) and the parallel_work variable(list of task to perform)

        parallel_work (list[str]): paralell tasks to perform [task1, task2, ...]
        """
        #import pdb; pdb.set_trace()

        batch_script_name = self.extra.get('slurm_script', 'attack.sh')


        with open(batch_script_name, 'w') as batch_script:
            batch_script.write("#!/bin/bash\n")
            for flag, argument in self.sbatch.items():
                if flag == "gpu" and argument > 0:
                    flag = flag.replace("_", "-")
                    batch_script.write(f"#SBATCH --gres={flag}:{argument.value}\n")
                else:
                    if isinstance(argument.value, bool):
                        if argument.value:
                            flag = flag.replace("_", "-")
                            batch_script.write(f"#SBATCH --{flag}\n")
                    else:
                        if argument.value:
                            flag = flag.replace("_", "-")
                            batch_script.write(f"#SBATCH --{flag}={argument.value}\n")

            if self.parallel_job_parser() == "OMP":
                batch_script.write("export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK\n")

            whiteLine = "\n"
            batch_script.write(whiteLine)
            for block in parallel_work:
                batch_script.write(whiteLine)
                for task in block:
                    batch_script.write(f"{task}\n")


        print_successful(f"Batch script generated: {batch_script_name}")

        return batch_script_name


    # @staticmethod
    # def gen_batchScript(core, extra, parallelWork):
    #     """
    #     [core, extra] are the variable returned by coreParameters method
    #     generate a slurm script to submit with sbatch using the slurm parameters(slurm constructor parameters) and the parallelWork variable(list of task to perform)

    #     parallelWork (list[str]): paralell tasks to perform [task1, task2, ...]
    #     """
    #     #import pdb; pdb.set_trace()
    #     #slurm, extra = self.parameters()
    #     slurmScriptName = extra['slurm-script']


    #     with open(slurmScriptName, 'w') as slurmScript:
    #         slurmScript.write("#!/bin/bash\n")
    #         for flag, argument in core.items():
    #             if not flag == "gpu" and (argument is not None):
    #                 if argument in ["True", "False"]:
    #                     if argument == "True":
    #                         flag = flag.replace("_", "-")
    #                         slurmScript.write(f"#SBATCH --{flag}={argument}\n")
    #                 else:
    #                     flag = flag.replace("_", "-")
    #                     slurmScript.write(f"#SBATCH --{flag}={argument}\n")

    #             else: # gpu flag
    #                 if argument > 0:
    #                     flag = flag.replace("_", "-")
    #                     slurmScript.write(f"#SBATCH --gres={flag}:{argument}\n")

    #         if Slurm.parserJob(core) == "OMP":
    #             slurmScript.write("export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK\n")


    #         whiteLine = "\n"
    #         slurmScript.write(whiteLine)
    #         for task in parallelWork:
    #             slurmScript.write(f"{task}\n")

    #     print_successful(f"Batch script generated: {slurmScriptName}")
