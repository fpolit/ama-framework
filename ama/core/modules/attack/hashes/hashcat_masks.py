#!/usr/bin/env python3
#
# Masks attack using hashcat
#
# implementation - date: Mar 6 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import Any
from fineprint.status import (
    print_failure,
    print_status
)


# base  imports
from ama.core.modules.base import (
    Attack,
    Argument,
    Auxiliary
)
from ama.core.plugins.cracker import Hashcat
from ama.core.slurm import Slurm
from ama.core.files import Path

# pre attack modules
## auxiliary/hashes
from ama.core.modules.auxiliary.hashes import (
    HashID,
    Nth
)

## auxiliary/wordlist
from ama.core.modules.auxiliary.wordlists import (
    CuppInteractive
)

## auxiliary/analysis
from ama.core.modules.auxiliary.analysis import (
    PackMaskgen,
    PackWholegen,
    PackPolicygen
)

# post attack import
from ama.core.modules.auxiliary.hashes import HashesStatus

class HashcatMasks(Attack):
    """
    Masks Attack using hashcat cracker
    """

    DESCRIPTION = "Masks attack using Hashcat"
    MNAME = "attack/hashes/hashcat_masks"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform masks attacks against hashes
        with hashcat submiting parallel tasks in a cluster using Slurm
        """
    )

    REFERENCES=None


    # {PRE_ATTACK_MNAME: PRE_ATTACK_CLASS, ...}
    PRE_ATTACKS = {
        # auxiliary/hashes
        f"{Nth.MNAME}": Nth,
        f"{HashID.MNAME}": HashID,

        # auxiliary/analysis
        f"{PackMaskgen.MNAME}": PackMaskgen,
        f"{PackWholegen.MNAME}": PackWholegen,
        f"{PackPolicygen.MNAME}": PackPolicygen,

        # auxiliary/wordlist
        f"{CuppInteractive.MNAME}": CuppInteractive,
    }

    # {POST_ATTACK_MNAME: POST_ATTACK_CLASS, ...}
    POST_ATTACKS = {
        # auxiliary/hashes
        f"{HashesStatus.MNAME}": HashesStatus,
    }

    def __init__(self, *,
                 hash_type: str = None, hashes_file: str = None,
                 masks_file:str = None,
                 sleep:int = 1,
                 slurm: Slurm = None,
                 pre_attack: Auxiliary = None, post_attack: Auxiliary = None):
        """
        Initialization of wordlist attack using hashcat
        """

        attack_options = {
            'hash_type': Argument(hash_type, True, "Hashcat hash type", value_type=int),
            'hashes_file': Argument(hashes_file, True, "Hashes file", value_type=str),
            'masks_file': Argument(masks_file, True, "Masks file", value_type=str),
            'sleep': Argument(sleep, True, 'Sleep time between each attack (seconds)', value_type=int)
        }


        if slurm is None:
            slurm_options = {
                "account": Argument(None, False, "Cluster account to submit the job", value_type=str),
                "array": Argument(None, False, "Number of array jobs", value_type=int),
                "dependency": Argument(None, False, "Defer the start of this job until the specified dependencies have been satisfied completed"),
                "chdir" : Argument(os.getcwd(), True, "Working directory path", value_type=str),
                "error": Argument(None, False, "Error file", value_type=str),
                "job_name" : Argument('attack', False, "Name for the job allocation", value_type=str),
                "cluster" : Argument(None, False, "Cluster Name", value_type=str),
                "distribution": Argument('block', True, "Distribution methods for remote processes (<block|cyclic|plane|arbitrary>)", value_type=str),
                "mail_type": Argument(None, False, "Event types to notify user by email(<BEGIN|END|FAIL|REQUEUE|ALL|TIME_LIMIT_PP>)", value_type=str),
                "main_user": Argument(None, False, "User email", value_type=str),
                "mem": Argument(None, False, "Memory per node (<size[units]>)", value_type=str),
                "mem_per_cpu": Argument(None, False, "Minimum memory required per allocated CPU (<size[units]>)", value_type=str),
                "cpus_per_task": Argument(1, True, "Number of processors per task", value_type=int),
                "nodes": Argument(1, True, "Number of nodes(<minnodes[-maxnodes]>)", value_type=int),
                "gpu": Argument(1, True, "Number of GPUS", value_type=int),
                "ntasks": Argument(1, True, "Number of tasks", value_type=int),
                "nice": Argument(None, False, "Run the job with an adjusted scheduling", value_type=int),
                "output": Argument('slurm-%j.out', True, "Output file name", value_type=str),
                "open_mode": Argument('truncate', True, "Output open mode (<append|truncate>)", value_type=str),
                "partition": Argument(None, True, "Partition to submit job", value_type=str),
                "reservation": Argument(None, False, "Resource reservation name", value_type=str),
                "time": Argument(None, False, "Limit of time (format: DD-HH:MM:SS)", value_type=str),
                "test_only": Argument(False, True, "Validate the batch script and return an estimate of when a job would be scheduled to run. No job is actually submitted", value_type=bool),
                "verbose": Argument(False, True, "Increase the verbosity of sbatch's informational messages", value_type=bool),
                "nodelist": Argument(None, False, "Nodelist", value_type=str),
                "wait": Argument(False, True, "Do not exit until the submitted job terminates", value_type=bool),
                "exclude": Argument(None, False, "Do not exit until the submitted job terminates", value_type=str),
                'batch_script': Argument('attack.sh', True, "Name for the generated batch script", value_type=str),
                'pmix': Argument('pmix_v3', True, "MPI type", value_type=str)
            }

            slurm = Slurm(**slurm_options)

        init_options = {
            'mname' : HashcatMasks.MNAME,
            'author': HashcatMasks.AUTHOR,
            'description': HashcatMasks.DESCRIPTION,
            'fulldescription':  HashcatMasks.FULLDESCRIPTION,
            'references': HashcatMasks.REFERENCES,
            'pre_attack': pre_attack,
            'attack_options': attack_options,
            'post_attack': post_attack,
            'slurm': slurm
        }
        super().__init__(**init_options)


    #debugged - date: Mar 6 2021
    def attack(self, *,
               local:bool = False, pre_attack_output: Any = None,
               db_status:bool = False, workspace:str = None, db_credential_file: Path = None,
               cracker_main_exec:Path = None, slurm_conf=None):
        """
        Wordlist attack using Hashcat

        Args:
           local (bool): if local is True run attack localy otherwise
                         submiting parallel tasks in a cluster using slurm
        """
        #import pdb; pdb.set_trace()

        try:

            self.no_empty_required_options(local)

            if not local and slurm_conf:
                self.slurm.config = slurm_conf

            if cracker_main_exec:
                hc = Hashcat(hashcat_exec=cracker_main_exec)
            else:
                hc = Hashcat()


            hash_type = None
            if isinstance(self.options['hash_type'].value, int):
                hash_types = [self.options['hash_type'].value]
            elif isinstance(self.options['hash_type'].value, str):
                hash_types = [int(hash_type) for hash_type in self.options['hash_type'].value.split(',')]
            else:
                raise TypeError(f"Invalid type hash_type: {type(hash_type)}")


            hc.masks_attack(hash_types = hash_types,
                            hashes_file = self.options['hashes_file'].value,
                            masks_file = self.options['masks_file'].value,
                            sleep = self.options['sleep'].value,
                            slurm = self.slurm,
                            local = local,
                            db_status= db_status,
                            workspace= workspace,
                            db_credential_file=db_credential_file)

        except Exception as error:
            print_failure(error)
