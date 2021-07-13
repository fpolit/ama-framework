#!/usr/bin/env python3
#
# Cerbrutus - network brute force tool
#
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import Any
import psutil
from pathlib import Path



from ama.modules.base import Attack
from ama.plugins.cracker import Cerbrutus
#from ama.utils.fineprint import print_failure, print_status
from ama.utils import Argument


class Cerbrutus(Attack):
    """
    Cerbrutus - network brute force tool
    """

    banner = """
    \t================================================================
    \t    __    ___  ____   ____   ____  __ __  ______  __ __  _____
    \t   /  ]  /  _]|    \ |    \ |    \|  |  ||      ||  |  |/ ___/
    \t  /  /  /  [_ |  D  )|  o  )|  D  )  |  ||      ||  |  (   \_
    \t /  /  |    _]|    / |     ||    /|  |  ||_|  |_||  |  |\__  |
    \t/   \_ |   [_ |    \ |  O  ||    \|  :  |  |  |  |  :  |/  \ |
    \t\     ||     ||  .  \|     ||  .  \     |  |  |  |     |\    |
    \t \____||_____||__|\_||_____||__|\_|\__,_|  |__|   \__,_| \___|
    \t
    \tNetwork Brute Force Tool
    \thttps://github.com/Cerbrutus-BruteForcer/cerbrutus
    \t================================================================
    """

    DESCRIPTION = "Cerbrutus - network brute force attack"
    MNAME = "attack/services/cerbrutus"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Network brute force attack
        """
    )

    REFERENCES = [
        "https://github.com/Cerbrutus-BruteForcer/cerbrutus"
    ]

    def __init__(self, host:str=None, service:str=None, users:str = None,
                 passwords:str = None, port:int = None, threads:int = None,
                 quiet:bool = True):
        """
        Initialization of John benchmark class
        """
        attack_options = {
            "HOST": Argument(host, False, "The host to connect to - in IP or VHOST/Domain Name form"),
            "SERVICE": Argument(service, False, "The service to brute force (currently implemented 'SSH')"),
            "USERS": Argument(users, False, "Either a single user, or the path to the file of users you wish to use"),
            "PASSWORDS": Argument(passwords, False, "Either a single password, or the path to the password list you wish to use"),
            "PORT": Argument(port, False, "The port you wish to target (only required if running on a non standard port)", value_type=int),
            "THREADS": Argument(threads, False, "Number of threads to use", value_type=int),
            "QUIET": Argument(quiet, False, "Do not print banner", value_type=bool)
        }

        init_options = {
            'mname' : Cerbrutus.MNAME,
            'authors': Cerbrutus.AUTHORS,
            'description': Cerbrutus.DESCRIPTION,
            'fulldescription':  Cerbrutus.FULLDESCRIPTION,
            'references': Cerbrutus.REFERENCES,
            'attack_options': attack_options
        }

        super().__init__(**init_options)


    # debugged - date: Jun 5 2021
    def attack(self):
        """
        Network brute force attack
        """
        #import pdb; pdb.set_trace()
        try:
            #self.no_empty_required_options(local)
            if self.options['QUIET'].value:
                print(Cerbrutus.banner)

            host = self.options['HOST'].value

            service = self.options['SERVICE'].value
            if service not in Cerbrutus.services.valid_services:
                raise Exception(f"Service named {service} does not yet exist...")

            port = Cerbrutus.services.valid_services[service]["port"]
            if self.options['PORT'].value:
                port = self.options['PORT'].value


            #if '/' not in args.users and '.' not in args.users and '\\' not in args.users:
            if not os.path.exits(self.options['USERS'].value):
                users = [self.options['USERS'].value]
            else:
                try:
                    userfile = Cerbrutus.Wordlist(self.options['USERS'].value)
                    users = userfile.read()
                except FileNotFoundError as e:
                    print(e)
                    sys.exit()

            #if '/' not in args.passwords and '.' not in args.passwords and '\\' not in args.passwords:
            if not os.path.exits(self.options['PASSWORDS'].value):
                passwords = [self.options['PASSWORDS'].value]
            else:
                try:
                    passfile = Cerbrutus.Wordlist(self.options['PASSWORDS'].value)
                    print("[*] - Initialising password list...")
                    passwords = passfile.read()
                except FileNotFoundError as e:
                    print(e)
                    sys.exit()

            threads = Cerbrutus.services.valid_services[service]["reccomendedThreads"]
            if self.options['THREADS'].value is not None:
                try:
                    threads = self.options['THREADS'].value
                except Exception:
                    print("[-] - Specified number of threads was not a number.")
                    sys.exit()

            Cerbrutus.BruteUtil(host, port, service, users, passwords, threads=threads).brute()

        except Exception as error:
            print(error) # print_failure
