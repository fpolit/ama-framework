#!/usr/bin/env python3
#
# Hydra Cracker
#
# Feb 23 2021
# Implementation of Hydra password cracker
#
# Maintainer: glozanoa <glozanoa@uni.pe>

# slurm import
from ...slurm import Slurm

# cracker modules import
from .cracker import PasswordCracker

# cracker exceptions import
from .crackerException import InvalidServiceError

# validator module imports
from ...validator import Args

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

    def __init__(self):
        """
        Hydra password cracker
        This class implement the diverse attack of hydra and its benchmark
        Suported Attacks: wordlist, incremental, masks, single, combination, hybrid
        """
        super().__init__(name=["hydra"])


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


    def wordlistAttack(user=None, usersFile=None, passwdFile=None,
                       usersPasswdFile=None,port=None, ip4=True,
                       output=None, outputFormat=None, verbose=True,
                       stopInSucess=False, stopInSucessPerTarget=True,
                       targetsFile=None, target=None, service=None, slurm=None):

        """
        Perform a wordlist attack against services using hydra
        submiting parallel task in a cluster using slurm.

        Args:
        user (str): None,
        usersFile (str): None,
        passwdFile (str): None,
        usersPasswdFile (str): None,
        port (str): None,
        ip4 (str): True,
        output=None,
        outputFormat=None,
        verbose=True,
        stopInSucess=False,
        stopInSucessPerTarget=True,
        targetsFile=None,
        target=None,
        service=None
        slurm = None
        """

        if self.status:
            try:
                # validation of data
                Args.notNone(service)
                Args.someNotNone(user, usersFile)
                Args.someNotNone(passwdFile, usersPasswdFile)
                Args.someNotNone(target, targetsFile)

                permission = [os.R_OK]
                Path.access(permission,
                            usersFile, passwdFile, usersPasswdFile, targetsFile)
                Hydra.checkService(service)

                cmd2.Cmd.poutput(f"Attacking {service} service of {target} target  with {wordlist} wordlist.")
                if slurm.partition:
                    parallelJobType = slurm.parserParallelJob()
                    if not  parallelJobType in ["OMP"]:
                        raise InvalidParallelJobError(parallelJobType)

                    core, extra = slurm.parameters()

                    attackCmd = f"{self.mainexec}"

                    # user and password flags
                    if usersPasswdFile:
                        attackCmd += f" -C {usersPasswdFile}"
                    else:
                        # user
                        if user:
                            attackCmd += f" -l {user}"
                        else: # use userFile as users file
                            attackCmd += f" -L {usersFile}"

                        # passwords
                        attackCmd += f" -P {passwdfile}"

                    # port
                    if port:
                        attackCmd += f" -s {port}"

                    # output
                    if output:
                        attackCmd += f" -o {output}"

                    # ip version
                    if ip4:
                        attackCmd += " -4"
                    else: # ipv6
                        attackCmd += " -6"

                    # exit if success
                    if stopInSucessPerTarget:
                        attackCmd += " -f"

                    if stopInSucess:
                        attackCmd += " -F"

                    # target
                    if targetsFile:
                        attackCmd += f" -M {targetsFile}"
                    else: # simple target
                        attackCmd += f" {target}"

                    # service
                    attackCmd += f" {service}"


                    parallelWork = (
                        attackCmd
                    )

                    Slurm.genScript(core, extra, parallelWork)
                    slurmScriptName = extra['slurm-script']
                    Bash.exec(f"sbatch {slurmScriptName}")

                else:
                    attackCmd = f"{self.mainexec}"

                    # user and password flags
                    if usersPasswdFile:
                        attackCmd += f" -C {usersPasswdFile}"
                    else:
                        # user
                        if user:
                            attackCmd += f" -l {user}"
                        else: # use userFile as users file
                            attackCmd += f" -L {usersFile}"

                        # passwords
                        attackCmd += f" -P {passwdfile}"

                    # port
                    if port:
                        attackCmd += f" -s {port}"

                    # output
                    if output:
                        attackCmd += f" -o {output}"

                    # ip version
                    if ip4:
                        attackCmd += " -4"
                    else: # ipv6
                        attackCmd += " -6"

                    # exit if success
                    if stopInSucessPerTarget:
                        attackCmd += " -f"

                    if stopInSucess:
                        attackCmd += " -F"

                    # target
                    if targetsFile:
                        attackCmd += f" -M {targetsFile}"
                    else: # simple target
                        attackCmd += f" {target}"

                    # service
                    attackCmd += f" {service}"

                    Bash.exec(attackCmd)

            except Exception as error:
                cmd2.Cmd.pexcept(error)

        else:
            cmd2.Cmd.pwarning("Cracker {self.mainName} is disable")



    # def (user=None, usersFile=None, passwdFile=None,
    #                    usersPasswdFile=None,port=None, ip4=True,
    #                    output=None, outputFormat=None, verbose=True,
    #                    stopInSucess=False, stopInSucessPerTarget=True,
    #                    targetsFile=None, target=None, service=None):
