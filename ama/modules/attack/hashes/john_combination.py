#!/usr/bin/env python3
#
# combination attack using john
#
# date: Feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from itertools import combinations
from pathlib import Path
from typing import List, Any
import os

# base  imports
from ama.modules import Attack, Auxiliary

from ama.utils import Argument
from ama.plugins.cracker import John
from ama.utils.files import only_name
from ama.utils import Shell, search_wordlists

from hcutils import pycombinator


class JohnCombination(Attack):
    """
    Combination Attack using john cracker
    """

    DESCRIPTION = "Combination attack using John The Ripper"
    MNAME = "attack/hashes/john_combination"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]
    FULLDESCRIPTION = (
        """
        Combine wordlists (2 by 2) to perform a wordlist attack
        """
    )
    REFERENCES = []

    def __init__(self, *,
             htype:str = None, hashes_file:str = None, wordlists: str=None,
             storage_dir:str = None,
             pre_attack: Auxiliary = None, post_attack: Auxiliary = None):
        """
        Initialization of John combination attack

        Args:
        hashType (str): Jonh's hash type
        hashesFile (str): Hashes file to attack
        slurm (Slurm): Instance of Slurm class
        """

        if storage_dir is None:
	        storage_dir = os.getcwd()

        attack_options = {
	        'WORDLISTS': Argument(wordlists, True, "Wordlists to combine (directory or list split by commas)"),
                'EXCLUDE': Argument(None, False, "Wordlists to exclude (split by commas)"),
                'HASH_TYPE': Argument(htype, True, "John hash types (split by commas)"),
                'HASHES_FILE': Argument(hashes_file, True, "hashes file"),
                'STORAGE_DIR': Argument(storage_dir, True, "Directory to save combinations"),
                "CORES": Argument(1, False, "Number of cores to lunch MPI job (-1: MAXIMUM CORES)", value_type=int),
                "THREADS": Argument(-1, False, "Number of threads to lunch OMP job (-1: MAXIMUM THREADS)", value_type=int),
                'JOB_NAME': Argument('jtr-combination-%j', True, "Job name"),
                'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }


        init_options = {
            'mname' : JohnCombination.MNAME,
            'authors': JohnCombination.AUTHORS,
            'description': JohnCombination.DESCRIPTION,
            'fulldescription':  JohnCombination.FULLDESCRIPTION,
	        'references': JohnCombination.REFERENCES,
            'attack_options': attack_options,
	        'pre_attack': pre_attack,
            'post_attack': post_attack
        }

        super().__init__(**init_options)


    def attack(self, quiet:bool = False, pre_attack_output: Any = None):
        """
        Combination attack using John the Ripper
        """
        try:
	        #import pdb; pdb.set_trace()

	        jtr = John()

	        hash_type = self.options['HASH_TYPE'].value
	        wordlists_option = self.options['WORDLISTS'].value
	        exclude = set()

	        if self.options['EXCLUDE'].value:
	                exclude = set(self.options['EXCLUDE'].value.split(','))

	        wordlists = []
	        if os.path.isdir(wordlists_option):
		        sdir = Path(wordlists_option)
		        wordlists += search_wordlists(sdir, exclude)

	        else:
		        for wordlist_file in wordlists_options.split(','):
			        if os.path.isfile(wordlist_file) and wordlist_file not in exclude:
				        wordlists.append(wordlist_file)
				        
	        storage_dir = self.options['STORAGE_DIR'].value
				        
	        for wl1, wl2 in combinations(wordlists, 2):
		        wl1_name = only_name(wl1)
		        wl2_name = only_name(wl2)

		        output_name = wl1_name + '_' + wl2_name + ".txt"
		        output = os.path.join(storage_dir, output_name)
		        
		        
		        status = combine2wls(wl1, wl2, output, False)
		        
		        if status != 0:
			        continue
			        
		        jtr.wordlist_attack(htype = hash_type,
							        hashes_file = self.options['HASHES_FILE'].value,
				                	wordlists = [output],
				                	cores = self.options['CORES'].value,
				                	threads = self.options['THREADS'].value)
                
                
                        
        except Exception as error:
	        print(error)
	        
    
def combine2wls(wl1, wl2, output, inverse):
    Shell.exec(f"echo -e '[*] Combining {wl1} and {wl2} into {output}'")
    status = pycombinator(wl1, wl2, output)

    inv_status = 0
    if inverse:
        Shell.exec(f"echo -w '[*] Combining {wl1} and {wl2} into {output}'")
        inv_status = pycombinator(wl1, wl2, output)

    return status or inv_status
    
