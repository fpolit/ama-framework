#!/usr/bin/env python3
#
# hybrid attack using hashcat
#
# Implemented - date: Apr 3 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import (
    List,
    Any
)
from fineprint.status import (
    print_failure,
    print_status
)


from ama.core.modules.base import (
    Attack,
    Argument,
    Auxiliary
)
from ama.core.plugins.cracker import Hashcat
from ama.core.slurm import Slurm
from ama.core.files import Path

# pre attack import
## auxiliary/hashes
from ama.core.modules.auxiliary.hashes import (
    HashID,
    Nth
)
## auxiliary/wordlist
from ama.core.modules.auxiliary.wordlists import (
    CuppInteractive
)

# post attack import
## auxiliary/hashes
from ama.core.modules.auxiliary.hashes import (
    HashesStatus
)


class HashcatHybrid(Attack):
    """
    Hybrid Attack using hashcat cracker
    """

    DESCRIPTION = "Hybrid attack using Hashcat"
    MNAME = "attack/hashes/hashcat_hybrid"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Perform hybrid attacks against hashes
        with hashcat submiting parallel tasks in a cluster using Slurm
        """
    )

    REFERENCES=None

    def __init__(self, *,
                 hash_type: str = None, hashes_file: str = None, inverse:bool = False,
                 wordlists: List[str] = None, masks = None,
                 slurm:Slurm = None,
                 pre_attack:Auxiliary = None, post_attack:Auxiliary = None):
        """
        Initialization of Hybrid Attack using hashcat cracker
        """

        attack_options = {
            'hash_type': Argument(hash_type, True, "Hashcat hash type"),
            'hashes_file': Argument(hashes_file, True, "Hashes file"),
            'wordlists': Argument(wordlists, True, "Wordlist files (split by commas)"),
            'masks': Argument(masks, True, "Masks(split by commas) or masks file"),
            'inverse': Argument(inverse, True, "Combine wordlists and masks in inverse form (masks + wordlists)"),
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
            'mname' : HashcatHybrid.MNAME,
            'author': HashcatHybrid.AUTHOR,
            'description': HashcatHybrid.DESCRIPTION,
            'fulldescription':  HashcatHybrid.FULLDESCRIPTION,
            'references': HashcatHybrid.REFERENCES,
            'pre_attack': pre_attack,
            'attack_options': attack_options,
            'post_attack': post_attack,
            'slurm': slurm
        }
        super().__init__(**init_options)


    def attack(self, *,
               local:bool = False, force:bool = False, pre_attack_output: Any = None,
               db_status:bool = False, workspace:str = None, db_credential_file: Path = None):
        """
        Hybrid Attack using hashcat cracker
        """
        #import pdb; pdb.set_trace()
        try:

            if not force:
                self.no_empty_required_options(local)


            hc = Hashcat()

            hash_type = None
            if isinstance(self.options['hash_type'].value, int):
                hash_types = [self.options['hash_type'].value]
            elif isinstance(self.options['hash_type'].value, str):
                hash_types = [int(hash_type) for hash_type in self.options['hash_type'].value.split(',')]
            else:
                raise TypeError(f"Invalid type hash_type: {type(hash_type)}")

            wordlists = [wordlist.strip() for wordlist in self.options['wordlists'].value.split(',')]

            masks = self.options['masks'].value

            if os.path.isfile(masks) and os.access(masks, os.R_OK): #a masks file was supplied
                masks_file = Path(masks)
                hc.hybrid_attack(
                    hash_types = hash_types,
                    hashes_file = self.options['hashes_file'].value,
                    inverse = self.options['inverse'].value,
                    wordlists = wordlists,
                    masks_file = masks_file,
                    slurm = self.slurm,
                    local = local,
                    db_status= db_status,
                    workspace= workspace,
                    db_credential_file=db_credential_file)

            else:
                masks = [mask.strip() for mask in masks.split(',')]
                hc.hybrid_attack(
                    hash_types = hash_types,
                    hashes_file = self.options['hashes_file'].value,
                    inverse = self.options['inverse'].value,
                    wordlists = wordlists,
                    masks = masks,
                    slurm = self.slurm,
                    local = local,
                    db_status= db_status,
                    workspace= workspace,
                    db_credential_file=db_credential_file)

        except Exception as error:
            print_failure(error)

