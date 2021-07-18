#!/usr/bin/env python3
# Search wordlists in a supplied directory

import os
from typing import Set
from pathlib import Path


def search_wordlists(sdir:Path, exclude:Set[Path] = None): 
	if exclude is None:
		exclude = set()
		
	wordlists = []
	if os.path.isdir(sdir):
		for wordlist_name in os.listdir(sdir):
		    wordlist_file = os.path.join(sdir, wordlist_name)
		    if os.path.isfile(wordlist_file) and wordlist_name not in exclude:
		        wordlists.append(wordlist_file)

	return wordlists
