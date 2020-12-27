#!/usr/bin/env python3
import json
import os
from os.path import expanduser
from os.path import join


pwd = os.getcwd()
hashesjson = join(pwd, 'hhash.json')
with open(hashesjson, 'r') as hash_hashcat:
    hc_hashes = json.load(hash_hashcat) 