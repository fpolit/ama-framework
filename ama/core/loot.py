#!/usr/bin/env python3
#
# ama subcommand - show loots (cracked hashes and credentials)
#
# date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# fineprint imports
from fineprint.status import print_status

# cliff imports
from cliff.lister import Lister

# psycopg2
import psycopg2


# core/cracker imports
#from .cracker import PasswordCracker

class LootHashes(Lister):
    """
    Show loots (cracked hashes)
    """
    def get_parser(self, prog_name):
        parser = super(LootHashes, self).get_parser(prog_name)

        parser.add_argument('-cr', '--cracker', type=str, choices=["jtr", "hc"], #choices=PasswordCracker.hashCrackers,
                            help="Hash Cracker")
        parser.add_argument('-m', dest='hashType', help="hash type")

        return parser

    def take_action(self, parsed_args):
        # MAKE A QUERY TO DB
        cracker = parsed_args.cracker
        hashType = parsed_args.hashType

        print_status(f"QUERY TO DB: hashType={hashType}, cracker={cracker}")

        return None # RETURN THE QUERY


class LootCredential(Lister):
    """
    Show loots (cracked credential)
    """
    def get_parser(self, prog_name):
        parser = super(LootCredential, self).get_parser(prog_name)
        parser.add_argument('target',
                            help="target IP or domainame")
        parser.add_argument('-s', '--services', nargs='+',
                            help="target services")
        return parser

    def take_action(self,parsed_args):
        target = parsed_args.target
        services = parsed_args.services

        print_status(f"QUERY TO DB: target={target}, services={services}")

        return None # RETURN THE QUERY
