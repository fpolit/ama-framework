#!/usr/bin/env python3
#
# Wordlist attack using Hydra Cracker
#
# Feb 23 2021
# Implementation of Hydra password cracker
#
# Maintainer: glozanoa <glozanoa@uni.pe>



# base  imports
from ama.core.modules.base import Attack

# cracker imports
from ama.core.cracker import Hydra


class HydraWordlist(Attack):
    """
    Wordlist Attack using hydra cracker
    """

    description = "Wordlist attack using Hydra"
    mname = "attack/hashes/hydra_wordlist"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    fuldescription = (
        """
        Perform wordlists attacks against services
        with hydra submiting parallel tasks in a cluster using Slurm
        """
        )
    def __init__(self, *, user=None, usersFile=None, passwdFile=None,
                       usersPasswdFile=None,port=None, ip4=True,
                       output=None, outputFormat=None, verbose=True,
                       stopInSucess=False, stopInSucessPerTarget=True,
                       targetsFile=None, target=None, service=None, slurm=None):
        """
        Initialization of hydra wordlist attack

        Args:
        Args:
        user (str): None,
        usersFile (str): None,
        passwdFile (str): None,
        usersPasswdFile (str): None,
        port (str): None,
        ip4 (str): True,
        output (str): None,
        outputFormat (str): None,
        verbose (bool): True,
        stopInSucess (bool): False,
        stopInSucessPerTarget (bool): True,
        targetsFile (str): None,
        target (str): None,
        service (str): None
        slurm (Slurm): Instance of Slurm class
        """
        attackOptions = {
            'user': user,
            'users_file': usersFile,
            'passwd_file': passwdFile,
            'users_passwd_file': usersPasswdFile,
            'port': port,
            'ip4': ip4,
            'output': output,
            'output_format' outputFormat,
            'verbose': verbose,
            'stop_in_sucess': stopInSucess,
            'stop_in_sucess_per_target': stopInSucessPerTarget,
            'targets_file': targetsFile,
            'target': target,
            'service': service
        }

        initOptions = {'mname' : nname,
                       'author': author,
                       'description': description,
                       'fulldescription':  fulldescription,
                       'atackOptions': attackOptions,
                       'slurm': slurm
                       }

        super().__init__(**initOptions)


    def attack(self):
        """
        Wordlist attack using Hydra
        """
        hydra = Hydra()
        hydra.wordlistAttack(user = self.user,
                             usersFile = self.users_file,
                             passwdFile = self.passwd_file,
                             usersPasswdFile = self.users_passwd_file,
                             port = self.port,
                             ip4 = self.ip4,
                             output = self.output,
                             outputFormat = self.output_format,
                             verbose = self.verbose,
                             stopInSucess = self.stop_in_sucess,
                             stopInSucessPerTarget = self.stop_in_sucess_per_target,
                             targetsFile = self.targets_file,
                             target = self.target,
                             service = self.service,
                             slurm = self.slurm)
