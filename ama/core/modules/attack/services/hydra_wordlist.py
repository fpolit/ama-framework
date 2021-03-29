#!/usr/bin/env python3
#
# Wordlist attack using Hydra Cracker
#
# Feb 23 2021
# Implementation of Hydra password cracker
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import Any
from fineprint.status import print_failure

# base  imports
from ama.core.modules.base import (
    Attack,
    Argument
)

# slurm imports
from ama.core.slurm import Slurm

# cracker imports
from ama.core.plugins.cracker import Hydra


class HydraWordlist(Attack):
    """
    Wordlist Attack using hydra cracker
    """

    DESCRIPTION = "Wordlist attack using Hydra"
    MNAME = "attack/services/hydra_wordlist"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHOR = [
        "glozanoa <glozanoa@uni.pe>"
    ]

    FULLDESCRIPTION = (
        """
        Perform wordlists attacks against services
        with hydra submiting parallel tasks in a cluster using Slurm
        """
    )

    REFERENCES = [
        "https://www.hackingarticles.in/comprehensive-guide-on-hydra-a-brute-forcing-tool/",
        "https://github.com/vanhauser-thc/thc-hydra"
    ]

    # {PRE_ATTACK_MNAME: PRE_ATTACK_CLASS, ...}
    PRE_ATTACKS = {}

    # {POST_ATTACK_MNAME: POST_ATTACK_CLASS, ...}
    POST_ATTACKS = {}


    def __init__(self, *, users=None, passwords=None,
                 #users_passwd_file=None,
                 port=None, ip4=True,
                 output=None, output_format="text", verbose=True,
                 stopInSuccess=False, stopInSuccessPerTarget=True,
                 targets=None, service=None, slurm=None):

        attack_options = {
            'users': Argument(users, True, "User or users file to login" ),
            #'users_passwd_file': Argument(users_passwd_file),
            'passwords': Argument(passwords, True, "Password or Passwords file"),
            'port': Argument(port, False, "Service port"),
            'ip4': Argument(ip4, True, "Use Ip4 otherwise use IP6"),
            'output': Argument(output, False, "Output file"),
            'output_format': Argument(output_format, True, "Output format file <text|json|jsonv1>"),
            'verbose': Argument(verbose, True, "Show login+pass for each attempt"),
            'stop_in_success': Argument(stopInSuccess, True, "Exit when a login/pass pair is found (global)"),
            'stop_in_success_per_target': Argument(stopInSuccessPerTarget, True, "Exit when a login/pass pair is found (per target)"),
            'targets': Argument(targets, True, "Server (DNS, IP or 192.168.0.0/24) or servers (one target per line, ':' to specify port) to attack"),
            'service': Argument(service, True, "Service to crack")
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
            'mname' : HydraWordlist.MNAME,
            'author': HydraWordlist.AUTHOR,
            'description': HydraWordlist.DESCRIPTION,
            'fulldescription':  HydraWordlist.FULLDESCRIPTION,
            'references': HydraWordlist.REFERENCES,
            'attack_options': attack_options,
            'slurm': slurm
        }

        super().__init__(**init_options)


    #debugged - date: Mar 13 2021
    def attack(self, local:bool = False, pre_attack_output: Any = None):
        """
        Wordlist attack using Hydra
        """

        #import pdb; pdb.set_trace()

        try:
            self.no_empty_required_options(local)

            users = self.options['users'].value
            if os.path.isfile(users) and os.access(users, os.R_OK):
                users_file = users
                user = None
            else:
                user = users
                users_file = None

            passwords = self.options['passwords'].value
            if os.path.isfile(passwords) and os.access(passwords, os.R_OK):
                passwd_file = passwords
                passwd = None
            else:
                passwd = passwords
                passwd_file = None

            targets = self.options['targets'].value
            if os.path.isfile(targets) and os.access(targets, os.R_OK):
                targets_file = targets
                target = None
            else:
                target = targets
                targets_file = None

            hydra = Hydra()
            hydra.wordlist_attack(user = user, users_file = users_file,
                                  passwd = passwd, passwd_file = passwd_file,
                                  port = self.options['port'].value,
                                  ip4 = self.options['ip4'].value,
                                  output = self.options['output'].value,
                                  output_format = self.options['output_format'].value,
                                  verbose = self.options['verbose'].value,
                                  stopInSuccess = self.options['stop_in_success'].value,
                                  stopInSuccessPerTarget = self.options['stop_in_success_per_target'].value,
                                  targets_file = targets_file,
                                  target = target,
                                  service = self.options['service'].value,
                                  slurm = self.slurm)

        except Exception as error:
            print_failure(error)
