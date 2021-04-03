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
from fineprint.color import ColorStr

# base imports
from ama.core.modules.base.argFormat import Argument

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


        print_successful(f"Batch script generated: {ColorStr(batch_script_name).StyleBRIGHT}")

        return batch_script_name
