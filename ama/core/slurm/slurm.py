#!/usr/bin/env python3
#
# Slurm class to manage sbatch parameters to submit parallel jobs
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import re
import os
from typing import List

#finprint imports
from fineprint.status import (
    print_successful,
    print_status
)
from fineprint.color import ColorStr


from ama.core.modules.base.argFormat import Argument
from ama.core.files import Path

class Slurm:
    """
    Manage sbatch parameters to submit parallel jobs
    """

    # sbatch options
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

    EXTRA_SBATCH_OPTIONS = [
        "batch_script",
        "pmix"
    ]

    OPTIONS = [*SBATCH_OPTIONS, *EXTRA_SBATCH_OPTIONS]

    # slurm.conf file options
    SLURM_CORE = [
        "ClusterName",
        "ControlMachine",
        "ControlAddr",
        "BackupController",
        "BackupAddr",
        "SlurmUser",
        "SlurmdUser",
        "SlurmctldPort",
        "SlurmdPort",
        "AuthType",
        #JobCredentialPrivateKey=
        #JobCredentialPublicCertificate=
        "StateSaveLocation",
        "SlurmdSpoolDir",
        "SwitchType",
        "MpiDefault",
        "SlurmctldPidFile",
        "SlurmdPidFile",
        "ProctrackType",
        #PluginDir=
        #FirstJobId=
        "ReturnToService",
        #MaxJobCount=
        #PlugStackConfig=
        #PropagatePrioProcess=
        #PropagateResourceLimits=
        #PropagateResourceLimitsExcept=
        #Prolog=
        #Epilog=
        #SrunProlog=
        #SrunEpilog=
        #TaskProlog=
        #TaskEpilog=
        #TaskPlugin=
        #TrackWCKey=no
        #TreeWidth=50
        #TmpFS=
        #UsePAM=
    ]

    SLURM_TIMERS = [
        "SlurmctldTimeout",
        "SlurmdTimeout",
        "InactiveLimit",
        "MinJobAge",
        "KillWait",
        "Waittime",
    ]

    SLURM_SCHEDULING = [
        "SchedulerType",
        #SchedulerAuth=
        #SelectType=select/cons_tres
        "selectType",
        "SelectTypeParameters",
        #PriorityType=priority/multifactor
        #PriorityDecayHalfLife=14-0
        #PriorityUsageResetPeriod=14-0
        #PriorityWeightFairshare=100000
        #PriorityWeightAge=1000
        #PriorityWeightPartition=10000
        #PriorityWeightJobSize=1000
        #PriorityMaxAge=1-0
    ]

    SLURM_LOGGING = [
        "SlurmctldDebug",
        "SlurmctldLogFile",
        "SlurmdDebug",
        "SlurmdLogFile",
        "JobCompType",
        #JobCompLoc=
    ]

    SLURM_ACCOUNTING = [
        #JobAcctGatherType=jobacct_gather/linux
        #JobAcctGatherFrequency=30
        #AccountingStorageType=accounting_storage/slurmdbd
        #AccountingStorageHost=
        #AccountingStorageLoc=
        #AccountingStoragePass=
        #AccountingStorageUser=
    ]

    SLURM_GPU = [
        "GresTypes",
    ]

    CONFIG_OPTIONS = [
        *SLURM_CORE,
        *SLURM_TIMERS,
        *SLURM_SCHEDULING,
        *SLURM_LOGGING,
        *SLURM_ACCOUNTING,
        *SLURM_GPU
    ]

    CONFIG_NODES = [
        "NodeName",
        "Gres",
        "NodeAddr",
        "CPUs",
        "Boards",
        "SocketsPerBoard",
        "CoresPerSocket",
        "ThreadsPerCore",
        "RealMemory",
    ]

    CONFIG_PARTITIONS = [
        "PartitionName",
        "Nodes",
        "Default",
        "MaxTime",
        "State",
    ]


    def __init__(self, **kwargs): # kwargs = {OPTION_NAME: Argument instance, ...}
        self.options = {}
        self.sbatch = {}
        self.extra = {} # extra sbatch options
        for name, arg in kwargs.items():
            if name in Slurm.OPTIONS:
                setattr(self, name, arg.value)
                self.options[name] = arg
                if name in Slurm.SBATCH_OPTIONS:
                    self.sbatch[name] = arg
                else: #name in Slurm.EXTRA_SBATCH_OPTIONS
                    self.extra[name] = arg


    def set_option(self, name, value):
        #import pdb;pdb.set_trace()
        if name in Slurm.OPTIONS:
            setattr(self, name, value)
            self.options[name].value = value
            if name in Slurm.SBATCH_OPTIONS:
                self.sbatch[name].value = value
            else: # option is a extra option
                self.extra[name].value = value
        else:
            raise Exception(f"{{ColorStr(name).StyleBRIGHT}} option isn't a valid slurm's option")

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

        batch_script_name = self.batch_script if self.batch_script is not None else 'attack.sh'


        with open(batch_script_name, 'w') as batch_script:
            batch_script.write("#!/bin/bash\n")
            for flag, argument in self.sbatch.items():
                if flag == "gpu" and (argument.value is not None and argument.value > 0):
                    flag = flag.replace("_", "-")
                    batch_script.write(f"#SBATCH --gres={flag}:{argument.value}\n")

                elif flag == 'array' and (argument.value is not None and argument.value > 0):
                    batch_script.write(f"#SBATCH --array=0-{argument.value-1}\n")
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


    @staticmethod
    def find_slurm_config():
        """
        Parse slurm.conf file to get the configurations (IP4s of nodes, partitions, nodes resources)

        force[bool] :force parsing even when slurm_conf file wasn't supplied, searching 'slurm.conf' file in POSSIBLE_SLURM_PATH
        """

        POSSIBLE_SLURM_PATH = [Path('/etc/slurm-llnl'),
                               Path('/etc/slurm')]

        slurm_conf = 'slurm.conf'

        for slurm_path in POSSIBLE_SLURM_PATH:
            if slurm_path.exists():
                for base, dirs, files in os.walk(slurm_path):
                    if slurm_conf in files:
                        return os.path.join(base, slurm_conf)

        return None


    @staticmethod
    def parser_slurm_conf(slurm_conf:Path):
        """
        Parse a slurm.conf file and return a dictionary {SLURM_CONFIG_OPTION: VALUE},
        with exception of nodes and partitions options,
        where SLURM_CONFIG_OPTIONS = 'nodes' and VALUE is {NODE_NAME: {NODE_SPECIFICATIONS},...} and
        SLURM_CONFIG_OPTIONS = 'partitions' and VALUE is {PARTITION_NAME: {PARTITION_SPECIFICATIONS},...}
        """
        slurm_config = {}
        slurm_config['nodes'] = {}
        slurm_config['partitions'] = {}
        comment_line = re.compile(r'#(\w|\W|\.|\s)*', re.DOTALL)

        #import pdb;pdb.set_trace()
        with open(slurm_conf) as slurm_conf_file:
            for config_line in slurm_conf_file.readlines():
                config_line = config_line.rstrip()
                config = config_line.split('=')
                if comment_line.fullmatch(config_line) is not None:
                    continue

                #config hasn't SLURM_OPTION=VALUE structure
                #(it can be a comment or a more complex configuration as NodeName or PartitionName SLURM_OPTION)
                if len(config) != 2:
                    # configure line is a multi config (OPTION1=VALUE1 OPTION2=VALUE2 ...)
                    slurm_config_key = None
                    multi_config = {}
                    #import pdb;pdb.set_trace()
                    for config in re.split(r'\s+', config_line):
                        config = config.rstrip().split('=')
                        if len(config) == 2:
                            option, value = config
                            multi_config[option] = value

                    for option in multi_config:
                        if option in ['NodeName', 'NodeAddr']: # This line is a node definition
                            slurm_config_key = 'nodes'
                            break
                        elif option in ['PartitionName']: # This line is a partition definition
                            slurm_config_key = 'partitions'
                            break

                    if slurm_config_key:
                        if slurm_config_key == "nodes":
                            node_name = multi_config['NodeName']
                            slurm_config['nodes'][node_name] = multi_config
                        elif slurm_config_key == "partitions":
                            partition_name = multi_config['PartitionName']
                            slurm_config['partitions'][partition_name] = multi_config
                else:
                    option, value = config
                    if not comment_line.fullmatch(config_line):
                        slurm_config[option] = value

        return slurm_config
