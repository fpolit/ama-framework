#!/usr/bin/env python3
#
# john benchmark
#
# Status: DEBUGGED - date: Jun 5 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import Any
import psutil

# base  imports
from ama.core.modules.base import (
    Attack,
    Argument
)

# cracker imports
from ama.core.plugins.cracker import John
from ama.core.files import Path

# slurm import
from ama.core.slurm import Slurm

# fineprint imports
from fineprint.status import print_failure, print_status

class JohnBenchmark(Attack):
    """
    john the ripper benchmark
    """

    DESCRIPTION = "John the Ripper benchmark"
    MNAME = "attack/hashes/john_benchmark"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform John benchmark submitting parallel task in a cluster using Slurm
        """
        )

    REFERENCES = None

    def __init__(self, slurm=None, pre_attack=None, post_attack=None):
        """
        Initialization of John benchmark class
        """
        attack_options = {
            "cores": Argument(1, False, "Number of cores to lunch MPI job (-1: MAXIMUM CORES)", value_type=int),
            "threads": Argument(-1, False, "Number of threads to lunch OMP job (-1: MAXIMUM THREADS)", value_type=int),
        }

        if slurm is None:
            slurm_options = {
                "account": Argument(None, False, "Cluster account to submit the job", value_type=str),
                "array": Argument(None, False, "Number of array jobs", value_type=int),
                "dependency": Argument(None, False, "Defer the start of this job until the specified dependencies have been satisfied completed"),
                "chdir" : Argument(os.getcwd(), True, "Working directory path", value_type=str),
                "error": Argument(None, False, "Error file"),
                "job_name" : Argument('attack', False, "Name for the job allocation", value_type=str),
                "cluster" : Argument(None, False, "Cluster Name"),
                "distribution": Argument('block', True, "Distribution methods for remote processes (<block|cyclic|plane|arbitrary>)", value_type=str),
                "mail_type": Argument(None, False, "Event types to notify user by email(<BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>)"),
                "mail_user": Argument(None, False, "User email"),
                "mem": Argument(None, False, "Memory per node (<size[units]>)"),
                "mem_per_cpu": Argument(None, False, "Minimum memory required per allocated CPU (<size[units]>)"),
                "cpus_per_task": Argument(1, True, "Number of processors per task", value_type=int),
                "nodes": Argument(1, True, "Number of nodes(<minnodes[-maxnodes]>)", value_type=int),
                "ntasks": Argument(1, True, "Number of tasks", value_type=int),
                "nice": Argument(None, False, "Run the job with an adjusted scheduling", value_type=int),
                "output": Argument('slurm-%j.out', True, "Output file name", value_type=str),
                "open_mode": Argument('truncate', True, "Output open mode (<append|truncate>)"),
                "partition": Argument(None, True, "Partition to submit job", value_type=str),
                "reservation": Argument(None, False, "Resource reservation name"),
                "time": Argument(None, False, "Limit of time (format: DD-HH:MM:SS)"),
                "test_only": Argument(False, True, "Validate the batch script and return an estimate of when a job would be scheduled to run. No job is actually submitted", value_type=bool),
                "verbose": Argument(False, True, "Increase the verbosity of sbatch's informational messages", value_type=bool),
                "nodelist": Argument(None, False, "Nodelist"),
                "wait": Argument(False, True, "Do not exit until the submitted job terminates", value_type=bool),
                "exclude": Argument(None, False, "Do not exit until the submitted job terminates"),
                'batch_script': Argument('attack.sh', True, "Name for the generated batch script", value_type=str),
                'pmix': Argument('pmix_v3', True, "MPI type", value_type=str)
            }

            slurm = Slurm(**slurm_options)

        init_options = {
            'mname' : JohnBenchmark.MNAME,
            'author': JohnBenchmark.AUTHOR,
            'description': JohnBenchmark.DESCRIPTION,
            'fulldescription':  JohnBenchmark.FULLDESCRIPTION,
            'references': JohnBenchmark.REFERENCES,
            'pre_attack': pre_attack,
            'attack_options': attack_options,
            'post_attack': post_attack,
            'slurm': slurm
        }

        super().__init__(**init_options)


    # debugged - date: Jun 5 2021
    def attack(self, *,
               local:bool = False, pre_attack_output: Any = None,
               db_status:bool = False, workspace:str = None, db_credential_file: Path = None,
               cracker_main_exec:Path = None, slurm_conf=None):
        """
        John the Ripper benchmark

        Args:
           local (bool): if local is True run attack localy otherwise
                         submiting parallel tasks in a cluster using slurm
        """
        #import pdb; pdb.set_trace()
        try:
            self.no_empty_required_options(local)

            if cracker_main_exec:
                jtr = John(john_exec=cracker_main_exec)
            else:
                jtr = John()

            jtr.benchmark(cores = self.options["cores"].value,
                          threads = self.options["threads"].value,
                          slurm = self.slurm,
                          local = local)

        except Exception as error:
            print_failure(error)


    def setv(self, option, value, *, pre_attack: bool = False, post_attack: bool = False):
        try:
            super().setv(option, value, pre_attack=pre_attack, post_attack = post_attack)
            option = option.lower()
            if option == "cores":
                max_cores = psutil.cpu_count(logical=False)
                cores = int(value)

                if cores <= -1 or cores > max_cores:
                    value = max_cores

                super().setv('NTASKS', value)

            elif option == "threads":
                max_threads = psutil.cpu_count(logical=True)
                threads = int(value)

                if threads <= -1 or threads > max_threads:
                    value = max_threads

                super().setv('CPUS_PER_TASK', value)

        except Exception as error:
            print_failure(error)
