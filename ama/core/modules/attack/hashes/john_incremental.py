#!/usr/bin/env python3
#
# incremental attack using john
# NOTE: rewite module (copied from john_wordlist module)
#
# date: Feb 21 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import Any

# base  imports
from ama.core.modules.base import (
    Attack,
    Argument
)

# cracker imports
from ama.core.plugins.cracker import John

# slurm import
from ama.core.slurm import Slurm

# fineprint imports
from fineprint.status import print_failure

# debugged - date: Feb 28 2021
class JohnIncremental(Attack):
    """
    Wordlist Attack using john cracker
    """

    DESCRIPTION = "Incremental attack using John The Ripper"
    MNAME = "attack/hashes/john_incremental"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform incremental attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )

    REFERENCES = None

    def __init__(self, *, hash_type=None, hashes_file=None, slurm=None):
        """
        Initialization of John incremental attack

        Args:
        hash_type (str): Jonh's hash type
        hashes_file (str): Hash file to attack
        slurm (Slurm): Instance of Slurm class
        """

        attack_options = {
            'hash_type': Argument(hash_type, True, "John hash type"),
            'hashes_file': Argument(hashes_file, True, "hashes file")
        }

        if slurm is None:
            slurm_options = {
                "account": Argument(None, False, "Cluster account to submit the job"),
                "dependency": Argument(None, False, "Defer the start of this job until the specified dependencies have been satisfied completed"),
                "chdir" : Argument(os.getcwd(), True, "Working directory path"),
                "error": Argument(None, False, "Error file"),
                "job_name" : Argument('attack', False, "Name for the job allocation"),
                "cluster" : Argument(None, False, "Cluster Name"),
                "distribution": Argument('block', True, "Distribution methods for remote processes (<block|cyclic|plane|arbitrary>)"),
                "mail_type": Argument(None, False, "Event types to notify user by email(<BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>)"),
                "main_user": Argument(None, False, "User email"),
                "mem": Argument(None, False, "Memory per node (<size[units]>)"),
                "mem_per_cpu": Argument(None, False, "Minimum memory required per allocated CPU (<size[units]>)"),
                "cpus_per_task": Argument(1, True, "Number of processors per task"),
                "nodes": Argument(1, True, "Number of nodes(<minnodes[-maxnodes]>)"),
                "ntasks": Argument(1, True, "Number of tasks"),
                "nice": Argument(None, False, "Run the job with an adjusted scheduling"),
                "output": Argument('slurm-%j.out', True, "Output file name"),
                "open_mode": Argument('truncate', True, "Output open mode (<append|truncate>)"),
                "partition": Argument(None, True, "Partition to submit job"),
                "reservation": Argument(None, False, "Resource reservation name"),
                "time": Argument(None, False, "Limit of time (format: DD-HH:MM:SS)"),
                "test_only": Argument(False, True, "Validate the batch script and return an estimate of when a job would be scheduled to run. No job is actually submitted"),
                "verbose": Argument(False, True, "Increase the verbosity of sbatch's informational messages"),
                "nodelist": Argument(None, False, "Nodelist"),
                "wait": Argument(False, True, "Do not exit until the submitted job terminates"),
                "exclude": Argument(None, False, "Do not exit until the submitted job terminates"),
                'batch_script': Argument('attack.sh', True, "Name for the generated batch script"),
                'pmix': Argument('pmix_v3', True, "MPI type")
            }

            slurm = Slurm(**slurm_options)

        init_options = {
            'mname' : JohnIncremental.MNAME,
            'author': JohnIncremental.AUTHOR,
            'description': JohnIncremental.DESCRIPTION,
            'fulldescription':  JohnIncremental.FULLDESCRIPTION,
            'references': JohnIncremental.REFERENCES,
            'attack_options': attack_options,
            'slurm': slurm
        }

        super().__init__(**init_options)

    def attack(self, local:bool = False, pre_attack_output: Any = None):
        """
        Incremental attack using John the Ripper
        """

        try:
            self.no_empty_required_options()
            jtr = John()
            jtr.incremental_attack(hash_type = self.options['hash_type'].value,
                                   hashes_file = self.options['hashes_file'].value,
                                   slurm = self.slurm)

        except Exception as error:
            print_failure(error)
