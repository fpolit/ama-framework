#!/usr/bin/env python3
#
# hybrid attack using john
# NOTE: rewite module (copied from john_wordlist module)
#
# date: Feb 21 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# base  imports
from ama.core.modules.base import Attack

# cracker imports
from ama.core.cracker import John

# slurm imports
from ama.core.slurm import Slurm


class JohnHybrid(Attack):
    """
    Hybrid Attack using john cracker
    """

    name = "Wordlist attack using John The Ripper"
    mname = "attack/hashes/john_wordlist"
    author = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    description = (
        """
        Perform wordlists attacks against hashes
        with john submiting parallel tasks in a cluster using Slurm
        """
    )

    def __init__(self, worklist, hashType, hashFile, slurm):

        attackOptions = {
            'wordlist': wordlist,
            'hash_type': hashType,
            'hash_file': hashFile
        }

        initOptions = {'name': name,
                       'mname' : nname,
                       'author': author,
                       'description': description,
                       'slurm': slurm,
                       'atackOptions': attackOptions
                       }

        super().__init__(**initOptions)


    def attack(self):
        """
        Wordlist attack using John the Ripper
        """
        jtr = John()
        cmd2.Cmd.poutput(f"Attacking {hashType} hashes in {hashFile} file with {wordlist} wordlist.")
        if self.slurm.partition:
            parallelJobType = self.slurm.parserParallelJob()
            if not  parallelJobType in ["MPI", "OMP"]:
                raise ParallelWorkError(parallelJobType)

            core, extra = self.slurm.parameters()
            attackOpt = self.options['attack']
            if parallelJobType == "MPI":
                parallelWork = [
                    (
                        f"srun --mpi={self.slurm.pmix}"
                        f" {jtr.mainexec} --wordlist={attackOpt.wordlist}"
                        f" --format={attackOpt.hashType} {attackOpt.hashFile}"
                    )
                ]

            elif parallelJobType == "OMP":
                parallelWork = [
                    (
                        f"{jtr.mainexec}"
                        f" --wordlist={attackOpt.wordlist}"
                        f" --format={attackOpt.hashType}"
                        f" {attackOpt.hashFile}"
                    )
                ]


            Slurm.genScript(core, extra, parallelWork)

            slurmScriptName = extra['slurm-script']
            Bash.exec(f"sbatch {slurmScriptName}")

        else:
            wordlistAttack =  (
                f"{jtr.mainexec}"
                f" --wordlist={attackOpt.wordlist}"
                f" --format={attackOpt.hashType}"
                f" {attackOpt.hashFile}"
            )
            Bash.exec(wordlistAttack)

