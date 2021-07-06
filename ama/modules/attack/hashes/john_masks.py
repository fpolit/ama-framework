#!/usr/bin/env python3
#
# masks attack using john
#
# date: Feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import Any
from fineprint.status import print_failure

from ama.core.modules.base import (
    Attack,
    Argument
)
from ama.core.modules.base.auxiliary import Auxiliary
from ama.core.plugins.cracker import John
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

class JohnMasks(Attack):
    """
    Mask Attack using john cracker
    """

    DESCRIPTION = "Masks attack using John The Ripper"
    MNAME = "attack/hashes/john_masks"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform mask attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
        )

    REFERENCES = None

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
                 hash_type:str = None, hashes_file:str = None,
                 masks_file: str = None, masks_attack: str = "masks_attack.py",
                 slurm: Slurm=None,
                 pre_attack = None, post_attack = None):
        """
        Initialization of John masks attack

        Args:
        hash_type (str): Jonh's hash type
        hashes_file (str): Hashes file to attack
        masks_file (str): Masks file
        masks_attack (str): Generated masks attack script
        slurm (Slurm): Instance of Slurm class
        """

        attack_options = {
            'hash_type': Argument(hash_type, True, "John hash types(split by commas)", value_type=str),
            'hashes_file': Argument(hashes_file, True, "Hashes file", value_type=str),
            'masks_file': Argument(masks_file, True, "Masks file", value_type=str),
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
            'mname' : JohnMasks.MNAME,
            'author': JohnMasks.AUTHOR,
            'description': JohnMasks.DESCRIPTION,
            'fulldescription':  JohnMasks.FULLDESCRIPTION,
            'references': JohnMasks.REFERENCES,
            'pre_attack': pre_attack,
            'attack_options': attack_options,
            'post_attack': post_attack,
            'slurm': slurm
        }

        super().__init__(**init_options)

    def attack(self, *,
               local=False, pre_attack_output: Any = None,
               db_status:bool = False, workspace:str = None, db_credential_file: Path = None,
               cracker_main_exec:Path = None,  slurm_conf = None):
        """
        Masks attack using John the Ripper
        Args:
          local (bool): try to perform the attack locally
        """
        #import pdb; pdb.set_trace()
        try:
            self.no_empty_required_options(local)

            if slurm_conf:
                self.slurm.config = slurm_conf

            if cracker_main_exec:
                jtr = John(john_exec=cracker_main_exec)
            else:
                jtr = John()

            hash_types  = self.options['hash_type'].value.split(',')
            hashes_file = Path(self.options['hashes_file'].value)
            masks_file = Path(self.options['masks_file'].value)

            jtr.masks_attack(hash_types = hash_types,
                             hashes_file = hashes_file,
                             masks_file= masks_file,
                             slurm = self.slurm,
                             local = local,
                             db_status= db_status,
                             workspace= workspace,
                             db_credential_file=db_credential_file)

        except Exception as error:
            print_failure(error)


    def setv(self, option, value, *, pre_attack: bool = False, post_attack: bool = False):
        #import pdb; pdb.set_trace()
        super().setv(option, value, pre_attack = pre_attack, post_attack = post_attack)

        option = option.lower()
        # attack ->  atack
        if option == "array":
            super().setv('output', 'slurm-%A_%a.out', pre_attack=False, post_attack=False)
