#!/usr/bin/env python3
#
# Hydra Cracker
#
# Feb 23 2021
# Implementation of Hydra password cracker
#
# Maintainer: glozanoa <glozanoa@uni.pe>
import os
from fineprint.status import print_failure
from sbash import Bash

# slurm import
from ...slurm import Slurm

# cracker modules import
from .password_cracker import PasswordCracker

# cracker exceptions import
from .crackerException import InvalidParallelJob

# validator module imports
from ama.core.validator import Args
from ama.core.files import Path


class Hydra(PasswordCracker):
    SERVICES = ("adam6500", "asterisk", "afp", "cisco", "cisco-enable", "cvs", "firebird", "ftp", "ftps",
                "http-head", "http-get", "http-post", "https-head", "https-get", "https-post",
                "http-get-form", "http-post-form", "https-get-form", "https-post-form", "http-proxy",
                "http-proxy-urlenum", "icq", "imap", "imaps", "irc", "ldap2", "ldap2s",
                "ldap3[-{cram|digest}md5][s]","memcached", "mongodb", "mssql", "mysql", "nntp",
                "oracle-listener", "oracle-sid", "pcanywhere", "pcnfs", "pop3", "pop3s", "postgres",
                "radmin2", "rdp", "redis", "rexec", "rlogin", "rpcap", "rsh", "rtsp",
                "s7-300", "sip", "smb", "smtp", "smtps", "smtp-enum", "snmp", "socks5", "ssh",
                "sshkey", "svn", "teamspeak", "telnet", "telnets", "vmauthd", "vnc", "xmpp")

    MAINNAME = "hydra"
    def __init__(self):
        """
        Hydra password cracker
        This class implement the diverse attack of hydra and its benchmark
        Suported Attacks: wordlist, incremental, masks, single, combination, hybrid
        """
        super().__init__(name=["hydra"], version="v9.1")


    @staticmethod
    def checkService(service):
        """
        check if service is a supported hydra service

        Args:
        service (str): service

        Raise:
        InvalidServiceError: Error if service is an unsupported hydra service
        """

        if not (service in Hydra.SERVICES):
            raise InvalidServiceError(service)


    #debugged - date: Mar 13 2021
    def wordlist_attack(self, *, user=None, users_file=None,
                        passwd = None, passwd_file=None,
                        users_passwd_file=None,port=None, ip4=True,
                        output=None, output_format=None, verbose=True,
                        stopInSuccess=False, stopInSuccessPerTarget=True,
                        targets_file=None, target=None, service=None,
                        slurm=None):

        """
        Perform a wordlist attack against services using hydra
        submiting parallel task in a cluster using slurm.

        Args:
        user (str): None,
        users_file (str): None,
        passwd_file (str): None,
        users_passwd_file (str): None,
        port (str): None,
        ip4 (str): True,
        output=None,
        output_format=None,
        verbose=True,
        stopInSucess=False,
        stopInSucessPerTarget=True,
        targets_file=None,
        target=None,
        service=None
        slurm = None
        """

        #import pdb; pdb.set_trace()
        if self.enable:
            try:
                # validation of data
                Args.not_none(service)
                Args.some_not_none(user, users_file)
                Args.some_not_none(passwd, passwd_file, users_passwd_file)
                Args.some_not_none(target, targets_file)

                permission = [os.R_OK]
                Hydra.checkService(service)

                #cmd2.Cmd.poutput(f"Attacking {service} service of {target} target  with {wordlist} wordlist.")
                #print_failure(f"Attacking {service} service of {target} target  with {wordlist} wordlist.")

                attack_cmd = f"{self.main_exec}"

                # user and password flags
                if users_passwd_file:
                    Path.access(permission, users_passwd_file)
                    attack_cmd += f" -C {users_passwd_file}"
                else:
                    # user
                    if user:
                        attack_cmd += f" -l {user}"
                    else: # use userFile as users file
                        Path.access(permission, users_file)
                        attack_cmd += f" -L {users_file}"


                    # passwords
                    if passwd:
                        attack_cmd += f" -p {passwd}"
                    else: # passwd_file is not None
                        Path.access(permission, passwd_file)
                        attack_cmd += f" -P {passwd_file}"

                # port
                if port:
                    attack_cmd += f" -s {port}"

                # output
                if output:
                    attack_cmd += f" -o {output}"

                # ip version
                if ip4:
                    attack_cmd += " -4"
                else: # ipv6
                    attack_cmd += " -6"

                # verbose
                if verbose:
                    attack_cmd += " -V"

                # exit if success
                if stopInSuccessPerTarget:
                    attack_cmd += " -f"

                if stopInSuccess:
                    attack_cmd += " -F"

                # target
                if targets_file:
                    Path.access(permission, targets_file)
                    attack_cmd += f" -M {targets_file}"
                else: # simple target
                    attack_cmd += f" {target}"

                # service
                attack_cmd += f" {service}"

                if slurm.partition:
                    parallel_job_type = slurm.parallel_job_parser()
                    if not  parallel_job_type in ["OMP"]:
                        raise InvalidParallelJob(parallel_job_type)

                    parallel_work = [
                        attack_cmd
                    ]

                    batch_script_name = slurm.gen_batch_script(parallel_work)
                    Bash.exec(f"sbatch {batch_script_name}")

                else:
                    Bash.exec(attack_cmd)

            except Exception as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

        else:
            #cmd2.Cmd.pwarning(f"Cracker {self.main_name} is disable")
            print_failure(f"Cracker {self.main_name} is disable")
