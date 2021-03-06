#!/usr/bin/env python3
#
# brute force attack using hashcat
#
# date: Feb 21 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os

# base  imports
from ama.core.modules.base import (
    Attack,
    Argument
)

# cracker imports
from ama.core.plugins.cracker import Hashcat

# slurm import
from ama.core.slurm import Slurm

#fineprint status
from fineprint.status import (
    print_failure,
    print_status
)


class HashcatBruteForce(Attack):
    """
    Brute force Attack using hashcat cracker
    """

    DESCRIPTION = "Brute force attack using Hashcat"
    MNAME = "attack/hashes/hashcat_brute_force"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform brute force attacks against hashes
        with hashcat submiting parallel tasks in a cluster using Slurm
        """
    )

    REFERENCES=None

    def __init__(self, *,
                 hash_type: str = None, hashes_file: str = None, mask:str = None,
                 slurm = None):
        """
        Initialization of wordlist attack using hashcat
        """

        attack_options = {
            'mask': Argument(mask, True, "Mask to attack"),
            'hash_type': Argument(hash_type, True, "Hashcat hash type"),
            'hashes_file': Argument(hashes_file, True, "Hashes file")
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
                "gpu": Argument(1, True, "Number of GPUS"),
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
            'mname' : HashcatBruteForce.MNAME,
            'author': HashcatBruteForce.AUTHOR,
            'description': HashcatBruteForce.DESCRIPTION,
            'fulldescription':  HashcatBruteForce.FULLDESCRIPTION,
            'references': HashcatBruteForce.REFERENCES,
            'attack_options': attack_options,
            'slurm': slurm
        }
        super().__init__(**init_options)


    # debugged - date: Mar 6 2021
    def attack(self, local:bool):
        """
        Wordlist attack using Hashcat

        Args:
           local (bool): if local is True run attack localy otherwise
                         submiting parallel tasks in a cluster using slurm
        """
        #import pdb; pdb.set_trace()

        try:
            self.no_empty_required_options()
            hc = Hashcat()

            if local:
                hc.brute_force_attack(hash_type = self.options['hash_type'].value,
                                      hashes_file = self.options['hashes_file'].value,
                                      mask = self.options['mask'].value,
                                      slurm = None)

            else:
                hc.brute_force_attack(hash_type = self.options['hash_type'].value,
                                      hashes_file = self.options['hashes_file'].value,
                                      mask = self.options['mask'].value,
                                      slurm = self.slurm)

        except Exception as error:
            print_failure(error)
