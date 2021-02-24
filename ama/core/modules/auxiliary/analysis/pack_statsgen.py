#!/usr/bin/env python3
#
# statsgen pack - auxiliary/analysis/pack_statsgen ama module
#
# date: Feb 23 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# cmd2 import
import cmd2

# typing import
from typing import (
    List
)

# module.base imports
from ama.core.modules.base import Auxiliary

# pack import
from ama.core.auxiliary.analysis.pack import (
    StatsGen,
    getPackversion,
    getPackBanner
)

# validator imports
from ama.core.validator import Args


class PackStatsgen(Auxiliary):
    """
    Wordlist analysis using pack-statsgen
    """

    description = "Wordlist analysis using pack-statsgen"
    mname = "auxiliary/analysis/pack_statsgen"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    fulldescription = (
        """
        Perform a wordlist analysis using pack-statsgen
        submiting tasks in a cluster using Slurm
        """
    )

    def __init__(self, *,
                 wordlist: str = None, output: str = None,
                 minlength: int = None , maxlenght: int = None,
                 simplemask: List[str], charset: List[str],
                 quiet=False, hiderare=False, slurm=None):
        self.banner = getPackBanner()

        auxiliaryOptions = {
            'wordlist': wordlist,
            'output': output,
            'minlength': minlength,
            'maxlength': maxlength,
            'simplemask': simplemask,
            'charset': charset,
            'quiet':  quiet
            'hiderare': hiderare,
        }

        initOptions = {
            'mname': mname,
            'author': author,
            'description': description,
            'fulldescription':  fulldescription,
            'auxiliaryOptions': auxiliaryOptions,
            'slurm': slurm
        }

        super().__init__(**initOptions)


    def run(self):
        Args.notNone(self.wordlist)
        # Print program header
        if not self.quiet:
            cmd2.Cmd.poutput(self.banner)

        cmd2.Cmd.poutput(f"[*] Analyzing passwords in {self.wordlist}")

        statsgen = StatsGen(**self.auxiliary)
        statsgen.generate_stats()
        statsgen.print_stats()
